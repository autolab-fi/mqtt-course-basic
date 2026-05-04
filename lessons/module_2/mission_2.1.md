# Lesson 3: LED Command Listener

## Lesson objective
React to MQTT commands and produce a visible physical effect.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Introduction
This is the first lesson where your ESP32 becomes remotely controllable. The broker delivers a JSON command, and your device must translate it into hardware behavior.

For the first version, the hardware output should be simple and robust:

- built-in LED, or
- external LED on a GPIO pin

## Assignment
Write a program that:

- subscribes to a command topic for LED control
- accepts JSON messages such as `{"state":"on"}` and `{"state":"off"}`
- turns the LED on or off
- publishes the resulting LED state back to a state topic

Recommended topics:

- command: `lnu/iot/<student_id>/command/led`
- state: `lnu/iot/<student_id>/state/led`

Recommended state payload:

```json
{
  "device": "esp32",
  "actuator": "led",
  "state": "on"
}
```

## Conclusion
You now have a realistic control loop: the backend or another client can send a command, and your device can confirm what actually happened.
