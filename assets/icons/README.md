# Brand icon assets and attribution

These SVGs are used only to identify technologies in the project's architecture diagrams.

## Simple Icons assets

The following marks are vendored from the Simple Icons project. Each source revision is recorded so the artwork can be traced to the exact upstream blob.

| Asset | Source | Upstream blob |
|---|---|---|
| Kubernetes | [simple-icons/icons/kubernetes.svg](https://github.com/simple-icons/simple-icons/blob/667f2d4725da2500e450a93bbb1d5f9d73dddaa4/icons/kubernetes.svg) | `667f2d4725da2500e450a93bbb1d5f9d73dddaa4` |
| Terraform | [simple-icons/icons/terraform.svg](https://github.com/simple-icons/simple-icons/blob/7aafae1318a063f94e4b472523f90b660aac3291/icons/terraform.svg) | `7aafae1318a063f94e4b472523f90b660aac3291` |
| Prometheus | [simple-icons/icons/prometheus.svg](https://github.com/simple-icons/simple-icons/blob/32a30255d6992471235663bd187cfc692de1b158/icons/prometheus.svg) | `32a30255d6992471235663bd187cfc692de1b158` |
| Grafana | [simple-icons/icons/grafana.svg](https://github.com/simple-icons/simple-icons/blob/a495a662508df1a41d39a6dcf7ed5b84b9deff39/icons/grafana.svg) | `a495a662508df1a41d39a6dcf7ed5b84b9deff39` |
| GitHub Actions | [simple-icons/icons/githubactions.svg](https://github.com/simple-icons/simple-icons/blob/bc925a351eb6fa2bb0f73a1192c8656db13eb2d3/icons/githubactions.svg) | `bc925a351eb6fa2bb0f73a1192c8656db13eb2d3` |

Upstream project: [simple-icons/simple-icons](https://github.com/simple-icons/simple-icons). Review its [usage guidance and legal disclaimer](https://github.com/simple-icons/simple-icons#usage) before reusing these marks elsewhere.

## Azure Kubernetes Service icon

The AKS service icon used in the diagrams is sourced from the July 2026 Azure Architecture Icons collection:

- [Azure Kubernetes Services SVG](https://az-icons.com/images/kubernetes-services/icon.svg)
- [Icon catalogue entry](https://az-icons.com/icon/kubernetes-services)
- [Microsoft Azure Architecture Center icon guidance](https://learn.microsoft.com/en-us/azure/architecture/icons/)

Microsoft permits its architecture icons in architecture diagrams, training materials and documentation. Keep the product name near the icon. Do not crop, flip, rotate or distort the icon. Microsoft product names and marks remain the property of Microsoft.

## How diagrams load icons

The editable diagrams.net files reference the committed Simple Icons assets through this repository's raw GitHub URLs. The Azure Kubernetes Service icon is referenced from the Azure icon catalogue. Open the diagrams with an internet connection so the image shapes can resolve.

The SVG previews inline the Simple Icons paths and use the Azure service icon as an image reference. If you fork or rename the repository, update the raw GitHub URLs in the `.drawio` source files.
