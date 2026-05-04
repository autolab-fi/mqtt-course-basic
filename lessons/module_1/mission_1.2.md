# Lesson 2: First Sensor Publish

## Lesson objective
Publish JSON telemetry on a fixed schedule.

![Beginner](https://img.shields.io/badge/Difficulty-Beginner-green)

## Assignment
Write a program that:

- connects to the MQTT broker already configured for the lab
- reads one real sensor value, such as `light`, `temperature`, or `humidity`
- publishes one JSON message every 2 seconds
- includes at least one sensor reading
- uses a stable topic for telemetry
- keeps the payload format identical on every publish
- includes enough metadata for backend ingestion and historical dashboards

Recommended payload shape:

```json
{
  "sensor": "light",
  "value": 412,
  "unit": "raw",
  "device_state": "ok",
  "timestamp": 1712345678,
  "device_id": "esp32-lab-01"
}
```

## Conclusion
Once your telemetry appears on schedule, you have the minimum building block for the rest of the course.
