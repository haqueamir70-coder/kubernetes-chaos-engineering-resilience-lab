"""Static validation for provisioned Grafana and Prometheus assets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
dashboard = json.loads((ROOT / "monitoring/grafana/dashboards/resilience-overview.json").read_text(encoding="utf-8"))
assert dashboard.get("uid") == "resilience-lab-overview"
assert len(dashboard.get("panels", [])) >= 6
assert all(panel.get("targets") for panel in dashboard["panels"])
assert any("http_requests_total" in target.get("expr", "") for panel in dashboard["panels"] for target in panel["targets"])
assert any("http_request_duration_seconds_bucket" in target.get("expr", "") for panel in dashboard["panels"] for target in panel["targets"])

manifests = sorted((ROOT / "chaos/experiments").glob("*.yaml"))
assert manifests, "No chaos experiment manifests found"
for manifest in manifests:
    content = manifest.read_text(encoding="utf-8")
    assert "namespace: resilience-lab" in content, f"{manifest.name}: wrong namespace"
    assert 'duration: "30s"' in content, f"{manifest.name}: expected bounded duration"
    assert "app.kubernetes.io/name: resilience-api" in content, f"{manifest.name}: target selector missing"
    assert "namespaces:" in content, f"{manifest.name}: namespace selector missing"

print(f"Validated {len(dashboard['panels'])} Grafana panels and {len(manifests)} scoped chaos manifests.")
