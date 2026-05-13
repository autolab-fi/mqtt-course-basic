# Lesson 7: Subscribe and Poll Commands

## Lesson objective
Subscribe to an MQTT command topic and poll for incoming messages.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
IoT devices often listen for commands from another program. In MicroPython with
`umqtt.simple`, a common beginner pattern is:

- subscribe to a topic
- set a callback
- call `check_msg()` inside a short loop

## Lab architecture
In command lessons, your ESP32 and the checker both use the same attempt topic
root. Your program subscribes to `.../command`, then publishes ready telemetry.
The ready message tells the worker that the board is connected and listening.
Only after that does the worker publish the checker command.

## MQTT concepts
`subscribe(topic)` registers interest in messages from a topic. `set_callback(...)`
registers the function that should run when a message arrives. With
`umqtt.simple`, incoming messages are not processed automatically while your code
is busy. `check_msg()` gives the MQTT client a chance to read one waiting message
and call your callback.

The loop must be bounded because this is a lab attempt, not permanent firmware.
A limited loop gives MQTT time to deliver the command while still allowing the
worker to finish the run predictably.

## Assignment
Write a program that:

- connects to MQTT
- subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- publishes ready telemetry to `ATTEMPT_TOPIC_ROOT + "/telemetry"`
- polls messages with `check_msg()` for a limited time
- disconnects cleanly

Required ready telemetry:

```json
{
  "name": "command_ready",
  "value": 1
}
```

## Notes
- Use a limited loop such as `for _ in range(30)`.
- Do not use an endless `while True` loop in this course task.

## Conclusion
You can now subscribe to a command topic and give MQTT time to deliver messages.
