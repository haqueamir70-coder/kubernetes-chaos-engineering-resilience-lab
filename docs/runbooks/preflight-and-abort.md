# Pre-flight and Abort Criteria

## Scope

Disposable Kubernetes lab only. Do not execute against production, shared, customer, regulated or OT/industrial workloads.

## Before injection

- [ ] Confirm current Kubernetes context and cluster identity.
- [ ] Confirm the dedicated lab namespace.
- [ ] Confirm the target Deployment, labels and replica count.
- [ ] Confirm only the intended test workload matches the selector.
- [ ] Confirm application health and baseline request metrics.
- [ ] Confirm an operator can stop/delete the experiment.
- [ ] Confirm the recovery procedure and time limit.
- [ ] Confirm no unrelated workload shares the target namespace/node pool.

Example checks:

```bash
kubectl config current-context
kubectl get namespace resilience-lab
kubectl -n resilience-lab get deploy,pods,svc
kubectl -n resilience-lab get events --sort-by=.lastTimestamp
```

## Abort immediately when

- The target selector matches an unexpected pod.
- The cluster/context/namespace is not the dedicated lab.
- Availability or error rate breaches the experiment's pre-agreed abort threshold.
- The workload does not recover within the approved time limit.
- Cluster node health, DNS, ingress or unrelated workloads degrade.
- The operator loses the ability to observe or stop the experiment.

## Stop and recover

Use the exact experiment resource name and namespace:

```bash
kubectl -n resilience-lab get podchaos,stresschaos,networkchaos
kubectl -n resilience-lab delete podchaos <experiment-name>
kubectl -n resilience-lab delete stresschaos <experiment-name>
kubectl -n resilience-lab delete networkchaos <experiment-name>
kubectl -n resilience-lab rollout status deployment/resilience-api --timeout=120s
kubectl -n resilience-lab get pods
```

Only delete the resource type that was created. Do not run placeholder commands literally. Confirm the fault is gone and the service has recovered before ending the experiment.

## Evidence

Record baseline, fault window, impact, recovery time, abort decision (if any), and follow-up actions in [chaos evidence](../chaos-evidence.md).
