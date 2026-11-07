# Runbook: Bounded CPU Stress

## Hypothesis

A bounded CPU stress experiment should expose how resource requests/limits, scheduling and application latency behave under contention, without affecting workloads outside the dedicated test namespace.

## Pre-conditions

- Use the [pre-flight and abort checklist](preflight-and-abort.md).
- Confirm resource requests and limits on the selected pod.
- Confirm node headroom and monitoring visibility.
- Set a short duration and narrow pod selector.
- Define an explicit p95 latency and error-ratio abort threshold.

## Execute

Review [chaos/experiments/cpu-stress.yaml](../../../../chaos/experiments/cpu-stress.yaml). Verify the target namespace, selector, CPU workers, load and duration. Apply only in the disposable lab:

```bash
kubectl apply -f chaos/experiments/cpu-stress.yaml
kubectl -n resilience-lab get stresschaos
kubectl -n resilience-lab top pods
```

## Verify

Capture CPU usage/throttling, pod readiness, request rate, p95 latency and error ratio before, during and after the fault.

## Cleanup and recovery

```bash
kubectl -n resilience-lab delete -f chaos/experiments/cpu-stress.yaml
kubectl -n resilience-lab rollout status deployment/resilience-api --timeout=120s
```

Stop immediately if the workload or node health crosses the agreed abort threshold. Do not increase stress duration or intensity to force a failure.
