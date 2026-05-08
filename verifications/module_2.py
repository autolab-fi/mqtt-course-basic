def verify_attempt(attempt_runtime, td=None):
    if td is None:
        td = {
            "task": attempt_runtime.task,
        }

    handlers = {
        "led_command_listener": _verify_led_command_listener,
    }
    handler = handlers.get(attempt_runtime.task)
    if handler is None:
        return td, {
            "success": False,
            "description": f"No verifier is defined for task '{attempt_runtime.task}' in module_2.",
            "score": 0,
            "stage": "unsupported_task",
            "details": {"task": attempt_runtime.task},
        }
    return handler(attempt_runtime, td)


def _verify_led_command_listener(attempt_runtime, td):
    details = {
        "enabled_layers": dict(attempt_runtime.enabled_layers),
        "telemetry_seen": bool(attempt_runtime.telemetry_messages),
        "event_seen": bool(attempt_runtime.event_messages),
        "final_status": attempt_runtime.final_status,
    }

    if attempt_runtime.layer_enabled("runtime_mqtt"):
        ready_msg = attempt_runtime.find_message(
            topic=attempt_runtime.topic("telemetry"),
            predicate=lambda item: item["payload"].get("name") == "led_ready"
            and item["payload"].get("value") == 1
            and "ts" in item["payload"],
        )
        if ready_msg is None:
            return td, {
                "success": False,
                "description": "Ready telemetry missing on the attempt telemetry topic.",
                "score": 0,
                "stage": "ready_telemetry_missing",
                "details": details,
            }
        details["ready_payload"] = ready_msg["payload"]

        command_seen = any(command["topic"] == attempt_runtime.topic("command") for command in attempt_runtime.checker_commands)
        if not command_seen:
            return td, {
                "success": False,
                "description": "Checker command was not sent on the attempt command topic.",
                "score": 0,
                "stage": "checker_command_missing",
                "details": details,
            }

        event_msg = attempt_runtime.find_message(
            topic=attempt_runtime.topic("event"),
            predicate=lambda item: item["payload"].get("name") == "led"
            and item["payload"].get("event") == "changed"
            and item["payload"].get("state") is True
            and "ts" in item["payload"],
        )
        if event_msg is None:
            return td, {
                "success": False,
                "description": "LED change event missing after the checker command.",
                "score": 0,
                "stage": "event_missing",
                "details": details,
            }
        details["event_payload"] = event_msg["payload"]

        if attempt_runtime.final_status not in {"ok", None}:
            description = "Student runtime did not finish successfully."
            if attempt_runtime.final_status == "timeout":
                description = "Student runtime timed out before the exchange finished."
            elif attempt_runtime.has_runtime_error():
                error_type = attempt_runtime.runtime_error.get("error_type", "RuntimeError")
                error_text = attempt_runtime.runtime_error.get("error", "student runtime failed")
                description = f"Student runtime failed: {error_type}: {error_text}"
            return td, {
                "success": False,
                "description": description,
                "score": 0,
                "stage": "runtime_failed",
                "details": details,
            }

    if attempt_runtime.layer_enabled("code_check"):
        required_flags = {
            "has_connect": "No MQTT client connect() call detected.",
            "has_subscribe": "No MQTT subscribe() call detected.",
            "has_publish": "No MQTT publish() call detected.",
            "has_bounded_loop": "No bounded wait loop detected.",
        }
        for flag, description in required_flags.items():
            if not attempt_runtime.code_features.get(flag):
                return td, {
                    "success": False,
                    "description": description,
                    "score": 0,
                    "stage": f"code_check_{flag}",
                    "details": details,
                }

        has_client_creation = attempt_runtime.code_features.get("has_make_mqtt_client") or attempt_runtime.code_features.get(
            "has_mqtt_client_ctor"
        )
        if not has_client_creation:
            return td, {
                "success": False,
                "description": "No MQTT client creation detected.",
                "score": 0,
                "stage": "code_check_client_creation",
                "details": details,
            }

        if not (
            attempt_runtime.code_features.get("uses_mqtt_config")
            or attempt_runtime.code_features.get("has_make_mqtt_client")
        ):
            return td, {
                "success": False,
                "description": "The solution does not appear to use injected MQTT runtime configuration.",
                "score": 0,
                "stage": "code_check_config_usage",
                "details": details,
            }

        if not (
            attempt_runtime.code_features.get("has_attempt_topic_root")
            and attempt_runtime.code_features.get("has_command_topic")
            and attempt_runtime.code_features.get("has_telemetry_topic")
            and attempt_runtime.code_features.get("has_event_topic")
        ):
            return td, {
                "success": False,
                "description": "The solution does not appear to use the attempt-scoped command, telemetry, and event topics.",
                "score": 0,
                "stage": "code_check_topics",
                "details": details,
            }

        if attempt_runtime.code_features.get("has_unbounded_while_true") and not attempt_runtime.code_features.get("has_disconnect"):
            return td, {
                "success": False,
                "description": "The solution appears to wait forever without disconnecting cleanly.",
                "score": 0,
                "stage": "code_check_unbounded_wait",
                "details": details,
            }

    return td, {
        "success": True,
        "description": "Ready telemetry and LED event received, and the MQTT client lifecycle was detected.",
        "score": 100,
        "stage": "event_received",
        "details": details,
    }
