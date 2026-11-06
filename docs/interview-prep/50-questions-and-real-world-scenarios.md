# Kubernetes Chaos Engineering & Resilience Lab — 50 Interview Questions & Real-World Scenarios

> Study guide for DevSecOps, SRE, Kubernetes and Cloud Platform Engineer interviews. Answers are deliberately practical: explain the concept, connect it to this repository, and state how you would verify the outcome.
>
> **Important:** This repository is a learning lab. The SLOs are illustrative targets, not measured production results. Never run fault injection against production or shared clusters without formal authorization.

## How to use this guide

For each question:
1. Explain the concept in your own words.
2. Describe the relevant component in this repository.
3. Give the command, metric, log or test you would use as evidence.
4. State the trade-off or failure mode.

---

# Part 1 — Kubernetes fundamentals (Q1–Q10)

### Q1. What problem does Kubernetes solve?
**Answer:** Kubernetes automates deployment, scheduling, scaling and recovery of containerized workloads. It continuously reconciles actual cluster state toward the desired state declared in objects such as Deployments. It does not automatically make an application resilient; the application still needs health checks, resource controls, safe rollout settings and observability.

**In this project:** The Deployment declares three API replicas. The controller recreates pods when a pod is deleted.

### Q2. What is the difference between a Pod, Deployment and Service?
**Answer:** A Pod is the smallest schedulable workload unit. A Deployment manages ReplicaSets and maintains the desired number of interchangeable pods. A Service provides a stable virtual endpoint and selects matching pods using labels.

**Verify:**
```bash
kubectl -n resilience-lab get deploy,rs,pods,svc
kubectl -n resilience-lab get endpointslice
```

### Q3. How do readiness, liveness and startup probes differ?
**Answer:** Readiness controls whether a pod receives Service traffic. Liveness detects a process that should be restarted. Startup probes protect slow-starting applications by delaying liveness/readiness evaluation until startup succeeds. A bad liveness probe can create restart loops; readiness is usually the safer signal for temporary dependency problems.

**In this project:** `/ready` and `/health` are intentionally separate endpoints. In a real service, readiness should include only dependencies required to serve traffic.

### Q4. What happens when a pod is deleted?
**Answer:** If it is managed by a Deployment, the ReplicaSet notices the replica count is below the desired count and creates a replacement. The scheduler assigns it to a node, kubelet starts its containers, and readiness determines when it receives Service traffic. Recovery time depends on scheduling, image availability, startup and probe configuration.

**Try:** `kubectl -n resilience-lab delete pod <pod-name>` and watch `kubectl get pods -w`.

### Q5. What are requests and limits?
**Answer:** Requests are used by the scheduler for placement and influence QoS. CPU limits throttle CPU usage; memory limits can cause OOM kills when exceeded. Setting them too low causes throttling or restarts; setting them too high wastes capacity and can reduce density.

**In this project:** API requests are 100m CPU/128Mi memory and limits are 500m/256Mi. Tune these from measured load, not guesswork.

### Q6. What is a PodDisruptionBudget (PDB)?
**Answer:** A PDB limits voluntary disruptions, such as node drains, by specifying how many pods must remain available or how many can be disrupted. It does not prevent involuntary failures such as node crashes or all pods failing simultaneously. It also does not replace replicas across failure domains.

**In this project:** `minAvailable: 2` with three replicas allows one voluntary disruption when all three are healthy.

### Q7. How do labels and selectors affect reliability?
**Answer:** Services, Deployments, NetworkPolicies and chaos experiments all depend on selectors. A selector that is too broad can route traffic to the wrong pods or inject faults into unintended workloads. Labels should be stable, specific and reviewed like code.

**Verify:** `kubectl -n resilience-lab get pods --show-labels`.

### Q8. What is a Kubernetes namespace? Is it a security boundary?
**Answer:** A namespace scopes names and many policy controls, but it is not a complete hard security boundary by itself. RBAC, NetworkPolicies, Pod Security Admission, admission policies and node isolation may also be needed. Cluster-scoped resources and privileged controllers require additional governance.

