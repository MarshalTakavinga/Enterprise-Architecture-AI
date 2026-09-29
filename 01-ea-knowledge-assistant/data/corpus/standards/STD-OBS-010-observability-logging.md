---
doc_id: STD-OBS-010
title: Observability & Logging Standard
doc_type: standard
version: "1.1"
status: Approved
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2025-044)
effective_date: 2025-07-01
next_review: 2026-10-01
classification: Internal
related: [AP-14, AP-15, AP-04, AP-12, STD-SEC-009, STD-DAT-004, STD-CTR-012, STD-RES-015, STD-EVT-003, RA-02, GOV-01, GOV-02]
---

# STD-OBS-010 — Observability & Logging Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard makes every Harbourline service observable by default (AP-14). It defines how services emit traces, metrics and logs, where that telemetry is stored and for how long, what must never be written to a log, and the minimum health and service-level instrumentation expected before a service goes live. Consistent telemetry is a precondition for the latency commitment in Horizon 2028 (95% of shipment milestones visible to customers in under five minutes, REQ-HSP-014) and for the recovery objectives in STD-RES-015.

## 2. Scope

### 2.1 In scope

- All new services and material changes to existing services built or bought by Harbourline, on Azure, on AWS (under STD-CLD-007) and at terminal edge sites.
- Platform components operated by Harbourline: AKS clusters, Azure Container Apps environments, API Management (APP-121), the Harbourline Event Backbone (APP-120) and integration runtimes.
- SaaS applications, to the extent that the vendor exposes audit and diagnostic logs.

### 2.2 Out of scope

- OT device telemetry at Purdue levels 0-2, which is collected and forwarded through the IT/OT DMZ as defined in STD-NET-011 and RA-03.
- Business analytics pipelines into Tidewater (APP-080), which follow RA-04.

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-14 Observable by Default | Primary driver of this standard |
| AP-15 Everything as Code | Dashboards, alert rules and diagnostic settings are deployed as code |
| AP-04 Business Continuity at the Quay | Edge sites must buffer telemetry during WAN loss |
| STD-DAT-004 | Defines Confidential and Restricted data that must not reach logs |
| STD-SEC-009 | Secrets and keys must never be logged |
| STD-RES-015 | Service tiers that determine SLO and alerting requirements |
| STD-EVT-003 | Kafka record headers used for trace propagation |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Instrumentation

### 4.1 OpenTelemetry

1. New services MUST be instrumented with the OpenTelemetry (OTel) SDK for their language (.NET, Java, Python, JavaScript). Vendor-proprietary agents MUST NOT be the sole instrumentation for new services.
2. Services MUST emit the three signals: distributed traces, metrics and structured logs.
3. Auto-instrumentation SHOULD be enabled for HTTP, gRPC, database and Kafka client libraries; manual spans SHOULD be added around business operations such as "record milestone" or "submit customs filing".
4. Existing services MAY retain Application Insights classic SDKs until their next major release, at which point they MUST move to OTel.

### 4.2 Context propagation

1. W3C Trace Context (`traceparent`, `tracestate`) MUST be propagated on all synchronous calls, including calls through the Harbourline API Gateway.
2. Event producers MUST write the `traceparent` value into Kafka record headers; consumers MUST continue the trace as a linked span. This allows a shipment milestone to be traced from HSP through the outbox and the Event Backbone to Harbourline Connect.
3. Services MUST NOT strip or regenerate trace headers received from an upstream Harbourline component.

### 4.3 Resource attributes

Every signal MUST carry the resource attributes `service.name`, `service.version`, `deployment.environment`, and the Harbourline attributes `hlg.app_id` and `hlg.service_tier`, matching the mandatory `app-id` tag in STD-CLD-007.

## 5. Telemetry Platform

