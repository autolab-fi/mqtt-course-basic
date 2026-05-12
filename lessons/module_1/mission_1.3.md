# Lesson 3: Connect, Publish, Disconnect

## Lesson objective
Practice the complete short MQTT lifecycle.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
Short MQTT programs should open the connection, do their work, and close the
connection. This makes tests predictable and keeps the board ready for the next
attempt.

## Assignment
Write a program that:

- creates an MQTT client with `make_mqtt_client()`
- calls `connect()`
- publishes one online telemetry message
- calls `disconnect()`

Required telemetry topic:

- `ATTEMPT_TOPIC_ROOT + "/telemetry"`

Required payload:

```json
{
  "name": "status",
  "value": "online"
}
```

## Notes
- Use `json.dumps(...)` to create the payload.
- Encode strings before publishing if your client requires bytes.
- This task should finish quickly.

## Conclusion
You can now write a complete small MQTT program from start to finish.
