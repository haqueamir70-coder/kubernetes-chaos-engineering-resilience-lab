# Controlled chaos experiment templates

These manifests are narrow examples for the disposable `resilience-lab` namespace only. They select one pod labelled `app.kubernetes.io/name=resilience-api` and use a bounded 30-second duration.

## Mandatory pre-flight gate

1. Confirm this is a disposable cluster dedicated to this lab.
2. Confirm your current context: `kubectl config current-context`.
3. Confirm the namespace and target pods: `kubectl -n resilience-lab get pods -l app.kubernetes.io/name=resilience-api`.
4. Capture baseline request rate, 5xx ratio, p95 latency and ready replica count.
5. Review the YAML and verify the Chaos Mesh CRDs and controller version installed in this cluster.
6. Have an operator ready to stop the experiment and restore the service.

**Never run these templates against production, shared, or customer clusters.**

## Run one experiment at a time

Pod termination:

```bash
kubectl apply --dry-run=server -f chaos/experiments/pod-kill.yaml
kubectl apply -f chaos/experiments/pod-kill.yaml
kubectl -n resilience-lab describe podchaos resilience-api-pod-kill
```

CPU stress:

```bash
kubectl apply --dry-run=server -f chaos/experiments/cpu-stress.yaml
kubectl apply -f chaos/experiments/cpu-stress.yaml
kubectl -n resilience-lab describe stresschaos resilience-api-cpu-stress
```

Network delay:

```bash
kubectl apply --dry-run=server -f chaos/experiments/network-delay.yaml
kubectl apply -f chaos/experiments/network-delay.yaml
kubectl -n resilience-lab describe networkchaos resilience-api-network-delay
```

## Abort and verify recovery

Delete the specific experiment resource if the target scope is unexpected or the agreed safety threshold is crossed:

```bash
kubectl -n resilience-lab delete podchaos resilience-api-pod-kill --ignore-not-found
kubectl -n resilience-lab delete stresschaos resilience-api-cpu-stress --ignore-not-found
kubectl -n resilience-lab delete networkchaos resilience-api-network-delay --ignore-not-found
kubectl -n resilience-lab rollout status deployment/resilience-api
```

Record the context, manifest revision, target pod, timestamps, baseline and fault-period telemetry, recovery time, SLO outcome and follow-up actions. A manifest in Git is not evidence that an experiment executed successfully.

Chaos Mesh CRD fields vary by release. Validate manifests server-side against the installed CRDs before applying. See the [experiment guide](https://chaos-mesh.org/docs/run-a-chaos-experiment/) and [scope guidance](https://chaos-mesh.org/docs/define-chaos-experiment-scope/).