### Q9. What is the difference between ClusterIP, NodePort and LoadBalancer?
**Answer:** ClusterIP exposes a Service internally; NodePort opens a port on cluster nodes; LoadBalancer provisions or integrates an external load balancer where supported. Choose the smallest exposure required. This lab uses ClusterIP and port-forwarding for local testing.

### Q10. How would you troubleshoot a pod stuck in Pending?
**Answer:** Inspect events first, then check scheduling constraints, node capacity, PVC binding, taints/tolerations, affinity and quota.
```bash
kubectl -n resilience-lab describe pod <pod-name>
kubectl get nodes
kubectl describe node <node-name>
kubectl -n resilience-lab get events --sort-by=.lastTimestamp
```
Do not randomly increase replicas until the scheduling reason is known.

---

# Part 2 — Chaos engineering and resilience (Q11–Q20)

### Q11. What is chaos engineering?
**Answer:** It is a disciplined method of testing hypotheses about system behavior under controlled failure conditions. The process is: define steady state, form a hypothesis, introduce a bounded fault, observe, compare results, and improve the system. Randomly breaking systems without controls is not chaos engineering.

### Q12. What is the difference between chaos engineering and load testing?
**Answer:** Load testing measures behavior under volume, concurrency or throughput pressure. Chaos engineering tests behavior when components or dependencies fail or degrade. They can be combined, but the hypothesis and safety controls must remain explicit.

### Q13. Explain the pod-kill experiment in this repository.
**Answer:** The PodChaos manifest selects one pod with label `app.kubernetes.io/name=resilience-api` only in namespace `resilience-lab`, for a bounded 30-second experiment. The expected control is Deployment reconciliation and readiness-aware Service routing. Evidence includes pod replacement, request errors and time to recovery.

### Q14. Why must chaos experiments have a narrow selector?
**Answer:** The selector defines blast radius. A namespace-only selector may affect every workload in that namespace. Use both a dedicated namespace and application-specific labels, inspect the selected pods before applying, and never reuse the manifest against production.

### Q15. How would you test CPU saturation safely?
**Answer:** Capture baseline CPU, latency and errors. Apply a short, low-intensity stress experiment to one selected lab pod. Watch throttling, request latency, restarts and replica health. Stop if abort thresholds are reached. Do not start with all replicas or an unbounded duration.

### Q16. What does a network latency experiment prove?
**Answer:** It can reveal whether timeouts, retries, connection pools and graceful degradation behave as expected when network delay is introduced. It does not prove every network path is resilient. Measure end-to-end latency and error rate, and ensure retry policies do not amplify load.

### Q17. What is a steady-state hypothesis?
**Answer:** A measurable statement about normal service behavior and expected behavior during a fault. Example: "During termination of one API pod, at least two replicas remain Ready and the 5xx ratio stays below the agreed abort threshold." It must be testable with telemetry.

### Q18. What are blast radius and abort conditions?
**Answer:** Blast radius is the maximum scope of potential impact. Abort conditions are predefined signals that require stopping the experiment. This repo proposes aborting if fewer than two replicas are Ready, the 5xx ratio exceeds 5% for two minutes, p95 exceeds two seconds for two minutes, or telemetry is unavailable.

### Q19. What is MTTR and how do you measure recovery time?
**Answer:** Mean Time to Recovery is an operational measure of how long service takes to recover after an incident or fault. For an experiment, define start and recovery timestamps consistently—for example, from fault activation until the service returns to its healthy state and SLOs recover. Avoid using pod creation time alone as proof of service recovery.

### Q20. Why should chaos experiments not run automatically on every production deployment?
**Answer:** Fault injection can degrade or interrupt service. Production experiments require risk assessment, approvals, blast-radius controls, customer impact considerations, observability, rollback/abort procedures and a suitable change window. Start in isolated environments and progress only with explicit authorization and mature safeguards.

---

# Part 3 — Observability, Prometheus, Grafana and SLOs (Q21–Q30)

### Q21. What is the difference between metrics, logs and traces?
**Answer:** Metrics are aggregated numeric time series for trends and alerting. Logs are timestamped event records useful for detailed diagnosis. Traces show the path and timing of a request across distributed components. They complement each other; none replaces the others.

