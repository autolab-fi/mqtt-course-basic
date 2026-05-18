TASK_CONFIGS = {
    "led_state_protocol": {
        "attempt_timeout_s": 30.0,
        "stream_ready_timeout_s": 30.0,
    }
}


def get_verification_config(task=None):
    if task is None:
        return {}
    return dict(TASK_CONFIGS.get(task, {}))


def verify_attempt(attempt_runtime, td=None):
    if td is None:
        td = {"task": attempt_runtime.task}

    if attempt_runtime.task != "led_state_protocol":
        return td, {
            "success": False,
            "description": "No verifier is defined for task '{}' in module_3.".format(attempt_runtime.task),
            "score": 0,
            "stage": "unsupported_task",
            "details": {"task": attempt_runtime.task},
        }

    details = {
        "enabled_layers": dict(attempt_runtime.enabled_layers),
        "telemetry_seen": bool(attempt_runtime.telemetry_messages),
        "event_seen": bool(attempt_runtime.event_messages),
        "state_seen": bool(attempt_runtime.state_messages),
        "final_status": attempt_runtime.final_status,
        "runtime_error": attempt_runtime.runtime_error,
        "code_features": dict(attempt_runtime.code_features),
    }

    ready_msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("telemetry"),
        predicate=lambda item: item["payload"].get("name") == "protocol_ready" and item["payload"].get("value") == 1,
    )
    if ready_msg is None:
        return _fail(td, "Protocol ready telemetry missing on the attempt telemetry topic.", "ready_telemetry_missing", details)

    state_msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("state"),
        predicate=lambda item: item["payload"].get("target") == "led" and item["payload"].get("state") is True,
    )
    if state_msg is None:
        return _fail(td, "Final LED state missing. Publish target='led' and state=true to the state topic.", "state_missing", details)

    event_msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("event"),
        predicate=lambda item: item["payload"].get("name") == "led"
        and item["payload"].get("event") == "changed"
        and item["payload"].get("state") is True,
    )
    if event_msg is None:
        return _fail(td, "LED changed event missing on the event topic.", "event_missing", details)

    if not _has_pin_output(attempt_runtime):
        return _fail(td, "Create LED outputs on GPIO 2 and GPIO 4, for example leds = [Pin(2, Pin.OUT), Pin(4, Pin.OUT)].", "code_check_pin", details)

    if "toggle" not in attempt_runtime.code:
        return _fail(td, "The final protocol must support the 'toggle' action.", "code_check_toggle", details)

    if "json.loads(" not in attempt_runtime.code and ".loads(" not in attempt_runtime.code:
        return _fail(td, "Parse command payloads with json.loads(...).", "code_check_json_loads", details)

    details["ready_payload"] = ready_msg["payload"]
    details["state_payload"] = state_msg["payload"]
    details["event_payload"] = event_msg["payload"]
    return td, {
        "success": True,
        "description": "LED protocol handled the command and published event plus state.",
        "score": 100,
        "stage": "state_protocol_received",
        "details": details,
    }


def _fail(td, description, stage, details):
    return td, {"success": False, "description": description, "score": 0, "stage": stage, "details": details}


def _has_pin_output(attempt_runtime):
    compact = attempt_runtime.code.replace(" ", "")
    return _has_required_pin(compact, 2) and _has_required_pin(compact, 4)


def _has_required_pin(compact, pin):
    return "Pin({},Pin.OUT".format(pin) in compact or "Pin({},machine.Pin.OUT".format(pin) in compact
