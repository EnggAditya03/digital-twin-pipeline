#!/bin/bash
DITTO_URL='http://localhost:8080/api/2/things'
THING_ID='com.example:sensor-001'

echo 'Starting telemetry simulation (Ctrl+C to stop)...'

while true; do
  TEMP=$(awk 'BEGIN{srand(); printf "%.1f", 60 + rand() * 40}')
  HUM=$(awk  'BEGIN{srand(); printf "%.1f", 40 + rand() * 40}')

  curl -s -X PUT -u ditto:ditto \
    -H 'Content-Type: application/json' \
    -d "{\"value\": $TEMP}" \
    "$DITTO_URL/$THING_ID/features/temperature/properties" > /dev/null

  curl -s -X PUT -u ditto:ditto \
    -H 'Content-Type: application/json' \
    -d "{\"value\": $HUM}" \
    "$DITTO_URL/$THING_ID/features/humidity/properties" > /dev/null

  echo "[$(date +%T)] Temp: ${TEMP}C  |  Humidity: ${HUM}%"
  sleep 5
done
