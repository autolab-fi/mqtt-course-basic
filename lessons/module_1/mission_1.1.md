# Lesson 1: Connect, Subscribe, Publish, Disconnect

## Lesson objective
Learn the minimum MQTT lifecycle on ESP32 with MicroPython.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
In this course you will use `MicroPython` on an `ESP32` to communicate through MQTT. Before building real labs, you need to understand the basic lifecycle:

- connect to the broker
- subscribe to one or more topics
- publish messages
- receive messages
- disconnect cleanly when the program finishes

For small lab tasks, a simple client from `umqtt.simple` is usually enough.

## Theory

### Basic MQTT roles
- A **publisher** sends messages to a topic.
- A **subscriber** listens to a topic.
- The **broker** routes messages between publishers and subscribers.

In this course you will often do both on the same ESP32:

- publish telemetry to a sensor topic
- subscribe to a command topic

### Example with `umqtt.simple`

```python
from umqtt.simple import MQTTClient

BROKER = "broker.emqx.io"
CLIENT_ID = b"esp32-demo"
TOPIC_PUB = b"lnu/iot/demo/status"
TOPIC_SUB = b"lnu/iot/demo/command"

def on_message(topic, msg):
    print("Received:", topic, msg)

client = MQTTClient(client_id=CLIENT_ID, server=BROKER)
client.set_callback(on_message)
client.connect()
client.subscribe(TOPIC_SUB)
client.publish(TOPIC_PUB, b'{"status":"online"}')

# Poll for incoming messages in a loop
for _ in range(20):
    client.check_msg()

client.disconnect()
```

### Notes for students
- `connect()` opens the session with the broker.
- `subscribe()` tells the broker which topic you want to receive.
- `publish()` sends a message to a topic.
- `check_msg()` polls for new incoming messages.
- `disconnect()` closes the MQTT session cleanly.

## Assignment
Write a program that:

- connects to the MQTT broker
- subscribes to a test topic of your own
- publishes one JSON message to another topic
- waits for incoming messages for a short time
- disconnects cleanly before the program ends

Recommended topic format for testing:

- `lnu/iot/<student_id>/status`
- `lnu/iot/<student_id>/command/test`

## Conclusion
After this lesson, you should understand how to join a topic-based MQTT workflow from MicroPython and how to leave it cleanly.
