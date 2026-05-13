TASK_CONFIGS = {
    "led_on_event": {
        "attempt_timeout_s": 15.0,
        "stream_ready_timeout_s": 15.0,
    },
    "led_off_event": {
        "attempt_timeout_s": 15.0,
        "stream_ready_timeout_s": 15.0,
    },
    "led_command_on_minimal": {
        "attempt_timeout_s": 30.0,
        "stream_ready_timeout_s": 30.0,
    },
    "subscribe_command_poll": {
        "attempt_timeout_s": 30.0,
        "stream_ready_timeout_s": 30.0,
    },
    "parse_json_command": {
        "attempt_timeout_s": 30.0,
        "stream_ready_timeout_s": 30.0,
    },
    "led_command_listener": {
        "attempt_timeout_s": 30.0,
        "stream_ready_timeout_s": 30.0,
    },
}


def get_verification_config(task=None):
    if task is None:
        return {}
    return dict(TASK_CONFIGS.get(task, {}))


def verify_attempt(attempt_runtime, td=None):
    if td is None:
        td = {"task": attempt_runtime.task}

    handlers = {
        "led_on_event": _verify_led_on_event,
        "led_off_event": _verify_led_off_event,
        "led_command_on_minimal": _verify_led_command_on_minimal,
        "subscribe_command_poll": _verify_subscribe_command_poll,
        "parse_json_command": _verify_parse_json_command,
        "led_command_listener": _verify_led_command_listener,
    }
    handler = handlers.get(attempt_runtime.task)
    if handler is None:
        return _unsupported(attempt_runtime, td)
    return handler(attempt_runtime, td)


def _verify_led_on_event(attempt_runtime, td):
    return _verify_direct_led_event(
        attempt_runtime,
        td,
        expected_state=True,
        expected_value_call="value(1",
        description="LED on event received.",
        stage="led_on_event_received",
    )


def _verify_led_off_event(attempt_runtime, td):
    return _verify_direct_led_event(
        attempt_runtime,
        td,
        expected_state=False,
        expected_value_call="value(0",
        description="LED off event received.",
        stage="led_off_event_received",
    )


def _verify_direct_led_event(attempt_runtime, td, *, expected_state, expected_value_call, description, stage):
    details = _details(attempt_runtime)
    event_msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("event"),
        predicate=lambda item: item["payload"].get("name") == "led"
        and item["payload"].get("state") is expected_state,
    )
    if event_msg is None:
        if attempt_runtime.has_runtime_error():
            return _fail(td, _runtime_error_hint(attempt_runtime), "runtime_failed", details)
        if not _has_pin_output(attempt_runtime):
            return _fail(td, "Create the LED output with led = Pin(2, Pin.OUT).", "code_check_pin", details)
        if expected_value_call not in attempt_runtime.code.replace(" ", ""):
            return _fail(td, "Set the LED to the required value before publishing the event.", "code_check_led_value", details)
        if not attempt_runtime.code_features.get("has_publish"):
            return _fail(td, "Publish an MQTT event after changing the LED.", "code_check_publish", details)
        if not attempt_runtime.code_features.get("has_event_topic"):
            return _fail(td, "Publish the LED report to ATTEMPT_TOPIC_ROOT + '/event'.", "code_check_event_topic", details)
        return _fail(td, "LED event was not received. Publish name='led' and the required state.", "event_missing", details)

    if not attempt_runtime.code_features.get("has_connect"):
        return _fail(td, "No MQTT connect() call detected.", "code_check_connect", details)
    if not attempt_runtime.code_features.get("has_disconnect"):
        return _fail(td, "No disconnect() call detected. End this short task with client.disconnect().", "code_check_disconnect", details)

    details["event_payload"] = event_msg["payload"]
    return _pass(td, description, stage, details)


