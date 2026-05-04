# Course Notes

This repository is a draft course package for an MQTT-first ESP32 lab track.

## Assumptions

- student code runs on an `ESP32`
- MQTT is the primary device communication channel
- some tasks are verified only through MQTT traffic
- some tasks may additionally use camera-based confirmation
- backend stores telemetry and exposes historical and realtime data

## Naming Direction

The first draft assumes topic names close to:

- `edu/<student_id>/<submission_id>/sensor`
- `edu/<student_id>/<submission_id>/state/...`
- `edu/<student_id>/<submission_id>/command/...`

Exact topic contracts should later be aligned with `mqtt-worker` and backend routing.
