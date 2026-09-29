---
doc_id: STD-CTR-012
title: Container Platform Standard
doc_type: standard
version: "1.2"
status: Approved
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2025-017)
effective_date: 2025-03-15
next_review: 2026-12-15
classification: Internal
related: [AP-10, AP-11, AP-12, AP-14, AP-15, STD-CLD-007, STD-IAM-008, STD-SEC-009, STD-OBS-010, STD-RES-015, STD-TLC-014, RA-02, GOV-01, GOV-02]
---

# STD-CTR-012 — Container Platform Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines the approved platforms for running containerised workloads at Harbourline and the mandatory controls for building, storing, deploying and operating container images. It ensures that the microservices of the Harbourline Shipment Platform (APP-022), the Harbourline Connect BFF (APP-050) and future cloud-native services run on a consistent, secure and supportable platform, in line with RA-02.

## 2. Scope

### 2.1 In scope

- All container workloads deployed to Harbourline Azure subscriptions in any environment (development, test, pre-production, production).
- Container image build pipelines, the container registry, and deployment tooling.
- Suppliers, including Kestrel Digital Partners on the HSP programme, that build or deploy containers on Harbourline's behalf.

### 2.2 Out of scope

- The Navis N4 edge cluster at terminals (APP-030), which is governed by ADR-0027 and RA-03.
- Container workloads of Nordhaven TMS (APP-021) on AWS, which remain covered by EXC-2025-003 until migration into HSP.
- Developer workstation tooling.

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-11 Managed Services over Self-Managed Infrastructure | Only managed Kubernetes and managed container services are permitted |
| AP-10 Cloud-Smart and Portable | Standard Kubernetes APIs and Helm charts preserve portability |
| AP-12 Zero Trust Access | Workload identity, network policy and private clusters |
| AP-15 Everything as Code | Clusters in Terraform; workloads delivered by GitOps |
| STD-CLD-007 | Landing zone placement, tagging and ingress rules |
| STD-SEC-009 | Encryption, secrets and certificate handling |
| STD-OBS-010 | Telemetry and health endpoints |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Approved Platforms

| Platform | Radar status | Use |
|---|---|---|
| Azure Kubernetes Service (AKS) | Adopt | Standard platform for microservices, APIs and long-running workloads |
| Azure Container Apps | Adopt | Simple event-driven services, scheduled jobs, low-traffic APIs without Kubernetes-specific needs |
| Azure Functions (container-hosted) | Adopt (via STD-CLD-007) | Short-lived functions where Container Apps is not justified |
| Self-managed Kubernetes (kubeadm, Rancher, OpenShift on VMs) | Prohibited | No new or existing use permitted |
| Docker on standalone VMs | Prohibited for production | Legacy only under exception |

1. AKS MUST be the default choice for new container workloads.
2. Azure Container Apps MAY be selected for a service that is event-driven or scale-to-zero, has no need for custom operators, service mesh or node-level configuration, and is classified Tier 2 or Tier 3 under STD-RES-015. Tier 0 or Tier 1 services on Container Apps require ARB Tier 2 review.
3. Self-managed Kubernetes distributions MUST NOT be deployed in any environment.

## 5. Cluster Configuration

1. AKS clusters MUST be provisioned with Terraform using the platform team's approved module; clusters MUST NOT be created through the portal or CLI.
2. Production clusters MUST be private clusters (API server via private endpoint) and MUST NOT expose public IPs on nodes. Ingress MUST enter through Azure Front Door with WAF or Application Gateway, per STD-CLD-007.
3. Production clusters MUST be zone-redundant across three availability zones, with the system node pool separated from user node pools.
4. Clusters MUST use Azure CNI Overlay networking and MUST enforce Kubernetes network policies with a default-deny posture per namespace.
5. Clusters MUST be integrated with Entra ID for Kubernetes RBAC; local accounts MUST be disabled. Cluster-admin rights MUST be obtained through Entra PIM (STD-IAM-008).
6. The Kubernetes version MUST be within the two most recent minor versions supported by AKS. Node images MUST be updated at least monthly through automatic node-image upgrade channels.
7. Microsoft Defender for Containers and Azure Policy for AKS MUST be enabled on every cluster.
8. Multi-tenant clusters are the default per environment and region; a dedicated cluster requires justification (for example, Restricted data isolation or a regulatory need).

## 6. Images and Registry

1. Images deployed to Harbourline clusters MUST be pulled only from the Harbourline Azure Container Registry `hlgacr`. Admission policy MUST reject images from any other registry.
2. Public base images MUST be imported into `hlgacr` through the curated base-image pipeline; teams MUST NOT reference Docker Hub or other public registries at runtime.
3. Every image MUST be signed with Notation using the Harbourline signing key held in Azure Key Vault, and signature verification MUST be enforced at admission.
4. Every image MUST be scanned for vulnerabilities at build time and continuously in the registry. Images with critical CVEs MUST NOT be deployed to production; high CVEs MUST be remediated within 30 days.
5. Images MUST be tagged with an immutable version and referenced by digest in production manifests; the `latest` tag MUST NOT be used.
6. Images MUST include a software bill of materials (SBOM) in SPDX or CycloneDX format, stored as an ACR artefact.

## 7. Workload Security

1. Containers MUST run as a non-root user with a read-only root file system unless an exception is recorded.
2. Privileged containers, host networking, host PID/IPC and `hostPath` mounts MUST NOT be used in workload namespaces.
3. Workloads MUST authenticate to Azure services with Entra Workload ID (federated managed identity). Kubernetes secrets MUST NOT hold long-lived credentials; secrets MUST be mounted from Azure Key Vault through the Secrets Store CSI driver (STD-SEC-009).
4. Every container MUST declare CPU and memory requests and memory limits.
5. Pod Security Admission MUST be enforced at the `restricted` profile for workload namespaces.

## 8. Deployment

1. Workloads MUST be packaged as Helm charts and deployed through GitOps using Flux. Manual `kubectl apply` in production is prohibited except during a recorded emergency change.
2. The Git repository is the source of truth for cluster state; drift MUST be reconciled automatically.
3. Production deployments MUST use a progressive strategy (rolling with readiness gates, or canary) and MUST define PodDisruptionBudgets for Tier 0/1 services.
4. Liveness and readiness probes MUST map to the health endpoints required by STD-OBS-010 §8.

## 9. Operations

1. Each cluster MUST run an OpenTelemetry Collector and forward telemetry per STD-OBS-010.
2. Cluster configuration and GitOps repositories MUST be recoverable within the RTO of the highest-tier workload hosted, as required by STD-RES-015.
3. Namespace ownership MUST be recorded against the `app-id` tag and the configuration item in ServiceNow (APP-110).

## 10. Compliance & Exceptions

1. Conformance is enforced by Azure Policy and admission controls, and assessed at ARB Tier 1 and Tier 2 reviews under GOV-01.
2. Deviations MUST be requested through the GOV-01 exception process and recorded in GOV-02 with a remediation plan and a maximum duration of 12 months, renewable once.
3. Admission-policy bypasses MUST be time-limited, logged and reviewed at the next ARB meeting.

## 11. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2024-03-04 | Kenji Watanabe | First issue; AKS as standard platform |
| 1.1 | 2024-10-14 | Kenji Watanabe | Added Notation signing and GitOps with Flux |
| 1.2 | 2025-03-15 | Kenji Watanabe | Azure Container Apps moved to Adopt; SBOM requirement; self-managed Kubernetes explicitly prohibited (ARB-2025-017) |
