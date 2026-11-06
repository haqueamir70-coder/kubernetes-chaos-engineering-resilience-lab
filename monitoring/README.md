# Observability stack

This folder contains version-controlled Prometheus scrape configuration, alert rules, Grafana data-source provisioning and a prebuilt service-health dashboard.

## Included

- Prometheus scrapes the `resilience-api` pods in the `resilience-lab` namespace through Kubernetes service discovery.
- Grafana provisions the Prometheus data source and the Resilience Lab dashboard from files.
- Alert rules cover 5xx ratio, p95 latency and scrape availability.
- The dashboard shows request throughput, error ratio, latency percentiles, target health and optional container resource telemetry.

## Install assumptions

The example configuration assumes:

- Prometheus runs in namespace `monitoring` and has Kubernetes API read permissions to discover pods in `resilience-lab`.
- Grafana can reach the Prometheus Service at `prometheus.monitoring.svc.cluster.local:9090`.
- The FastAPI deployment exposes a named `http` container port and `/metrics` endpoint.
- Container resource panels require kubelet/cAdvisor metrics; CPU and memory panels remain empty if those metrics are not collected.

Mount `prometheus/prometheus.yml` and `prometheus/alerts.yml` into the Prometheus configuration and rule paths. Mount `grafana/provisioning/` and `grafana/dashboards/` into the corresponding Grafana paths. Adapt paths and service names to the Helm chart or manifests used in your lab.

## Open the dashboard

After provisioning, open Grafana → Dashboards → Resilience Engineering → **Resilience Lab | Service Health & Recovery**.

The dashboard is provisioned as code. Make durable edits in the JSON source and commit them; do not rely on UI-only changes.

## Interpretation

The SLO values are illustrative learning targets, not measured production SLOs. A dashboard panel showing no data means its metric is not currently being scraped or there has been no traffic in the selected time window. Generate test traffic and verify Prometheus targets before interpreting the panels.

## References

- [Grafana file provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)
- [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/)
