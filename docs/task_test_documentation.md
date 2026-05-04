# Verification Notes

This course is expected to use a mixed verification model:

- MQTT payload validation
- timing and periodicity checks
- command-response checks
- optional camera confirmation for LEDs, servo position, or visible state changes

Each lesson that becomes auto-checked should eventually define:

- expected topics
- expected JSON schemas
- timing tolerances
- success and failure conditions
- whether camera evidence is required
