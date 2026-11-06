# Architecture diagram library

This folder contains original architecture diagrams maintained as editable diagrams.net source plus SVG previews.

| Diagram | Preview | Editable source | What it explains |
|---|---|---|---|
| Platform architecture | [SVG](01-platform-architecture.svg) | [Draw.io](01-platform-architecture.drawio) | CI/CD, Terraform, Azure Kubernetes Service, Kubernetes workload and observability |
| Chaos experiment lifecycle | [SVG](02-chaos-experiment-lifecycle.svg) | [Draw.io](02-chaos-experiment-lifecycle.drawio) | Baseline, safety review, bounded fault injection, monitoring and recovery |
| Observability and SLO flow | [SVG](03-observability-and-slo-flow.svg) | [Draw.io](03-observability-and-slo-flow.drawio) | Workload telemetry, Prometheus, Grafana and reliability evidence |

## Brand icon treatment

- Azure Kubernetes Service uses an icon from the Azure Architecture Icons collection.
- Kubernetes, Terraform, Prometheus, Grafana and GitHub Actions use their traceable Simple Icons SVG assets.
- Every brand mark is accompanied by its product name; the marks are not used as decoration or as substitutes for architecture boundaries.
- Sources and usage notes: [assets/icons/README.md](../../assets/icons/README.md).

## Edit the diagrams

1. Open [diagrams.net](https://app.diagrams.net/).
2. Choose **File → Import From → Device**.
3. Select the downloaded `.drawio` file.
4. Keep the product labels close to their logos and do not distort brand marks.
5. Export an SVG and replace the matching preview after editing.

The diagrams are intentionally hand-maintained to make the engineering decisions and system boundaries easy to explain in a technical interview. Update them whenever the implementation changes.
