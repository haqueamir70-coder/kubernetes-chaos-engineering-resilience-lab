# Chaos experiment evidence report

## Current evidence status

**Status: NOT RUN IN THIS repository update.**

The repository now contains bounded Chaos Mesh experiment templates, a provisioned Grafana dashboard, Prometheus scrape configuration and static CI validation. No live Kubernetes cluster was available here to execute experiments or collect real telemetry.

Do not represent example SLO targets or dashboard panels as measured results.

## Evidence capture checklist

- [ ] Cluster name and Kubernetes context (redact account identifiers).
- [ ] Git commit SHA and exact experiment manifest.
- [ ] Target namespace, selector and pod identity.
- [ ] Baseline period and baseline metrics.
- [ ] Fault start and end timestamps with timezone.
- [ ] Prometheus query exports or Grafana screenshots.
- [ ] Pod replacement / readiness evidence.
- [ ] Recovery time and SLO evaluation.
- [ ] Operator notes, aborts and remediation.

## Suggested run sequence

1. Deploy the local lab and confirm all three replicas are Ready.
2. Verify the Prometheus target is UP and Grafana panels return data.
3. Generate steady test traffic for a baseline window.
4. Execute only one bounded experiment from `chaos/experiments/`.
5. Capture metrics during the fault and after recovery.
6. Repeat only after the cluster returns to a healthy baseline.

## Report template

| Measurement | Baseline | During fault | After recovery |
|---|---:|---:|---:|
| Ready replicas | Record actual | Record actual | Record actual |
| Request rate | Record actual | Record actual | Record actual |
| 5xx error ratio | Record actual | Record actual | Record actual |
| p95 latency | Record actual | Record actual | Record actual |
| Recovery time | — | Record start/end | Record actual |

Until a run is performed, label the dashboard as a provisioned dashboard definition and the manifests as experiment templates. After a real run, replace this status with timestamped evidence. Never fabricate benchmark values or claim a chaos experiment passed without recorded measurements.
