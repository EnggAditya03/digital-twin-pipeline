# Digital Twin Observability Pipeline

A real-time Digital Twin pipeline using Eclipse Ditto, InfluxDB, and Grafana — fully containerized with Docker Compose.

## Stack
- **Eclipse Ditto** — Digital Twin platform (REST API + SSE)
- **InfluxDB 2.7** — Time-series database
- **Grafana 10.4** — Live dashboards
- **Docker Compose** — Container orchestration

## Architecture
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.env
.env
