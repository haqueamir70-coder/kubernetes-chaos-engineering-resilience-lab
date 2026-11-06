# Install the observability stack (local lab)

This guide uses the Prometheus Community `kube-prometheus-stack` Helm chart to install Prometheus, Grafana, Alertmanager and Kubernetes monitoring components in the dedicated local cluster.

## 1. Add the chart repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
```

## 2. Install the stack

```bash
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --values monitoring/kube-prometheus-stack-values.yaml
```

The values file adds a Kubernetes pod-discovery scrape job for the FastAPI service, provisions three example alerts, and enables Grafana's dashboard sidecar.

## 3. Publish the version-controlled dashboard

```bash
kubectl -n monitoring create configmap resilience-lab-dashboard \
  --from-file=resilience-overview.json=monitoring/grafana/dashboards/resilience-overview.json \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl -n monitoring label configmap resilience-lab-dashboard \
  grafana_dashboard=1 --overwrite
```

The Grafana sidecar watches ConfigMaps carrying that label. The dashboard JSON remains the source of truth in Git; edit the file and re-apply the ConfigMap to publish changes.

## 4. Confirm Prometheus sees the API

Deploy the sample API first, then check:

```bash
kubectl -n resilience-lab get pods -l app.kubernetes.io/name=resilience-api
kubectl -n monitoring port-forward svc/prometheus-kube-prometheus-prometheus 9090:9090
```

Open `http://127.0.0.1:9090/targets` and confirm the `resilience-api` target is UP.

## 5. Open Grafana

In another terminal:

```bash
kubectl -n monitoring port-forward svc/prometheus-grafana 3000:80
```

Open `http://127.0.0.1:3000`. The chart's default admin password is generated in a Kubernetes Secret; retrieve it locally with:

```bash
kubectl get secret -n monitoring prometheus-grafana \
  -o jsonpath="{.data.admin-password}" | base64 -d; echo
```

The dashboard appears under **Dashboards → Resilience Engineering** after the sidecar syncs the ConfigMap.

## 6. Generate test traffic

In another terminal, port-forward the API:

```bash
kubectl -n resilience-lab port-forward svc/resilience-api 8080:80
```

Then generate a small amount of traffic:

```bash
for i in $(seq 1 120); do curl -fsS http://127.0.0.1:8080/work >/dev/null; sleep 0.25; done
```

Allow at least a few scrape intervals for metrics to appear. A dashboard with no data before traffic or before Prometheus discovers the pods is expected.

## 7. Run a controlled experiment

Only after the baseline is healthy, follow [chaos experiment instructions](../chaos/README.md). Capture screenshots and query results, then complete the [evidence report](../docs/chaos-evidence.md).

## 8. Cleanup

```bash
helm uninstall prometheus -n monitoring
kubectl delete namespace monitoring
```

This removes the monitoring stack from the disposable local cluster. Do not run cleanup commands against a shared or production cluster.