1. The central observability platform is Azure Monitor (Log Analytics workspaces and Application Insights) with Azure Managed Grafana for dashboards.
2. Telemetry SHOULD be exported via an OpenTelemetry Collector deployed per AKS cluster or per Container Apps environment, allowing sampling, attribute redaction and routing to be configured centrally.
3. Log Analytics workspaces are regional. Telemetry containing EU personal data MUST NOT be generated in the first place (see §7); operational telemetry from EU workloads MUST nonetheless be stored in the West Europe workspace so that any accidental leakage remains in-region.
4. Security-relevant logs (Entra ID sign-ins and audit, Key Vault access, Azure Activity, FortiGate and FortiAnalyzer events, AKS audit) MUST be forwarded to Microsoft Sentinel.
5. Nordhaven workloads on AWS MUST forward logs to Harbourline Log Analytics through the approved collector until migration into HSP.

## 6. Retention

| Telemetry type | Store | Retention |
|---|---|---|
| Application and platform logs | Log Analytics | 13 months (90 days interactive, remainder archive tier) |
| Security logs | Microsoft Sentinel | 24 months |
| Metrics | Azure Monitor Metrics / managed Prometheus | 13 months (downsampled after 93 days) |
| Traces | Application Insights | 90 days |
| AI prompts and responses | Log Analytics (dedicated table, restricted access) | 90 days |

Retention MUST NOT be reduced below these values without an approved exception. Longer retention required by legal hold is set by the Group DPO or legal counsel and overrides this table.

## 7. Content Rules — What Must Not Be Logged

1. Logs, traces, span attributes and metric labels MUST NOT contain personal data. This includes names, email addresses, phone numbers, passport numbers, customer contact details and free-text fields that may contain them.
2. Logs MUST NOT contain secrets, access tokens, API keys, session cookies, connection strings or cryptographic material (STD-SEC-009).
3. Logs MUST NOT contain Restricted data as defined in STD-DAT-004, including OT/terminal security configuration.
4. Business identifiers that are not personal data (shipment ID, container number, booking reference) MAY be logged and SHOULD be used for correlation.
5. The OTel Collector MUST apply a redaction processor for known sensitive attribute keys as a safety net; redaction does not remove the obligation in rules 1-3.
6. Log records MUST be structured JSON with a severity field; unstructured `printf`-style logs MUST NOT be introduced in new services.

## 8. Health Endpoints

1. Every service MUST expose liveness and readiness endpoints (`/health/live`, `/health/ready`). Readiness MUST reflect the availability of critical dependencies.
2. Health endpoints MUST NOT return dependency connection strings, stack traces or version details to unauthenticated callers.
3. Services on AKS MUST wire these endpoints to Kubernetes probes in line with STD-CTR-012.

## 9. Service Level Objectives and Alerting

1. Tier 0 and Tier 1 services (STD-RES-015) MUST define SLOs for availability and latency before go-live, expressed as SLIs computed from OTel data, and MUST publish them on a Grafana dashboard.
2. Tier 0 and Tier 1 services MUST implement error-budget burn-rate alerts routed to the on-call rota in ServiceNow (APP-110).
3. Tier 2 services SHOULD define SLOs; Tier 3 services MAY rely on platform alerts.
4. Alert rules, action groups and dashboards MUST be defined in Terraform or as dashboard JSON in source control (AP-15).
5. Terminal edge systems MUST buffer telemetry locally for at least 72 hours and forward it when WAN connectivity is restored (AP-04).

## 10. Compliance & Exceptions

1. Conformance is verified at ARB review against the observability checklist in GOV-01; Azure Policy enforces diagnostic settings on all resources in the `hlg-corp` and `hlg-online` management groups.
2. Deviations MUST follow the GOV-01 exception process and be recorded in GOV-02 with a remediation plan and a maximum duration of 12 months, renewable once.
3. A detected occurrence of personal data or secrets in logs MUST be raised as a security incident and the affected records purged from the workspace.

## 11. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2024-08-01 | Kenji Watanabe | First issue; OpenTelemetry mandatory for new services |
| 1.1 | 2025-07-01 | Kenji Watanabe | Added Kafka header trace propagation, Sentinel 24-month retention, SLO requirement for Tier 0/1, edge buffering (ARB-2025-044) |
