# Development Plan

## Goal

Prepare a basic course repository for a new MQTT and ESP32 lab course while preserving the repository structure used by existing Ondroid courses.

## Phase 1

- create course metadata
- define a compact module structure
- add five realistic core lessons
- add verification placeholders

## Phase 2

- attach lesson content to concrete hardware kits
- connect lessons to `mqtt-worker` verification logic
- standardize MQTT topics and payload schemas
- add example dashboards and backend API references
- use the existing `py` execution path for short-term infrastructure smoke tests
- keep the short-term smoke path separate from the long-term pedagogical MQTT API
- align early smoke tasks with the current `edu/<student_id>/<submission_id>/...` namespace

## Phase 3

- add real images and diagrams
- replace placeholder verification modules with actual checks
- align lessons with final submission and report requirements
- rewrite early lessons so students explicitly learn broker connection, authentication, subscribe, publish, and polling with `umqtt.simple`
- move lesson contracts away from ad-hoc topic drafts toward the canonical `edu/...` attempt namespace
- add a firmware/runtime milestone for long-lived student MQTT programs that can keep running independently of the service-control loop
- add a controlled stop/reset model for student runtime so worker-side timeouts can end a submission cleanly without depending on the student code to exit on its own

## Revised Course Direction

The first production version should target the hardware that already exists:

- ESP32 board
- one visible LED output
- MQTT broker connection
- worker-side MQTT observation and command injection

The course should avoid sensors and servo tasks until that hardware is actually
available. The first course version should be a seven-task MQTT/LED path where
the first task is a 30-second sandbox.

Recommended task sequence:

1. Run a small program in the 30-second sandbox.
2. Publish one JSON telemetry message.
3. Connect, publish, and disconnect cleanly.
4. Subscribe to a command topic and poll with `check_msg()`.
5. Receive and parse a JSON command.
6. Turn the LED on or off from a JSON MQTT command.
7. Implement a small LED state protocol with `on`, `off`, and `toggle`.

Canonical attempt topics:

- `ATTEMPT_TOPIC_ROOT + "/telemetry"`
- `ATTEMPT_TOPIC_ROOT + "/command"`
- `ATTEMPT_TOPIC_ROOT + "/event"`
- `ATTEMPT_TOPIC_ROOT + "/state"`

Student-facing code should use the injected runtime values already provided by
the firmware:

- `mqtt_config`
- `make_mqtt_client(...)`
- `ATTEMPT_TOPIC_ROOT`

## 30-Second Sandbox

Add a sandbox mode before, or alongside, strict lesson verification.

Goal:

- let teachers and developers run arbitrary small MicroPython snippets on the
  ESP32 through the same worker/firmware path used by lessons
- cap execution at 30 seconds
- collect stdout, runtime status, and observed MQTT messages
- avoid producing a course score unless the sandbox is explicitly attached to a
  lesson verifier

Recommended sandbox behavior:

- upload student/developer code to the board
- inject the same values as lesson attempts:
  - `ATTEMPT_USER_ID`
  - `ATTEMPT_SUBMISSION_ID`
  - `ATTEMPT_TOPIC_ROOT`
  - `mqtt_config`
  - `make_mqtt_client(...)`
- subscribe to the attempt topics:
  - telemetry
  - command
  - event
  - state
- run for at most `30` seconds
- stream or store:
  - service-plane code status
  - Python output
  - MQTT messages seen on attempt topics
  - runtime error or timeout reason
- finish with a neutral sandbox result:
  - `status: ok`
  - `status: error`
  - `status: timeout`

The sandbox should be separate from lesson scoring. It is a diagnostics and
course-authoring tool, not a replacement for task-specific verification.

## Worker Changes Needed For Lessons

The current worker already has the hard part for the LED command listener:

- code upload to ESP32
- code run request
- subscription to `telemetry`, `event`, and `state`
- checker command publish to `command`
- MQTT message collection
- code feature extraction

The next worker changes should focus on making this generic enough for all seven
lessons:

1. Add a `sandbox_30s` task or mode that uses a fixed `30` second timeout and
   returns observed output without scoring.
2. Replace the single hardcoded LED verifier flow with small reusable MQTT
   scenario steps:
   - wait for telemetry
   - publish command
   - wait for event
   - wait for state
   - validate JSON payload fields
3. Add task-specific configs for the seven lessons in the course verification
   modules.
4. Extend static code checks only where useful for beginners:
   - client creation
   - `connect()`
   - `publish()`
   - `subscribe()`
   - `check_msg()` or `wait_msg()`
   - bounded loop
   - `disconnect()`
   - `json.loads(...)` for command parsing tasks
5. Keep strict runtime MQTT checks as the main grading source. Static checks
   should explain common mistakes, not become the primary assessment.
6. Preserve service/control topics separately from student attempt topics.

## Firmware Changes Needed Later

The current synchronous code-run path is enough for short lesson attempts and
the 30-second sandbox if the guard resets the board on timeout.

For a more robust course runtime, firmware should later support:

- starting student code without blocking the service-control loop
- stopping student code explicitly
- worker-triggered cleanup after timeout
- safe board reset if student code enters an infinite loop
