# mqtt-course-basic
Course scaffold for an introductory MQTT and ESP32 lab course on [ondroid.org](https://ondroid.org).

## Purpose

This repository is a starting point for a real-hardware IoT course built around:

- `ESP32`
- MQTT telemetry and commands
- sensor readings
- actuator control such as LEDs and servo motors
- backend ingestion and dashboards
- optional camera-based verification

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
- a compact `lessons-list.json` with 3 teaching modules and 5 core lessons
- placeholder lesson content for the current lesson set
- verification placeholders that can later be connected to `mqtt-worker`

## Planned Course Direction

The current draft assumes a progression like this:

1. MQTT foundations and first telemetry
2. Remote device control with visible outputs
3. Integrated local automation on the device
