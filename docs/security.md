# Security and safety model

## Scope

This repository is an educational reference lab. It is not a hardened production chaos platform. Fault injection must remain inside a disposable cluster dedicated to this exercise.

## Workload security

- The sample API is designed to run without Kubernetes API permissions.
- Keep service-account token automount disabled unless a documented requirement exists.
- Run the container as a non-root user and retain the configured container hardening.
- Set resource requests and limits deliberately; tune them from measured workload behaviour.
- Keep health and readiness probes distinct and verify their behaviour under failure.

## Chaos control plane

Chaos Mesh controllers can require powerful Kubernetes permissions. Treat installation and experiment creation as privileged operations.

- Restrict controller access to trusted administrators.
- Do not grant broad permissions to the sample application.
- Use a dedicated namespace and narrow label selectors.
- Bound experiment duration and fault intensity.
- Require human review and a documented abort procedure before execution.

## Infrastructure and supply chain

- Review Terraform plans before applying Azure resources.
- Use least-privilege Azure identities and protect state files and credentials.
- Never commit secrets, kubeconfigs, access tokens or state files.
- Pin and review action, provider, container and chart versions before production use.
- Treat CI validation as a guardrail, not proof that a deployment is secure.

## Network policy considerations

NetworkPolicy enforcement depends on the cluster's network plugin. Validate DNS, application traffic and Prometheus scraping before enabling restrictive policies.

## Operational prohibition

**Never run the supplied chaos experiments against production or shared clusters.** Any future production use would require a separate threat model, formal change approval, explicit service-owner authorization, tested rollback, monitoring coverage and a narrowly scoped blast-radius design.
