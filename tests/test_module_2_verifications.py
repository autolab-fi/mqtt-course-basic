import pathlib
import sys


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKER_ROOT = pathlib.Path("/root/git-images/mqtt-worker")
for path in (PROJECT_ROOT, WORKER_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from attempt_runtime import AttemptRuntime, extract_code_features
from verifications.module_2 import get_verification_config, verify_attempt


def make_runtime(*, code: str, mqtt_messages=None, checker_commands=None, final_status="ok"):
    parsed_code, code_features = extract_code_features(code)
    return AttemptRuntime(
        user_id="32",
        submission_id="2001",
        task="led_command_listener",
        module="module_2",
        attempt_topic_root="edu/32/2001",
        code=code,
        enabled_layers={"runtime_mqtt": True, "code_check": True, "video_check": False},
        mqtt_messages=mqtt_messages or [],
        telemetry_messages=[item for item in (mqtt_messages or []) if item["topic"].endswith("/telemetry")],
        event_messages=[item for item in (mqtt_messages or []) if item["topic"].endswith("/event")],
        checker_commands=checker_commands or [],
        parsed_code=parsed_code,
        code_features=code_features,
        final_status=final_status,
    )


def test_led_command_listener_verifier_passes_happy_path():
    mqtt_messages = [
        {"topic": "edu/32/2001/telemetry", "payload": {"name": "led_ready", "value": 1, "ts": 1}, "received_at": 1.0, "source": "broker"},
        {"topic": "edu/32/2001/event", "payload": {"name": "led", "event": "changed", "state": True, "ts": 2}, "received_at": 2.0, "source": "broker"},
    ]
    code = """
client = make_mqtt_client()
client.connect()
client.subscribe((ATTEMPT_TOPIC_ROOT + "/command").encode())
client.publish((ATTEMPT_TOPIC_ROOT + "/telemetry").encode(), b'{"name":"led_ready","value":1}')
for _ in range(10):
    client.check_msg()
client.publish((ATTEMPT_TOPIC_ROOT + "/event").encode(), b'{"name":"led","event":"changed","state":true}')
client.disconnect()
"""
    runtime = make_runtime(
        code=code,
        mqtt_messages=mqtt_messages,
        checker_commands=[{"topic": "edu/32/2001/command", "payload": {"target": "led"}, "sent_at": 1.5}],
    )

    _td, result = verify_attempt(runtime, None)

    assert result["success"] is True


def test_led_command_listener_verifier_fails_without_ready_telemetry():
    code = "client = make_mqtt_client()\nclient.connect()\nclient.subscribe((ATTEMPT_TOPIC_ROOT + '/command').encode())\nfor _ in range(5):\n    client.check_msg()\nclient.disconnect()\n"
    runtime = make_runtime(
        code=code,
        mqtt_messages=[],
        checker_commands=[{"topic": "edu/32/2001/command", "payload": {"target": "led"}, "sent_at": 1.5}],
    )

    _td, result = verify_attempt(runtime, None)

    assert result["success"] is False
    assert "Ready telemetry missing" in result["description"]


def test_led_command_listener_verifier_fails_without_bounded_loop():
    mqtt_messages = [
        {"topic": "edu/32/2001/telemetry", "payload": {"name": "led_ready", "value": 1, "ts": 1}, "received_at": 1.0, "source": "broker"},
        {"topic": "edu/32/2001/event", "payload": {"name": "led", "event": "changed", "state": True, "ts": 2}, "received_at": 2.0, "source": "broker"},
    ]
    code = """
client = make_mqtt_client()
client.connect()
client.subscribe((ATTEMPT_TOPIC_ROOT + "/command").encode())
while True:
    client.check_msg()
"""
    runtime = make_runtime(
        code=code,
        mqtt_messages=mqtt_messages,
        checker_commands=[{"topic": "edu/32/2001/command", "payload": {"target": "led"}, "sent_at": 1.5}],
        final_status="timeout",
    )

    _td, result = verify_attempt(runtime, None)

    assert result["success"] is False
    assert "Student runtime timed out" in result["description"] or "wait forever" in result["description"]


def test_module_2_exposes_task_level_timeout_contract():
    config = get_verification_config("led_command_listener")

    assert config["attempt_timeout_s"] == 30.0
    assert config["stream_ready_timeout_s"] == 30.0
