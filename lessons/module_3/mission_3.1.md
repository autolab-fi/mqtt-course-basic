# Lesson 5: Threshold Rule on the Device

## Lesson objective
Implement local automation logic on the ESP32 while still reporting telemetry and state.

## Introduction
Not every IoT action has to come from the backend. In many realistic systems, the device reacts locally to a sensor threshold and still reports what it did.

That makes the device both observable and autonomous.

## Assignment
Create a rule such as:

- if `light` is below a threshold, turn the LED on
- if `temperature` is above a threshold, move the servo to a warning position

Your program should:

- keep publishing telemetry
- apply the local rule
- publish the actuator state after the rule triggers

Suggested extension:
- still allow a remote MQTT command to override the actuator state

## Conclusion
This is the most realistic single-device assignment in the course, because it combines sensing, local decision-making, reporting, and visible hardware output.
