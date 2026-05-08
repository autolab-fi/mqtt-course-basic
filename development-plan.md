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