### Q22. What metrics does the sample API expose?
**Answer:** It exposes `http_requests_total` labeled by method, path and status, plus `http_request_duration_seconds` as a histogram. These support request rate, error ratio and latency percentile calculations. Avoid unbounded labels such as user IDs or raw URLs because they create cardinality problems.

### Q23. How do you calculate a 5xx error ratio in PromQL?
**Answer:** Divide the rate of 5xx requests by the rate of all requests over the same window:
```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
clamp_min(sum(rate(http_requests_total[5m])), 1)
```
The clamp prevents division by zero. Interpret the result alongside request volume and the measurement window.

### Q24. How do you calculate p95 latency from a Prometheus histogram?
**Answer:** Use `histogram_quantile` over the aggregated bucket rates:
```promql
histogram_quantile(
  0.95,
  sum by (le) (rate(http_request_duration_seconds_bucket[5m]))
)
```
All replicas should be aggregated by the `le` bucket label. Histogram buckets need enough resolution around the target latency.

### Q25. What is an SLI, SLO and SLA?
**Answer:** An SLI is the measured indicator, such as successful request ratio. An SLO is the internal target for that indicator over a defined window. An SLA is a customer-facing agreement, often with remedies or consequences. Do not call a sample dashboard threshold an SLA.

### Q26. How would you define availability?
**Answer:** Define what counts as a good event and a total eligible event. For example, successful valid requests divided by all valid requests over a rolling window. Exclusions, synthetic checks, maintenance windows and dependency failures must be documented to avoid misleading numbers.

### Q27. What is an error budget?
**Answer:** It is the allowable unreliability implied by an SLO. For a 99.9% availability SLO over a period, the error budget is 0.1% of eligible events in that period. Teams can use burn rate to decide whether to slow feature releases and prioritize reliability work.

### Q28. What is alert fatigue and how do you reduce it?
**Answer:** Too many low-value or duplicate alerts cause responders to ignore important signals. Alert on user-impacting symptoms, use sensible duration windows, group related alerts, assign clear ownership and include actionable runbook links. Avoid paging on every transient pod restart.

### Q29. Why is telemetry required before injecting faults?
**Answer:** Without a baseline and reliable telemetry, the team cannot quantify impact or know when to abort. Missing observability makes the experiment inconclusive, not successful. Confirm scrape targets, dashboards and alert delivery before starting.

### Q30. How would you distinguish an application failure from a Prometheus scrape failure?
**Answer:** Compare application health checks and user-facing synthetic requests with Prometheus target status. A failed scrape may mean the app is down, networking is blocked, the ServiceMonitor is misconfigured or Prometheus is unhealthy. Check target labels, endpoints, service port names, network policies and Prometheus logs.

---

# Part 4 — DevSecOps, Terraform and CI/CD (Q31–Q40)

### Q31. Why run containers as non-root?
**Answer:** It reduces the privileges available if an attacker compromises the process. Combine it with a read-only root filesystem, dropped Linux capabilities, seccomp, resource limits and minimal images. Non-root alone is not a complete container security strategy.

### Q32. Why disable service-account token automount for this API?
**Answer:** The sample API does not need to call the Kubernetes API. Removing an unnecessary token reduces credential exposure if the container is compromised. If a workload later needs Kubernetes API access, create a dedicated ServiceAccount and narrowly scoped Role/RoleBinding.

### Q33. What does a NetworkPolicy do?
**Answer:** It controls pod ingress and/or egress when the cluster network plugin supports NetworkPolicy. Policies are additive and selector-driven. A policy that blocks DNS or metrics scraping can break the lab, so validate the actual CNI and required flows before enforcement.

### Q34. What is Terraform state and why protect it?
**Answer:** State maps Terraform configuration to real infrastructure and may contain sensitive attributes. Store it remotely with encryption, access control, locking and versioning. Never commit state or secret-bearing tfvars to Git. Separate environments and restrict who can apply changes.

