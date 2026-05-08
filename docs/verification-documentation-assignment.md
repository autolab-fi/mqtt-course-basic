# Verification Assignment Guide

## Verification split

Verification for this course is split between two repositories:

- `mqtt-course-basic`: lesson-specific verification rules and learner-facing semantics
- `mqtt-worker`: execution framework, MQTT orchestration, runtime collection, and verifier invocation

Lesson verification logic must live in `verifications/module_<n>.py` inside the course repository.

## Standard verifier API

Each module verifier must export:

```python
def verify_attempt(attempt_runtime, td=None):
    ...
    return td, result
```

The worker loads the correct module verifier and calls it after building `attempt_runtime`.

## Layer model

Every lesson can use any subset of these layers:

- `runtime_mqtt`
- `code_check`
- `video_check`

The worker always builds one common runtime object. The lesson verifier decides which layers matter for that lesson.

## Current intended module mapping

- `module_1`: MQTT connection lifecycle and simple telemetry
- `module_2`: LED and servo command handling with reported state
- `module_3`: threshold-based local device logic

## Maintainer checklist

For every new auto-checked lesson:

- ensure the lesson `str_id` exists in `lessons-list.json`
- ensure the corresponding module verifier recognizes that task id
- define enabled verification layers
- define learner-facing pass/fail descriptions
- define required MQTT payloads and timing expectations
- define code-check requirements if the lesson teaches a specific programming pattern
- define video-check rules only when physical confirmation is truly required
