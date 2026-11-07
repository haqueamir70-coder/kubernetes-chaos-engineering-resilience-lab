# Runbook: Network Delay

## Hypothesis

A bounded network-delay experiment should reveal whether client timeouts, retries and graceful degradation behave as designed, and whether latency returns to baseline after the fault is removed.

## Pre-conditions

- Use the [pre-flight and abort checklist](preflight-and-abort.md).
- Confirm only the intended test pod/network path is selected.
- Confirm baseline p95 latency and error ratio.
- Define a maximum injected delay, duration and abort threshold.
- Confirm the operator can delete the NetworkChaos resource immediately.

## Execute

Review [chaos/experiments/network-delay.yaml](../../../../chaos/experiments/network-delay.yaml), especially namespace, pod selector, direction, delay and duration. Apply only after approval:

```bash
kubectl apply -f chaos/experiments/network-delay.yaml
kubectl -n resilience-lab get networkchaos
```

## Verify

Observe request p95/p99 latency, timeout/error rate, retry behavior, readiness and dependency health. Distinguish expected injected delay from unrelated cluster/network faults.

## Cleanup

```bash
kubectl -n resilience-lab delete -f chaos/experiments/network-delay.yaml
kubectl -n resilience-lab rollout status deployment/resilience-api --timeout=120s
```

Confirm latency returns to the recorded baseline range. If it does not, stop further experiments and investigate before proceeding.
