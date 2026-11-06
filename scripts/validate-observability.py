"""Static validation for provisioned dashboards and scoped chaos manifests."""
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
dashboard = json.loads((ROOT / "monitoring/grafana/dashboards/resilience-overview.json").read_text(encoding="utf-8"))
assert dashboard.get("uid") == "resilience-lab-overview"
assert len(dashboard.get("panels", [])) == 8
assert all(panel.get("targets") for panel in dashboard["panels"])
assert any("http_requests_total" in target.get("expr", "") for panel in dashboard["panels"] for target in panel["targets"])
assert any("http_request_duration_seconds_bucket" in target.get("expr", "") for panel in dashboard["panels"] for target in panel["targets"])

yaml_files = list((ROOT / "monitoring").rglob("*.yml")) + list((ROOT / "monitoring").rglob("*.yaml"))
yaml_files += list((ROOT / "chaos").rglob("*.yaml"))
for path in yaml_files:
    list(yaml.safe_load_all(path.read_text(encoding="utf-8")))

manifests = sorted((ROOT / "chaos/experiments").glob("*.yaml"))
assert len(manifests) == 3, "Expected pod-kill, CPU-stress and network-delay examples"
for manifest in manifests:
    content = manifest.read_text(encoding="utf-8")
    assert "namespace: resilience-lab" in content, f"{manifest.name}: wrong namespace"
    assert 'duration: "30s"' in content, f"{manifest.name}: expected bounded duration"
    assert "app.kubernetes.io/name: resilience-api" in content, f"{manifest.name}: target selector missing"
    assert "namespaces:" in content, f"{manifest.name}: namespace selector missing"
    assert "mode: one" in content, f"{manifest.name}: target mode must be one"

print(f"Validated {len(dashboard['panels'])} Grafana panels, {len(yaml_files)} YAML files and {len(manifests)} scoped chaos manifests.")
