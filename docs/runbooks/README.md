# Resilience Lab Runbooks

These procedures are for a **disposable, isolated test cluster only**. They are not approved production change procedures. Never run fault injection against production, shared, customer or industrial control workloads.

## Runbook index

| Procedure | Purpose |
|---|---|
| [Pre-flight and abort](preflight-and-abort.md) | Verify scope, safety controls and stop conditions |
| [Pod disruption](pod-disruption.md) | Validate replica replacement and service continuity |
| [CPU stress](cpu-stress.md) | Observe bounded CPU contention and latency impact |
| [Network delay](network-delay.md) | Observe bounded latency injection and recovery |

## Mandatory evidence

For every experiment, capture:

1. Experiment ID, operator, timestamp and exact target selector.
2. Approved namespace and workload scope.
3. Baseline request rate, error ratio and p95 latency.
4. Fault start/end timestamps and manifest used.
5. Pod readiness, restart counts and service-level telemetry during the fault.
6. Abort/recovery actions and final outcome.
7. Follow-up actions with an owner.

A configured SLO target is not a measured pass. Record observed values from the actual run.

## Cleanup

After each experiment, delete the Chaos Mesh experiment object, confirm no fault remains active, and verify the workload returns to its baseline state. Follow the cleanup commands in the specific runbook.
