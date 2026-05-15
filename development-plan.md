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

## Lesson Visuals Plan

Goal:

- make every lesson visually explain the one new concept it introduces
- reuse a consistent ESP32/MQTT visual language across the course
- prefer diagrams, message-flow graphics, and small UI-like protocol examples
  over decorative images
- keep hardware visuals concrete: ESP32 board, GPIO 13 LED, MQTT broker,
  worker/checker, and attempt topics

Shared visual system:

- Use the same four actors in architecture diagrams:
  - student code on ESP32
  - MQTT broker
  - worker/checker
  - attempt topic namespace
- Use consistent colors by message type:
  - telemetry: blue
  - command: orange
  - event: green
  - state: purple
- Show MQTT topics as labels on arrows, not as long paragraphs.
- Show JSON payloads as compact code cards beside the relevant arrow.
- Keep diagrams simple enough to fit inside a lesson page without horizontal
  scrolling.
- Store final assets under `images/lessons/` using stable names such as
  `lesson-01-sandbox-flow.png`.

Recommended assets by lesson:

1. `Lesson 1: 30-Second MQTT Sandbox`
   - Asset: sandbox run timeline.
   - Format: horizontal timeline from upload to run, collect output, timeout or
     finish.
   - Purpose: explain that the code runs on a real ESP32 and the 30-second limit
     protects shared hardware.
   - Suggested filename: `images/lessons/lesson-01-sandbox-timeline.png`.

2. `Lesson 2: Publish One JSON Message`
   - Asset: first publish path.
   - Format: ESP32 publishes one telemetry arrow through the broker to the
     checker, with the JSON payload shown next to the arrow.
   - Purpose: make topic, payload, JSON, and `publish(...)` visible as one
     action.
   - Suggested filename: `images/lessons/lesson-02-telemetry-publish.png`.

3. `Lesson 3: Connect, Publish, Disconnect`
   - Asset: MQTT lifecycle strip.
   - Format: four-step sequence: create client, connect, publish, disconnect.
   - Purpose: reinforce the complete short-program lifecycle and why cleanup
     matters.
   - Suggested filename: `images/lessons/lesson-03-mqtt-lifecycle.png`.

4. `Lesson 4: Turn LED On and Report It`
   - Asset: GPIO-to-event diagram.
   - Format: ESP32 pin GPIO 13 lights an LED, then an event message travels to
     the checker.
   - Purpose: connect physical output with MQTT confirmation.
   - Suggested filename: `images/lessons/lesson-04-led-on-event.png`.

5. `Lesson 5: Turn LED Off and Report It`
   - Asset: on/off GPIO comparison.
   - Format: split diagram showing `led.value(1)` as LED on and `led.value(0)`
     as LED off, with the required false event payload.
   - Purpose: make the boolean and GPIO value mapping obvious.
   - Suggested filename: `images/lessons/lesson-05-led-off-event.png`.

6. `Lesson 6: Minimal LED Command Listener`
   - Asset: subscribe-callback-poll loop.
   - Format: loop diagram: subscribe to command, checker sends command,
     `check_msg()` runs callback, callback turns LED on.
   - Purpose: explain why receiving MQTT messages needs both a callback and
     polling in `umqtt.simple`.
   - Suggested filename: `images/lessons/lesson-06-command-listener-loop.png`.

7. `Lesson 7: Subscribe and Poll Commands`
   - Asset: ready-before-command handshake.
   - Format: sequence diagram: ESP32 subscribes, publishes `command_ready`,
     worker sends command, ESP32 polls with `check_msg()`.
   - Purpose: show why the ready telemetry prevents the checker from sending a
     command before the board is listening.
   - Suggested filename: `images/lessons/lesson-07-ready-handshake.png`.

8. `Lesson 8: Parse a JSON Command`
   - Asset: bytes-to-dictionary transformation.
   - Format: pipeline from MQTT payload bytes to decoded text to
     `json.loads(...)` dictionary to parsed event.
   - Purpose: make clear that MQTT transports bytes and JSON parsing is a
     separate program step.
   - Suggested filename: `images/lessons/lesson-08-json-parse-pipeline.png`.

9. `Lesson 9: Control the LED from MQTT`
   - Asset: full command-action-event loop.
   - Format: worker sends JSON command, ESP32 parses it, GPIO 13 changes LED,
     ESP32 publishes `led changed` event.
   - Purpose: show the first complete physical IoT control loop.
   - Suggested filename: `images/lessons/lesson-09-led-command-loop.png`.

10. `Lesson 10: LED State Protocol`
    - Asset: protocol map for command, event, and state.
    - Format: compact protocol diagram with three channels:
      `command -> hardware action -> event + state`.
    - Purpose: explain the difference between event history and final known
      state.
    - Suggested filename: `images/lessons/lesson-10-state-protocol.png`.

Additional course-level visuals:

- Course hero image: real ESP32 board connected to an MQTT broker/cloud concept,
  with one visible LED as the central hardware cue.
- Module 1 overview: MQTT basics map with broker, topics, publish, and lifecycle.
- Module 2 overview: command receiving map with subscribe, callback, polling,
  JSON command, and LED output.
- Module 3 overview: small device protocol map showing command, event, and
  state as separate channels.

Implementation tasks:

1. Create `images/lessons/`.
2. Produce a first low-fidelity diagram set as SVG or PNG drafts.
3. Add each image to the matching lesson near `Lab architecture` or
   `MQTT concepts`, depending on where the concept is introduced.
4. Review mobile rendering in the Ondroid lesson page so diagrams stay readable.
5. Replace draft diagrams with final visual assets after content review.
6. Add alt text for every image that states the concept, not just the visual
   appearance.
