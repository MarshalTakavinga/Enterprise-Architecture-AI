---
doc_id: ADR-0021
title: Temporarily Retain Nordhaven TMS on AWS
doc_type: adr
version: "1.1"
status: Accepted
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2024-026)
effective_date: 2024-07-02
next_review: 2026-07-02
classification: Internal
related: [AP-06, AP-10, AP-11, AP-12, STD-CLD-007, STD-DAT-005, STD-DB-006, STD-EVT-003, ADR-0007, ADR-0019, GOV-02, F-01, APP-021, APP-022, APP-120]
---

# ADR-0021 — Temporarily Retain Nordhaven TMS on AWS

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-07-02 |
| ARB decision | ARB-2024-026 (session of Thursday 2024-06-27), Approved with Conditions |
| Deciders | David Okafor (Chair), Kenji Watanabe, Priya Raman, Amara Osei, Lena Vogel |
| Consulted | Nordhaven Freight GmbH IT lead, Marieke de Vries (DPO), Grace Liu |
| Review tier | Tier 1 (deviation from cloud hosting standard; EU personal data) |
| Revision 1.1 | Hosting deviation recorded in the Exceptions Register as EXC-2025-003 |

## 2. Context

Harbourline completed the acquisition of Nordhaven Freight GmbH (Hamburg) in March 2024. Nordhaven's transport management system (APP-021) is a Java 11 application running on Amazon EKS in AWS eu-central-1 (Frankfurt), with MongoDB Atlas (also in eu-central-1) as its database. It handles ~1,400 shipments/day for about 2,300 active customers, most of them EU-based, so it holds EU personal data (consignee contacts, driver names).

STD-CLD-007 names Azure as the primary cloud. The target state is that Nordhaven lanes run on the Harbourline Shipment Platform (HSP, APP-022), which is still in build; the Nordhaven migration is planned as a later wave after US lanes go live. The question is what to do with the Nordhaven TMS in the interim.

Nordhaven's platform team is 7 engineers, all AWS-skilled; none have Azure production experience. Their AWS run cost is ~EUR 41k/month.

## 3. Decision Drivers

1. Minimise disruption to Nordhaven customers during integration of the business.
2. Avoid migrating the same workload twice (once to Azure IaaS/AKS, then again into HSP).
3. Keep EU personal data in the EU (AP-06, STD-DAT-005).
4. Establish secure, governed connectivity to Harbourline's Azure estate and event backbone.
5. Retain Nordhaven staff and their knowledge through the transition.

## 4. Considered Options

- **Option A — Retain on AWS eu-central-1 until HSP migration**, connected via Confluent cluster linking and private connectivity.
- **Option B — Lift-and-shift to Azure West Europe now** (AKS + MongoDB Atlas on Azure), then migrate into HSP later.
- **Option C — Accelerate Nordhaven into HSP immediately**, ahead of US lanes.

### 4.1 Comparison

| Criterion | A — Retain on AWS | B — Lift-and-shift to Azure | C — Accelerate into HSP |
|---|---|---|---|
| One-off cost (est.) | EUR 0.3M (connectivity, integration) | EUR 1.6M (migration, re-testing, dual run) | Not estimable; HSP not feature-ready |
| Double migration | No | Yes | No |
| Customer disruption risk | Low | Medium (cutover of live TMS) | High |
| EU data residency | Compliant (Frankfurt) | Compliant (West Europe) | Compliant |
| Alignment with STD-CLD-007 | Deviation; exception required | Compliant | Compliant |
| Skills fit | Strong | Weak in the first 12 months | Weak |
| Impact on HSP US release | None | Low | Severe (scope diverted) |

## 5. Decision Outcome

**Chosen option: A — Retain the Nordhaven TMS in AWS eu-central-1 until it is migrated into HSP.**

Conditions:

1. **Integration:** Nordhaven publishes shipment events to its own Confluent Cloud cluster on AWS eu-central-1, linked to the Harbourline Event Backbone (APP-120) with **Confluent cluster linking**. Topics follow STD-EVT-003 naming. No point-to-point database links to Harbourline systems.
2. **Connectivity:** private connectivity only (AWS PrivateLink to Confluent; site-to-site IPsec between the Nordhaven VPC and the Harbourline West Europe hub). No new public endpoints; any API consumed outside Nordhaven is fronted by the Harbourline API Gateway (ADR-0019).
3. **Identity:** AWS IAM Identity Center federated to Microsoft Entra ID; MFA enforced, local IAM users removed within 90 days.
4. **Data:** personal data stays in eu-central-1; only non-personal event fields replicate to US-hosted consumers, with a Transfer Impact Assessment where that is not possible.
5. **Freeze:** no new capabilities on the Nordhaven TMS beyond regulatory changes; no new AWS workloads under this decision.
6. **Exception:** the hosting deviation is recorded in the Exceptions Register (GOV-02) as **EXC-2025-003**, with a remediation plan tied to the HSP migration work package.

## 6. Consequences

### 6.1 Positive

- Nordhaven customers see no platform change during the integration year.
- Avoids an estimated EUR 1.6M spent on a migration that would be discarded.
- Cluster linking gives Harbourline near-real-time visibility of Nordhaven shipments (lag < 5 s measured in PoC).

### 6.2 Negative

- Two cloud estates to secure and monitor; Sentinel must ingest AWS CloudTrail and GuardDuty findings (~USD 3k/month ingestion).
- MongoDB Atlas and Java 11 remain in the estate (Trial and Contain respectively on the radar), sustaining skills and patching overhead.
- Cross-cloud replication costs ~USD 4-6k/month in Confluent linking and AWS egress.
- Exceptions are capped at 12 months and renewable once under GOV-01, so this retention window is finite; if the HSP migration of Nordhaven slips past the final expiry, a fresh Tier 1 decision will be needed and the programme may be forced into an interim move.
- Nordhaven engineers are not building Azure skills in the meantime, which raises migration risk later.

### 6.3 Neutral

- AWS remains a secondary cloud under STD-CLD-007; this decision does not broaden its permitted use.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Stand up cluster link and private connectivity | Amara Osei / Kenji Watanabe | 2024-09-30 |
| Federate AWS access to Entra ID, remove IAM users | Priya Raman | 2024-10-31 |
| Register exception with remediation plan | Samuel Adeyemi | before expiry of the interim ARB approval |
| Azure enablement programme for Nordhaven team | Kenji Watanabe | 2025-06-30 |
| Quarterly exception status to ARB | Kenji Watanabe | quarterly |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| STD-CLD-007 | Deviation; permitted only as case (a) Nordhaven legacy workloads under EXC-2025-003. |
| AP-10 Cloud-Smart and Portable | Consistent with pragmatic use of the secondary cloud; Kafka linking keeps integration portable. |
| AP-06 / STD-DAT-005 | Compliant; EU personal data remains in the EU. |
| AP-12 / STD-IAM-008 | Compliant after Entra federation. |
| STD-DB-006 | MongoDB Atlas permitted as Trial for Nordhaven only. |

## 8. Links

- GOV-02 Architecture Exceptions Register (EXC-2025-003)
- F-01 Architecture Roadmap & Migration Plan — Horizon 2028 (Nordhaven migration)
- ADR-0007 Adopt Confluent Cloud as the Enterprise Event Backbone
- ADR-0019 Azure API Management as the Single API Gateway
- ARB log entry ARB-2024-026
