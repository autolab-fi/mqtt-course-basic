# MQTT Verification Function Guide

This course uses a lesson-specific verification function stored in the course repository and executed by `mqtt-worker`.

## Function signature

Every MQTT course verification module must export:

```python
def verify_attempt(attempt_runtime, td=None):
    ...
    return td, result
```

Where:
- `attempt_runtime` is the worker-collected context for one student submission
- `td` is lesson-managed persistent verification state
- `result` is a dictionary with verification outcome data

## Required result fields

The returned `result` dictionary must include:

```python
{
    "success": True or False,
    "description": "human-readable status",
}
```

Recommended fields:

```python
{
    "score": 0..100,
    "stage": "event_received",
    "details": {...}
}
```

## What `attempt_runtime` contains

Core fields:
- `user_id`
- `submission_id`
- `task`
- `module`
- `attempt_topic_root`
- `code`
- `enabled_layers`

Runtime MQTT fields:
- `mqtt_messages`
- `telemetry_messages`
- `event_messages`
- `state_messages`
- `system_messages`
- `checker_commands`
- `stage_timestamps`

Runtime output fields:
- `runtime_output`
- `runtime_error`
- `final_status`

Code-check fields:
- `parsed_code`
- `code_features`

Video placeholders:
- `stream_ready`
- `current_frame`
- `frame_timestamp`
- `video_artifacts`

## Helper methods

`attempt_runtime` exposes helper methods so verifiers can stay small:

- `find_message(topic=None, predicate=None)`
- `find_messages(topic=None, predicate=None)`
- `last_message(topic=None, predicate=None)`
- `saw_stage(name)`
- `has_runtime_error()`
- `topic(name)`
- `layer_enabled(name)`

## Verification authoring rules

- Verification functions must be deterministic.
- Verification functions must not perform MQTT I/O directly.
- Verification functions must not mutate worker state.
- Verification functions should return learner-safe descriptions.
- Lessons may enable any combination of:
  - `runtime_mqtt`
  - `code_check`
  - `video_check`

## Current course policy

The course framework supports three layers:

1. Runtime MQTT check
2. Code check
3. Video check

Each lesson enables only the layers it needs. For `module_2.1`, use:

- `runtime_mqtt = true`
- `code_check = true`
- `video_check = false`
