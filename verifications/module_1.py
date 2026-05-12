TASK_CONFIGS = {
    "sandbox_30s": {
        "attempt_timeout_s": 30.0,
        "stream_ready_timeout_s": 30.0,
    },
    "publish_telemetry_json": {
        "attempt_timeout_s": 15.0,
        "stream_ready_timeout_s": 15.0,
    },
    "connect_publish_disconnect": {
        "attempt_timeout_s": 15.0,
        "stream_ready_timeout_s": 15.0,
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
        "sandbox_30s": _verify_sandbox_30s,
        "publish_telemetry_json": _verify_publish_telemetry_json,
        "connect_publish_disconnect": _verify_connect_publish_disconnect,
    }
    handler = handlers.get(attempt_runtime.task)
    if handler is None:
        return _unsupported(attempt_runtime, td)
    return handler(attempt_runtime, td)


def _verify_sandbox_30s(attempt_runtime, td):
    details = _details(attempt_runtime)

    if attempt_runtime.has_runtime_error():
        return _fail(td, "Sandbox code failed with a runtime error.", "sandbox_runtime_error", details)

    if attempt_runtime.final_status == "timeout":
        return td, {
            "success": True,
            "description": "Sandbox ran for 30 seconds and was stopped by timeout.",
            "score": 100,
            "stage": "sandbox_timeout_ok",
            "details": details,
        }

    return td, {
        "success": True,
        "description": "Sandbox code finished.",
        "score": 100,
        "stage": "sandbox_finished",
        "details": details,
    }


def _verify_publish_telemetry_json(attempt_runtime, td):
    details = _details(attempt_runtime)
    msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("telemetry"),
        predicate=lambda item: item["payload"].get("name") == "hello" and item["payload"].get("value") == 1,
    )
    if msg is not None:
        details["telemetry_payload"] = msg["payload"]
        return _pass(td, "Telemetry JSON message received.", "telemetry_received", details)

    return _fail(td, _missing_telemetry_hint(attempt_runtime, "hello"), "telemetry_missing", details)


def _verify_connect_publish_disconnect(attempt_runtime, td):
    details = _details(attempt_runtime)
    msg = attempt_runtime.find_message(
        topic=attempt_runtime.topic("telemetry"),
        predicate=lambda item: item["payload"].get("name") == "status" and item["payload"].get("value") == "online",
    )
    if msg is None:
        return _fail(td, _missing_telemetry_hint(attempt_runtime, "status"), "status_telemetry_missing", details)

    if not attempt_runtime.code_features.get("has_disconnect"):
        return _fail(
            td,
            "The MQTT message was received, but no disconnect() call was detected. Finish this short task with client.disconnect().",
            "code_check_disconnect",
            details,
        )

    details["telemetry_payload"] = msg["payload"]
    return _pass(td, "MQTT connect, publish, and disconnect lifecycle detected.", "lifecycle_received", details)


def _missing_telemetry_hint(attempt_runtime, expected_name):
    if attempt_runtime.has_runtime_error():
        error = attempt_runtime.runtime_error or {}
        return "Student code failed: {}: {}".format(error.get("error_type", "RuntimeError"), error.get("error", "unknown error"))
    features = attempt_runtime.code_features
    if not features.get("has_make_mqtt_client") and not features.get("has_mqtt_client_ctor"):
        return "No MQTT client creation was detected. Start with client = make_mqtt_client()."
    if not features.get("has_connect"):
        return "No connect() call was detected. Connect to the MQTT broker before publishing."
    if not features.get("has_publish"):
        return "No publish() call was detected. Publish a JSON message to the telemetry topic."
    if not features.get("has_telemetry_topic"):
        return "Publish to ATTEMPT_TOPIC_ROOT + '/telemetry'."
    return "Telemetry message '{}' was not received. Check the topic name and JSON payload fields.".format(expected_name)


def _details(attempt_runtime):
    return {
        "enabled_layers": dict(attempt_runtime.enabled_layers),
        "final_status": attempt_runtime.final_status,
        "runtime_output": list(attempt_runtime.runtime_output),
        "runtime_error": attempt_runtime.runtime_error,
        "code_features": dict(attempt_runtime.code_features),
        "mqtt_message_count": len(attempt_runtime.mqtt_messages),
    }


def _pass(td, description, stage, details):
    return td, {"success": True, "description": description, "score": 100, "stage": stage, "details": details}


def _fail(td, description, stage, details):
    return td, {"success": False, "description": description, "score": 0, "stage": stage, "details": details}


def _unsupported(attempt_runtime, td):
    return _fail(
        td,
        "No verifier is defined for task '{}' in module_1.".format(attempt_runtime.task),
        "unsupported_task",
        {"task": attempt_runtime.task},
    )