### Q35. What is the purpose of Terraform plan?
**Answer:** Plan previews the proposed changes by comparing configuration, state and provider observations. Review resource replacement, destructive actions, network exposure, identity permissions and cost before applying. A successful plan does not guarantee a successful deployment.

### Q36. Why does this project use a dedicated AKS resource group?
**Answer:** It isolates lifecycle, permissions, cost tracking and cleanup. The resource group should contain only lab resources. Verify the target subscription and resource group before apply or destroy; never run destroy against shared infrastructure.

### Q37. What should a secure GitHub Actions workflow include?
**Answer:** Least-privilege workflow permissions, pinned/reviewed actions, dependency and container scanning, secretless OIDC where cloud deployment is needed, protected environments for apply, artifact provenance and branch protection. This starter workflow validates code; it does not deploy to Azure.

### Q38. What is the difference between CI validation and CD deployment?
**Answer:** CI builds and validates changes—tests, linting, manifest checks, IaC validation and security scans. CD promotes approved artifacts/configuration to environments. This repository currently demonstrates validation, not a complete production deployment pipeline.

### Q39. How would you add image scanning?
**Answer:** Build the container, scan it with a maintained scanner such as Trivy, fail on agreed severity thresholds, generate an SBOM, and publish only approved immutable image digests. Document exceptions with owners and expiry dates. Do not rely only on a floating image tag.

### Q40. What is policy as code?
**Answer:** It expresses security and operational rules as version-controlled policies evaluated automatically. Examples include requiring non-root containers, blocking privileged pods and requiring resource limits. Test policy rules against both compliant and intentionally non-compliant examples to prove they work.

---

# Part 5 — Real-world troubleshooting scenarios (Q41–Q50)

### Q41. Scenario: one API pod is killed, but users report a brief spike in 503s. What do you investigate?
**Answer:** First confirm how many replicas were Ready and whether Service endpoints updated. Inspect pod termination, readiness probe timing, endpoint slices, application startup and client retry behavior. Correlate request errors with the fault timestamp. Potential fixes include faster but safe startup, accurate readiness, adequate replicas, topology spread and bounded client retries.

```bash
kubectl -n resilience-lab get pods -w
kubectl -n resilience-lab get endpointslice
kubectl -n resilience-lab describe pod <pod-name>
kubectl -n resilience-lab get events --sort-by=.lastTimestamp
```

### Q42. Scenario: all three replicas are Running, but the Service returns errors. What next?
**Answer:** Running is not the same as Ready or reachable. Check pod readiness, Service selector, EndpointSlices, container port/targetPort, NetworkPolicy, application logs and the actual response. Test from a temporary pod in the same namespace. Do not assume the Service is healthy from pod status alone.

### Q43. Scenario: CPU stress causes p95 latency to jump while CPU usage appears low. Why?
**Answer:** The container may be CPU-throttled by its limit, the metric may be sampled at a coarse interval, or the bottleneck may be elsewhere such as connection pools or downstream calls. Inspect throttling metrics (for example, container CPU throttled periods), node pressure, request concurrency and traces. Compare metrics at the same time resolution.

### Q44. Scenario: pods restart repeatedly after you add liveness probes. How do you fix it?
**Answer:** Inspect restart count, previous container logs and probe events. The liveness endpoint may be too strict, depend on a slow external service, or have an insufficient initial delay/timeout. Use startup probes for slow initialization and readiness for temporary inability to serve traffic. Tune from observed startup distributions rather than disabling health checks blindly.

### Q45. Scenario: NetworkPolicy is applied and Prometheus stops scraping the API. What happened?
**Answer:** The policy may not allow ingress from the Prometheus namespace/pods to TCP 8080, or selectors/labels may not match. Check the Prometheus namespace labels, ServiceMonitor selection, Service labels, endpoint port and CNI support. Add only the required scrape ingress rule; avoid opening all traffic as a permanent workaround.

### Q46. Scenario: Terraform wants to replace the AKS cluster unexpectedly. What do you do?
**Answer:** Stop before applying. Inspect the plan for ForceNew attributes, provider version changes, immutable settings and state drift. Confirm workspace, subscription and state backend. Discuss downtime and data implications. Back up state and use a controlled migration or import/state operation only when understood. Never approve a destructive plan just to make CI green.

