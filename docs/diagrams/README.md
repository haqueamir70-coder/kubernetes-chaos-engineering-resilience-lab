# Diagram source and usage

This folder contains three hand-authored architecture diagrams with both rendered SVG previews and editable diagrams.net source files.

| Diagram | SVG preview | Editable source | Purpose |
|---|---|---|---|
| Platform architecture | [SVG](01-platform-architecture.svg) | [Draw.io](01-platform-architecture.drawio) | Delivery, AKS, workload, chaos, telemetry and guardrails |
| Chaos experiment lifecycle | [SVG](02-chaos-experiment-lifecycle.svg) | [Draw.io](02-chaos-experiment-lifecycle.drawio) | Pre-flight, bounded injection, observation and recovery |
| Observability and SLO flow | [SVG](03-observability-and-slo-flow.svg) | [Draw.io](03-observability-and-slo-flow.drawio) | Request metrics through Prometheus, Grafana and scorecard |

## Editing

1. Download the `.drawio` source file from GitHub.
2. Open [diagrams.net](https://app.diagrams.net/).
3. Choose **File → Import From → Device** and select the downloaded file.
4. Edit labels, connectors or layout, then export SVG to replace the matching preview.

## Visual conventions

- Rounded cards represent services, platforms or operational stages.
- Small colored markers are deliberately simple diagram glyphs, not vendor logos.
- Product names are written explicitly beside their components to avoid misleading or incorrect brand marks.
- Solid arrows show the main flow; the written architecture explains control and trust boundaries.

The diagrams are original project documentation, not screenshots of another architecture. Review them whenever implementation changes so that they remain aligned with the code.
