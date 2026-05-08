# Lesson 3: One-Shot MQTT LED Smoke Test

## Lesson objective
Connect to MQTT directly, receive one command, and produce one visible response.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the first lesson where your ESP32 acts as a real MQTT client. Your code must connect to the broker itself, authenticate, subscribe to a command topic, and publish a response after acting on the command.

For this smoke version, keep the hardware output simple and robust:

- built-in LED, or
- external LED on a GPIO pin

Assume the LED is connected to `GPIO 2`.

## Assignment
Write a program that:

- reads broker host, port, username, and password from the board configuration
- creates its own MQTT client
- subscribes to the attempt command topic
- publishes one ready message to telemetry
- waits for one command for a limited time
- turns the LED on when it receives the command payload
- publishes one event message confirming the LED change
- disconnects and exits after the exchange finishes

Use the attempt-scoped topic root injected by the platform:

- `ATTEMPT_TOPIC_ROOT + "/telemetry"`
- `ATTEMPT_TOPIC_ROOT + "/command"`
- `ATTEMPT_TOPIC_ROOT + "/event"`

Required ready telemetry payload:

```json
{
  "name": "led_ready",
  "value": 1,
  "ts": 1710000000
}
```

Command payload sent by the checker:

```json
{
  "target": "led",
  "action": "set",
  "value": true,
  "ts": 1710000010
}
```

Required event payload after the LED turns on:

```json
{
  "name": "led",
  "event": "changed",
  "state": true,
  "ts": 1710000011
}
```

## Notes

- The platform injects `ATTEMPT_USER_ID`, `ATTEMPT_SUBMISSION_ID`, and `ATTEMPT_TOPIC_ROOT` before your code runs.
- The smoke task is intentionally short-lived. Your code should not run forever.
- A simple loop with a timeout is enough for this task.

## Conclusion
You now have the minimum real MQTT round-trip: connect, authenticate, subscribe, receive, publish, disconnect.