def _verify_led_command_on_minimal(attempt_runtime, td):
    details = _details(attempt_runtime)

    if not _checker_command_seen(attempt_runtime):
        return _fail(td, "Checker command was not sent on the attempt command topic.", "checker_command_missing", details)
    if attempt_runtime.has_runtime_error():
        return _fail(td, _runtime_error_hint(attempt_runtime), "runtime_failed", details)
    if not _has_pin_output(attempt_runtime):
        return _fail(td, "Create the LED output with led = Pin(2, Pin.OUT).", "code_check_pin", details)
    if "set_callback(" not in attempt_runtime.code:
        return _fail(td, "Register a callback with client.set_callback(...).", "code_check_callback", details)
    if not attempt_runtime.code_features.get("has_connect"):
        return _fail(td, "No MQTT connect() call detected.", "code_check_connect", details)
    if not attempt_runtime.code_features.get("has_subscribe"):
        return _fail(td, "Subscribe to ATTEMPT_TOPIC_ROOT + '/command'.", "code_check_subscribe", details)
    if not attempt_runtime.code_features.get("has_command_topic"):
        return _fail(td, "Use ATTEMPT_TOPIC_ROOT + '/command' as the command topic.", "code_check_command_topic", details)
    if not _has_poll_call(attempt_runtime):
        return _fail(td, "Call check_msg() or wait_msg() so MQTT can deliver the command.", "code_check_poll", details)
    if not attempt_runtime.code_features.get("has_bounded_loop"):
        return _fail(td, "Use a limited loop such as for _ in range(30), not an endless wait.", "code_check_bounded_loop", details)
    if "value(1" not in attempt_runtime.code.replace(" ", ""):
        return _fail(td, "Turn the LED on in the callback with led.value(1).", "code_check_led_on", details)
    if not attempt_runtime.code_features.get("has_disconnect"):
        return _fail(td, "No disconnect() call detected. End this short task with client.disconnect().", "code_check_disconnect", details)
    if attempt_runtime.final_status not in {"ok", None}:
        return _fail(td, _final_status_hint(attempt_runtime), "runtime_failed", details)

    return _pass(td, "Minimal LED command listener ran and used the expected MQTT polling shape.", "minimal_command_listener", details)


def _verify_subscribe_command_poll(attempt_runtime, td):
    details = _details(attempt_runtime)
    ready_msg = _find_telemetry(attempt_runtime, "command_ready", 1)
    if ready_msg is None:
        return _fail(td, _ready_hint(attempt_runtime, "command_ready"), "ready_telemetry_missing", details)

    if not _checker_command_seen(attempt_runtime):
        return _fail(td, "Checker command was not sent to the attempt command topic.", "checker_command_missing", details)

    if not _has_poll_call(attempt_runtime):
        return _fail(td, "Subscribe is not enough. Use check_msg() or wait_msg() to receive incoming MQTT messages.", "code_check_poll", details)

    if not attempt_runtime.code_features.get("has_bounded_loop"):
        return _fail(td, "Use a limited loop such as for _ in range(30), not an endless wait.", "code_check_bounded_loop", details)

    details["ready_payload"] = ready_msg["payload"]
    return _pass(td, "Command topic subscription and bounded polling were detected.", "command_poll_ready", details)


def _verify_parse_json_command(attempt_runtime, td):
    details = _details(attempt_runtime)
    ready_msg = _find_telemetry(attempt_runtime, "command_ready", 1)
    if ready_msg is None:
        return _fail(td, _ready_hint(attempt_runtime, "command_ready"), "ready_telemetry_missing", details)

    event_msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("event"),
        predicate=lambda item: item["payload"].get("name") == "command"
        and item["payload"].get("event") == "parsed"
        and item["payload"].get("action") == "set",
    )
    if event_msg is None:
        if not _has_json_loads(attempt_runtime):
            return _fail(td, "The command payload must be parsed with json.loads(...).", "code_check_json_loads", details)
        return _fail(td, "Parsed command event was not received. Publish name='command', event='parsed', action='set'.", "parsed_event_missing", details)

    details["ready_payload"] = ready_msg["payload"]
    details["event_payload"] = event_msg["payload"]
    return _pass(td, "JSON command was parsed and reported.", "command_parsed", details)


