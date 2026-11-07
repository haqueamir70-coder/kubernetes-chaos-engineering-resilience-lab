# Runbook: Pod Disruption

## Hypothesis

If one selected application pod is terminated, the Deployment controller should create a replacement and the Service should continue routing to ready replicas within the defined recovery objective.

## Pre-conditions

- Use the [pre-flight and abort checklist](preflight-and-abort.md).
- Confirm at least two healthy replicas.
- Confirm the PodDisruptionBudget and readiness probe behavior.
- Confirm the Chaos Mesh operator and permissions are installed in the disposable lab.

## Execute

Inspect the target first:

```bash
kubectl -n resilience-lab get pods -l app=resilience-api -o wide
kubectl -n resilience-lab get pdb
```

Review [chaos/experiments/pod-kill.yaml](../../../../chaos/experiments/pod-kill.yaml), replace/confirm the selector and duration, then apply only after approval:

```bash
kubectl apply -f chaos/experiments/pod-kill.yaml
kubectl -n resilience-lab get podchaos
kubectl -n resilience-lab get pods -w
```

## Verify

- Replacement pod becomes Ready.
- Service endpoints contain only ready pods.
- Request success/error ratio and p95 latency remain within the experiment limits.
- Record time from fault injection to stable service recovery.

## Cleanup

```bash
kubectl -n resilience-lab delete -f chaos/experiments/pod-kill.yaml
kubectl -n resilience-lab rollout status deployment/resilience-api --timeout=120s
```

If the manifest namespace or selector differs from the actual lab, correct it before applying. Never assume the sample file is safe without inspection.
