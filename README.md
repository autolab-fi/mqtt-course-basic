# mqtt-course-basic
Course scaffold for an introductory MQTT and ESP32 lab course on [ondroid.org](https://ondroid.org).

## Purpose

This repository is a starting point for a real-hardware IoT course built around:

- `ESP32`
- MQTT telemetry and commands
- one visible LED output
- JSON command parsing
- worker-observed MQTT verification

The directory layout intentionally follows the same structure as `lineRobot-micropython-course` so the course can be adapted without changing the expected repository shape.

## Lab Architecture

Students are not running a simulator. Each attempt is uploaded to a real ESP32 board running MicroPython firmware. The board connects to Wi-Fi and to an MQTT broker, receives the uploaded attempt from the lab worker, runs the code, and publishes output back through MQTT.

The main parts are:

- **Student code**: short MicroPython programs written in the lesson editor.
- **MQTT broker**: the message router between the board, checker, and worker.
- **ESP32 firmware**: provides `make_mqtt_client()`, file upload support, and controlled code execution.
- **Worker**: uploads code, subscribes to the attempt topics, sends checker commands, and evaluates the observed MQTT messages.
- **Attempt topics**: every submission gets its own `ATTEMPT_TOPIC_ROOT`, so messages from different attempts do not mix.

Typical message flow:

1. The worker uploads the student's program to the ESP32.
2. The worker starts the program and subscribes to `telemetry`, `event`, and `state` topics for that attempt.
3. The student's code connects to MQTT and publishes telemetry or waits for commands.
4. For command lessons, the worker publishes a JSON command to the attempt command topic.
5. The verifier checks the messages produced by the real board.

## MQTT Concepts Used in This Course

- **Client**: a program or device connected to the MQTT broker.
- **Broker**: the server that receives published messages and delivers them to subscribers.
- **Topic**: a string address such as `edu/user/submission/telemetry`.
- **Publish**: send a message to a topic.
- **Subscribe**: ask the broker to deliver messages from a topic.
- **Payload**: the message body. In this course payloads are JSON text encoded as bytes.
- **Telemetry**: device-to-checker information such as ready or status messages.
- **Command**: checker-to-device instructions.
- **Event**: a report that something happened.
- **State**: the final known device state.

## Repository Structure

- `course-info.json`: main course metadata for the platform
- `course-info-metropolia.json`: alternate metadata variant for another deployment
- `lessons-list.json`: module and lesson index used by the platform
- `lessons/`: Markdown lesson content grouped by module
- `images/`: course and module image assets
- `docs/`: maintainer documentation and verification notes
- `verifications/`: module-level verification placeholders

## Current Scope

This repository is only a scaffold. It contains:

- rewritten course metadata for an MQTT/ESP32 course
- a compact `lessons-list.json` with 3 teaching modules and 10 beginner lessons
- lesson content for the current LED-only lesson set
- verification handlers that can be connected to `mqtt-worker`
- example solutions for local debugging and worker smoke tests

## Planned Course Direction

The current draft assumes a progression like this:

1. 30-second sandbox for trying code
2. MQTT publish/connect/disconnect basics
3. Subscribe, poll, and parse JSON commands
4. Directly control the ESP32 LED and publish events
5. Subscribe, poll, and parse JSON commands
6. Control the ESP32 LED and publish event/state messages
