# Getting started

This guide deploys the sample API to a disposable local Kubernetes cluster. It does not require Azure.

## Prerequisites

- Docker Engine or Docker Desktop with the Linux container backend
- kind
- kubectl
- Python 3.12+ only if you want to run the application tests outside the container

Check the tools before starting:

```bash
docker version
kind version
kubectl version --client
```

## 1. Create the local cluster

```bash
kind create cluster --name resilience-lab
kubectl cluster-info --context kind-resilience-lab
```

## 2. Build and load the API image

Run these commands from the repository root:

```bash
docker build -t resilience-api:local .
kind load docker-image resilience-api:local --name resilience-lab
```

## 3. Deploy the workload

```bash
kubectl apply -k platform/kubernetes/overlays/local
kubectl -n resilience-lab rollout status deployment/resilience-api
kubectl -n resilience-lab get pods,svc
```

## 4. Verify the endpoints

In one terminal:

```bash
kubectl -n resilience-lab port-forward svc/resilience-api 8080:80
```

In another terminal:

```bash
curl -fsS http://127.0.0.1:8080/health
curl -fsS http://127.0.0.1:8080/metrics
```

## 5. Continue to observability and chaos testing

Use the manifests and configuration in `monitoring/` and `chaos/experiments/`. Install monitoring and Chaos Mesh only into this disposable lab, following the upstream installation instructions for the versions you select. Review every manifest and the safety gates in [Experiments](experiments.md) before applying it.

## AKS path

The repository also contains an AKS Terraform starter under `infra/terraform/`. Review its variables, provider configuration and outputs before use. Run Terraform formatting, validation and a plan first. Confirm the Azure subscription, region, permissions, quotas and estimated cost. Do not apply to a shared or production subscription.

## Cleanup

Delete the local cluster when finished:

```bash
kind delete cluster --name resilience-lab
```

For Azure resources, use the Terraform state and outputs for the exact environment you provisioned. Review the destroy plan carefully before approving it.
