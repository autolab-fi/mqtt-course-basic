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
- a compact `lessons-list.json` with 3 teaching modules and 7 beginner lessons
- lesson content for the current LED-only lesson set
- verification handlers that can be connected to `mqtt-worker`
- example solutions for local debugging and worker smoke tests

## Planned Course Direction

The current draft assumes a progression like this:

1. 30-second sandbox for trying code
2. MQTT publish/connect/disconnect basics
3. Subscribe, poll, and parse JSON commands
4. Control the ESP32 LED and publish event/state messages
