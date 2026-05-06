# Digital Twin Observability Pipeline

A real-time Digital Twin pipeline using Eclipse Ditto, InfluxDB, and Grafana — fully containerized with Docker Compose.

## Stack
- **Eclipse Ditto** — Digital Twin platform (REST API + SSE)
- **InfluxDB 2.7** — Time-series database
- **Grafana 10.4** — Live dashboards
- **Docker Compose** — Container orchestration

## Architecture

Simulator --> REST API --> Eclipse Ditto --> SSE --> Python Bridge --> InfluxDB --> Grafana

## Setup & Usage

### 1. Prerequisites
- Docker Desktop installed and running

### 2. Create shared network
```bash
docker network create ditto-net
```

### 3. Start Eclipse Ditto
```bash
git clone https://github.com/eclipse-ditto/ditto.git
cd ditto/deployment/docker
docker compose up -d
```

### 4. Start InfluxDB + Grafana
```bash
docker compose -f docker-compose.observability.yml up -d
```

### 5. Install Python dependencies
```bash
pip3 install requests influxdb-client sseclient-py
```

### 6. Run the bridge
```bash
python3 ditto_to_influx.py
```

### 7. Run the simulator
```bash
./simulate_telemetry.sh
```

### 8. Open Grafana
Visit http://localhost:3000 — login: admin / grafanapassword

## Credentials

| Service | URL | Login |
|---|---|---|
| Eclipse Ditto | http://localhost:8080 | ditto / ditto |
| InfluxDB | http://localhost:8086 | admin / adminpassword123 |
| Grafana | http://localhost:3000 | admin / grafanapassword |
