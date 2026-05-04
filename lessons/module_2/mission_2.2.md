# Lesson 4: Servo Control Basics

## Lesson objective
Control a servo motor from MQTT and report the actual angle.

## Introduction
Servo control is one of the most interesting lab outputs because it is both physically visible and easy to verify. A servo can represent:

- a vent
- a blind
- a pointer
- a small mechanical flag

## Assignment
Write a program that:

- subscribes to a servo command topic
- parses a JSON payload with an `angle`
- validates the angle before moving the servo
- moves the servo to the requested position
- publishes the resulting angle to a state topic

Suggested first command payload:

```json
{
  "angle": 90
}
```

Suggested first angles:

- `0`
- `90`
- `180`

## Conclusion
This lesson introduces actuator control that is much more expressive than a simple LED while still remaining practical for automatic verification.
