# Logging for Django


---
## The Flow of Logs

Logs in this project follow the pipeline below:

1. **Django Application**
    - Logs are generated within the Django application.
2. **Kafka**
    - Logs are pushed into a Kafka topic for stream processing.
3. **Logstash**
    - Parses, transforms, and prepares logs for storage.
4. **Elasticsearch**
    - Logs are indexed and stored for searching and analysis.
5. **Grafana**
    - Visualizes logs and provides monitoring dashboards.

This pipeline ensures that logs are efficiently managed, stored, and visualized for debugging and performance monitoring.

