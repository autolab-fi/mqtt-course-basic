# Lesson 7: LED State Protocol

## Lesson objective
Implement a tiny IoT command protocol for one LED.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
A real device usually supports more than one command. In this final beginner
task, your ESP32 supports three LED actions:

- `on`
- `off`
- `toggle`

After the command, the device reports the final state.

## Lab architecture
This lesson uses the full course architecture: command input, hardware action,
event output, and state output. The worker sends a command to the real ESP32. The
board updates the LED, publishes an event that describes the change, and publishes
a state message that describes the final known state.

## MQTT protocol concepts
A protocol is an agreement about message shapes and meanings. Here the command
protocol uses `target` and `action`, the event protocol uses `name`, `event`, and
`state`, and the state protocol uses `target` and `state`.

Events and state are different. An event says that something happened, for
example "the LED changed". State says what is true now, for example "the LED is
on". Real IoT systems often publish both because applications need both history
and the latest known state.

## Assignment
Write a program that:

- subscribes to `ATTEMPT_TOPIC_ROOT + "/command"`
- publishes `protocol_ready` telemetry
- accepts JSON commands with `action`
- supports `on`, `off`, and `toggle`
- publishes the final LED state to `ATTEMPT_TOPIC_ROOT + "/state"`
- publishes a LED event to `ATTEMPT_TOPIC_ROOT + "/event"`

Example checker command:

```json
{
  "target": "led",
  "action": "toggle"
}
```

Required final state:

```json
{
  "target": "led",
  "state": true
}
```

Required event:

```json
{
  "name": "led",
  "event": "changed",
  "state": true
}
```

## Conclusion
You have built a small MQTT device protocol with command input and state output.
