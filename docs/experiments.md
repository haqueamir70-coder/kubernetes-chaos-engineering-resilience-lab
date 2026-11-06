# Chaos experiments and reliability scorecard

## Purpose

The experiments are designed to test recovery behaviour in a disposable Kubernetes lab. They are not production-ready fault-injection procedures.

## Experiment catalogue

| Scenario | Failure injected | Signals to inspect | Expected behaviour |
|---|---|---|---|
| Pod termination | Terminate one selected replica | Ready replicas, request success, recovery time | Replacement pod becomes Ready and traffic continues |
| CPU stress | Create CPU contention on a selected workload | CPU usage, p95 latency, 5xx ratio | Resource controls and application behaviour limit impact |
| Network fault | Add latency or packet loss to selected traffic | Request duration, timeouts, errors | Timeouts and retries bound the impact |

Use the corresponding templates in `chaos/experiments/`. Read the manifest before applying it; do not assume a template's selector or duration is safe for another cluster.

## Mandatory pre-flight gate

- [ ] Confirm the current Kubernetes context and cluster identity.
- [ ] Confirm the target namespace is the dedicated lab namespace.
- [ ] Confirm the target selector matches only the intended sample workload.
- [ ] Confirm replicas are healthy and capture a baseline.
- [ ] Confirm the experiment duration and fault parameters are bounded.
- [ ] Confirm the abort command and recovery owner are known.
- [ ] Confirm no production or shared workload can match the selector.

## Execution method

1. Capture a healthy baseline.
2. Run exactly one experiment at a time.
3. Observe workload status and telemetry while the fault is active.
4. Abort immediately if the target scope is wrong, the service becomes unrecoverable, or the agreed safety boundary is crossed.
5. Wait for recovery and verify pod readiness and API health.
6. Record timestamps, impact, recovery time, SLO evaluation and remediation.

## Example scorecard

| Field | Record |
|---|---|
| Experiment ID | Unique run identifier |
| Cluster / namespace | Lab cluster and target namespace |
| Start / end time | Timestamp with timezone |
| Baseline | Ready replicas, request rate, error ratio, p95 |
| Fault parameters | Exact manifest and parameters used |
| Impact | Observed availability, latency and errors |
| Recovery time | Fault start to verified healthy service |
| SLO outcome | Pass / fail / inconclusive, with evidence |
| Follow-up | Remediation owner and action |

## Illustrative objectives

The repository's example objectives are targets for learning, not measured performance claims:

- Availability: 99.9%
- Request latency: p95 at or below 300 ms
- Error rate: at or below 0.1%
- Recovery time: at or below 60 seconds

Do not report an objective as passed until a real run has produced reproducible evidence.
