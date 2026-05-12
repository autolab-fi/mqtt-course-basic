import pathlib
import sys


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKER_ROOTS = (
    pathlib.Path("/home/pi/mqtt-worker"),
    pathlib.Path("/root/git-images/mqtt-worker"),
)
for path in (PROJECT_ROOT, *WORKER_ROOTS):
    try:
        path_exists = path.exists()
    except OSError:
        path_exists = False
    if path_exists and str(path) not in sys.path:
        sys.path.insert(0, str(path))

from attempt_runtime import AttemptRuntime, extract_code_features
from verifications import module_1, module_2, module_3


def make_runtime(*, task, module, code, mqtt_messages=None, checker_commands=None, final_status="ok", runtime_error=None):
    mqtt_messages = mqtt_messages or []
    parsed_code, code_features = extract_code_features(code)
    return AttemptRuntime(
        user_id="32",
        submission_id="2001",
        task=task,
        module=module,
        attempt_topic_root="edu/32/2001",
        code=code,
        enabled_layers={"runtime_mqtt": True, "code_check": True, "video_check": False},
        mqtt_messages=mqtt_messages,
        telemetry_messages=[item for item in mqtt_messages if item["topic"].endswith("/telemetry")],
        event_messages=[item for item in mqtt_messages if item["topic"].endswith("/event")],
        state_messages=[item for item in mqtt_messages if item["topic"].endswith("/state")],
        checker_commands=checker_commands or [],
        parsed_code=parsed_code,
        code_features=code_features,
        final_status=final_status,
        runtime_error=runtime_error,
    )


def msg(topic, payload):
    return {"topic": topic, "payload": payload, "received_at": 1.0, "source": "broker"}


def test_sandbox_accepts_timeout_as_success():
    runtime = make_runtime(
        task="sandbox_30s",
        module="module_1",
        code="while True:\n    pass\n",
        final_status="timeout",
    )

    _td, result = module_1.verify_attempt(runtime, None)

    assert result["success"] is True
    assert result["stage"] == "sandbox_timeout_ok"
    assert module_1.get_verification_config("sandbox_30s")["attempt_timeout_s"] == 30.0


def test_publish_telemetry_json_passes_happy_path():
    runtime = make_runtime(
        task="publish_telemetry_json",
        module="module_1",
        code="""
client = make_mqtt_client()
client.connect()
client.publish((ATTEMPT_TOPIC_ROOT + "/telemetry").encode(), b'{"name":"hello","value":1}')
client.disconnect()
""",
        mqtt_messages=[msg("edu/32/2001/telemetry", {"name": "hello", "value": 1})],
    )

    _td, result = module_1.verify_attempt(runtime, None)

    assert result["success"] is True


def test_publish_telemetry_json_gives_beginner_hint_without_publish():
    runtime = make_runtime(
        task="publish_telemetry_json",
        module="module_1",
        code="client = make_mqtt_client()\nclient.connect()\nclient.disconnect()\n",
    )

    _td, result = module_1.verify_attempt(runtime, None)

    assert result["success"] is False
    assert "publish()" in result["description"]


def test_subscribe_command_poll_requires_polling_call():
    runtime = make_runtime(
        task="subscribe_command_poll",
        module="module_2",
        code="""
client = make_mqtt_client()
client.connect()
client.subscribe((ATTEMPT_TOPIC_ROOT + "/command").encode())
client.publish((ATTEMPT_TOPIC_ROOT + "/telemetry").encode(), b'{"name":"command_ready","value":1}')
for _ in range(5):
    pass
client.disconnect()
""",
        mqtt_messages=[msg("edu/32/2001/telemetry", {"name": "command_ready", "value": 1})],
        checker_commands=[{"topic": "edu/32/2001/command", "payload": {"target": "led"}, "sent_at": 1.5}],
    )

    _td, result = module_2.verify_attempt(runtime, None)

    assert result["success"] is False
    assert "check_msg()" in result["description"]


def test_parse_json_command_passes_happy_path():
    runtime = make_runtime(
        task="parse_json_command",
        module="module_2",
        code="""
import json
client = make_mqtt_client()
client.connect()
client.subscribe((ATTEMPT_TOPIC_ROOT + "/command").encode())
command = json.loads('{"action":"set"}')
client.publish((ATTEMPT_TOPIC_ROOT + "/telemetry").encode(), b'{"name":"command_ready","value":1}')
client.publish((ATTEMPT_TOPIC_ROOT + "/event").encode(), b'{"name":"command","event":"parsed","action":"set"}')
for _ in range(5):
    client.check_msg()
client.disconnect()
""",
        mqtt_messages=[
            msg("edu/32/2001/telemetry", {"name": "command_ready", "value": 1}),
            msg("edu/32/2001/event", {"name": "command", "event": "parsed", "action": "set"}),
        ],
    )

    _td, result = module_2.verify_attempt(runtime, None)

    assert result["success"] is True


def test_led_command_listener_passes_happy_path():
    runtime = make_runtime(
        task="led_command_listener",
        module="module_2",
        code="""
import json
client = make_mqtt_client()
client.connect()
client.subscribe((ATTEMPT_TOPIC_ROOT + "/command").encode())
client.publish((ATTEMPT_TOPIC_ROOT + "/telemetry").encode(), b'{"name":"led_ready","value":1}')
command = json.loads('{"value":true}')
for _ in range(10):
    client.check_msg()
client.publish((ATTEMPT_TOPIC_ROOT + "/event").encode(), b'{"name":"led","event":"changed","state":true}')
client.disconnect()
""",
        mqtt_messages=[
            msg("edu/32/2001/telemetry", {"name": "led_ready", "value": 1}),
            msg("edu/32/2001/event", {"name": "led", "event": "changed", "state": True}),
        ],
        checker_commands=[{"topic": "edu/32/2001/command", "payload": {"target": "led"}, "sent_at": 1.5}],
    )

    _td, result = module_2.verify_attempt(runtime, None)

    assert result["success"] is True


def test_led_state_protocol_requires_state_and_event():
    runtime = make_runtime(
        task="led_state_protocol",
        module="module_3",
        code="""
import json
client = make_mqtt_client()
client.connect()
client.subscribe((ATTEMPT_TOPIC_ROOT + "/command").encode())
action = "toggle"
command = json.loads('{"action":"toggle"}')
for _ in range(10):
    client.check_msg()
client.publish((ATTEMPT_TOPIC_ROOT + "/telemetry").encode(), b'{"name":"protocol_ready","value":1}')
client.publish((ATTEMPT_TOPIC_ROOT + "/state").encode(), b'{"target":"led","state":true}')
client.publish((ATTEMPT_TOPIC_ROOT + "/event").encode(), b'{"name":"led","event":"changed","state":true}')
client.disconnect()
""",
        mqtt_messages=[
            msg("edu/32/2001/telemetry", {"name": "protocol_ready", "value": 1}),
            msg("edu/32/2001/state", {"target": "led", "state": True}),
            msg("edu/32/2001/event", {"name": "led", "event": "changed", "state": True}),
        ],
    )

    _td, result = module_3.verify_attempt(runtime, None)

    assert result["success"] is True
    assert module_3.get_verification_config("led_state_protocol")["attempt_timeout_s"] == 30.0