### Q47. Scenario: a chaos experiment is still active after the test window. How do you respond?
**Answer:** Treat it as an active risk. Identify the exact Chaos Mesh custom resource, stop/delete that resource using the correct kind and namespace, then verify no other experiment remains. Confirm workload recovery and record why automatic expiry did not behave as expected. Add a cleanup safeguard to the run procedure.

### Q48. Scenario: the experiment dashboard shows no data. Can you call the experiment successful?
**Answer:** No. The run is inconclusive because impact cannot be measured. Check Prometheus target health, ServiceMonitor discovery, endpoint path/port, NetworkPolicy, scrape labels and Grafana data source. Restore telemetry and repeat the experiment only after a healthy baseline is confirmed.

### Q49. Scenario: AKS nodes run out of memory during a test. What is your response?
**Answer:** Stop the experiment and protect the cluster. Inspect node memory pressure, pod requests/limits, OOMKilled status, eviction events and workload placement. Reduce experiment intensity, isolate the lab, size nodes appropriately and ensure system capacity. Do not continue testing while node-level health is degraded.

### Q50. Scenario: your manager asks, "How do you prove this platform improves resilience?"
**Answer:** Agree measurable service objectives first. Run repeatable baseline and fault experiments, capture availability, p95 latency, error ratio and recovery time, compare results before and after remediation, and attach timestamped telemetry and configuration versions. Report failures and inconclusive tests honestly. A dashboard screenshot alone is not proof; include the experiment definition, conditions, raw evidence and reproducible steps.

---

# Practical lab assignments

Complete these in order and write your own observations in the result table.

## Lab 1 — Baseline and pod replacement
1. Deploy the app and confirm three Ready replicas.
2. Send a small stream of requests to `/work`.
3. Delete one pod and observe replacement.
4. Record time until three replicas are Ready and until requests are healthy again.

## Lab 2 — Chaos Mesh pod kill
1. Install Chaos Mesh in a disposable cluster using its official guide.
2. Confirm the CRDs and controllers are healthy.
3. Review the pod-kill manifest and verify its namespace and label selector.
4. Capture baseline metrics, apply for the documented duration, then verify recovery.
5. Record any 5xx spike and recovery time.

## Lab 3 — CPU stress
1. Capture baseline CPU, p95 latency and error ratio.
2. Apply the CPU stress template to one lab pod only.
3. Watch throttling, pod readiness, request latency and error rate.
4. Stop at the first abort condition and document what happened.

## Lab 4 — Security review
1. Inspect the Deployment securityContext.
2. Verify the process UID in a running container where the image/runtime permits.
3. Confirm service account token automount is disabled.
4. Test NetworkPolicy behavior in your CNI and document required flows.
5. Explain which controls are preventive and which are detective.

## Lab 5 — CI and Terraform
1. Open a pull request with a deliberate Python test failure and confirm CI catches it.
2. Make a deliberately invalid Kubernetes manifest in a temporary branch and confirm validation fails.
3. Run Terraform fmt, init with backend disabled, and validate.
4. Inspect a Terraform plan without applying it to a shared subscription.

## Personal study notes

| Topic | My explanation | Command / evidence | Confidence (1–5) |
|---|---|---|---|
| Kubernetes reconciliation | | | |
| Probes and recovery | | | |
| Chaos experiment safety | | | |
| PromQL and SLOs | | | |
| Terraform plan/state | | | |
| Container security | | | |
| CI/CD guardrails | | | |
| Incident troubleshooting | | | |

## Interview answer framework

Use this structure for scenario questions:

**Context → Impact → Diagnosis → Action → Validation → Prevention**

Example: "A pod termination caused elevated 5xx responses. I checked EndpointSlices and readiness transitions, correlated the error spike with the experiment, verified replacement pod startup, then adjusted readiness behavior and repeated the same controlled test. I used request error ratio and recovery time as evidence."

Do not claim a result you have not personally measured. In an interview, it is stronger to say "I designed the test and here is how I would validate it" than to invent a production success story.