def _verify_led_command_listener(attempt_runtime, td):
    details = _details(attempt_runtime)
    ready_msg = _find_telemetry(attempt_runtime, "led_ready", 1)
    if ready_msg is None:
        return _fail(td, _ready_hint(attempt_runtime, "led_ready"), "ready_telemetry_missing", details)
    details["ready_payload"] = ready_msg["payload"]

    if not _checker_command_seen(attempt_runtime):
        return _fail(td, "Checker command was not sent on the attempt command topic.", "checker_command_missing", details)

    event_msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("event"),
        predicate=lambda item: item["payload"].get("name") == "led"
        and item["payload"].get("event") == "changed"
        and item["payload"].get("state") is True,
    )
    if event_msg is None:
        if attempt_runtime.has_runtime_error():
            return _fail(td, _runtime_error_hint(attempt_runtime), "runtime_failed", details)
        if not _has_json_loads(attempt_runtime):
            return _fail(td, "The LED command is JSON. Decode the message and parse it with json.loads(...).", "code_check_json_loads", details)
        return _fail(td, "LED change event missing after the checker command.", "event_missing", details)
    details["event_payload"] = event_msg["payload"]

    if attempt_runtime.final_status not in {"ok", None}:
        return _fail(td, _final_status_hint(attempt_runtime), "runtime_failed", details)

    required_flags = {
        "has_connect": "No MQTT client connect() call detected.",
        "has_subscribe": "No MQTT subscribe() call detected.",
        "has_publish": "No MQTT publish() call detected.",
        "has_bounded_loop": "No bounded wait loop detected.",
    }
    for flag, description in required_flags.items():
        if not attempt_runtime.code_features.get(flag):
            return _fail(td, description, "code_check_{}".format(flag), details)

    if not _has_poll_call(attempt_runtime):
        return _fail(td, "No check_msg() or wait_msg() call detected.", "code_check_poll", details)

    if not attempt_runtime.code_features.get("has_disconnect"):
        return _fail(td, "No disconnect() call detected. End this short task with client.disconnect().", "code_check_disconnect", details)

    return _pass(td, "Ready telemetry and LED event received, and the MQTT client lifecycle was detected.", "event_received", details)


def _has_pin_output(attempt_runtime):
    compact = attempt_runtime.code.replace(" ", "")
    return "Pin(2,Pin.OUT" in compact or "Pin(2,machine.Pin.OUT" in compact


def _find_telemetry(attempt_runtime, name, value):
    return attempt_runtime.find_message(
        topic=attempt_runtime.topic("telemetry"),
        predicate=lambda item: item["payload"].get("name") == name and item["payload"].get("value") == value,
    )


def _checker_command_seen(attempt_runtime):
    return any(command["topic"] == attempt_runtime.topic("command") for command in attempt_runtime.checker_commands)


def _has_poll_call(attempt_runtime):
    return attempt_runtime.code_features.get("has_check_msg") or attempt_runtime.code_features.get("has_wait_msg")


def _has_json_loads(attempt_runtime):
    code = attempt_runtime.code
    return "json.loads(" in code or ".loads(" in code


def _ready_hint(attempt_runtime, name):
    if attempt_runtime.has_runtime_error():
        return _runtime_error_hint(attempt_runtime)
    features = attempt_runtime.code_features
    if not features.get("has_connect"):
        return "No connect() call was detected. Connect before subscribing or publishing."
    if not features.get("has_subscribe"):
        return "No subscribe() call was detected. Subscribe to ATTEMPT_TOPIC_ROOT + '/command'."
    if not features.get("has_publish"):
        return "No publish() call was detected. Publish '{}' telemetry before waiting for commands.".format(name)
    if not features.get("has_telemetry_topic"):
        return "Ready telemetry must be published to ATTEMPT_TOPIC_ROOT + '/telemetry'."
    return "Ready telemetry '{}' missing on the attempt telemetry topic.".format(name)


def _runtime_error_hint(attempt_runtime):
    error = attempt_runtime.runtime_error or {}
    return "Student runtime failed: {}: {}".format(error.get("error_type", "RuntimeError"), error.get("error", "student runtime failed"))


def _final_status_hint(attempt_runtime):
    if attempt_runtime.final_status == "timeout":
        return "Student runtime timed out before the exchange finished. Use a bounded loop and disconnect."
    if attempt_runtime.has_runtime_error():
        return _runtime_error_hint(attempt_runtime)
    return "Student runtime did not finish successfully."


def _details(attempt_runtime):
    return {
        "enabled_layers": dict(attempt_runtime.enabled_layers),
        "telemetry_seen": bool(attempt_runtime.telemetry_messages),
        "event_seen": bool(attempt_runtime.event_messages),
        "final_status": attempt_runtime.final_status,
        "runtime_error": attempt_runtime.runtime_error,
        "code_features": dict(attempt_runtime.code_features),
    }


def _pass(td, description, stage, details):
    return td, {"success": True, "description": description, "score": 100, "stage": stage, "details": details}


def _fail(td, description, stage, details):
    return td, {"success": False, "description": description, "score": 0, "stage": stage, "details": details}


def _unsupported(attempt_runtime, td):
    return _fail(
        td,
        "No verifier is defined for task '{}' in module_2.".format(attempt_runtime.task),
        "unsupported_task",
        {"task": attempt_runtime.task},
    )
