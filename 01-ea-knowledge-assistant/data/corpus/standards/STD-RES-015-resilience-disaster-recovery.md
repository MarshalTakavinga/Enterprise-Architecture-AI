---
doc_id: STD-RES-015
title: Resilience & Disaster Recovery Standard
doc_type: standard
version: "1.3"
status: Approved
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2025-029)
effective_date: 2025-05-15
next_review: 2026-11-15
classification: Internal
related: [AP-04, AP-06, AP-10, AP-11, AP-14, STD-CLD-007, STD-DAT-005, STD-SEC-009, STD-OBS-010, STD-CTR-012, STD-NET-011, ADR-0027, RA-02, RA-03, GOV-01, GOV-02]
---

# STD-RES-015 — Resilience & Disaster Recovery Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard assigns every Harbourline service to a resilience tier and defines the recovery time objective (RTO), recovery point objective (RPO), architecture patterns, backup controls and testing regime that each tier requires. It ensures that the services on which quay operations, customs compliance and customer visibility depend can survive component, zone, region and site failures, and it gives effect to AP-04: terminal operations must survive loss of WAN or cloud for 72 hours.

## 2. Scope

- All production services listed in the application portfolio, hosted in Azure, AWS (under STD-CLD-007), SaaS, the Baltimore data centre, and terminal edge sites.
- Platform services on which applications depend: the Harbourline Event Backbone (APP-120), the Harbourline API Gateway (APP-121), Entra ID (APP-100), SD-WAN (STD-NET-011) and AKS clusters.
- Non-production environments are out of scope except where they serve as DR capacity.

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-04 Business Continuity at the Quay | 72-hour edge autonomy for Tier 0 |
| AP-06 Data Residency Follows Jurisdiction | DR copies must respect residency |
| AP-11 Managed Services over Self-Managed Infrastructure | Use platform-native zone redundancy and geo-replication |
| AP-14 Observable by Default | Recovery depends on telemetry and SLOs (STD-OBS-010) |
| STD-DAT-005 | Approved regions for primary and DR data |
| ADR-0027 | Edge-hosted Navis N4 with local failover |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Service Tiers

### 4.1 Tier definitions

| Tier | Examples | RTO | RPO | Required pattern | DR test frequency |
|---|---|---|---|---|---|
| Tier 0 | Navis N4 TOS (APP-030), terminal gate automation (APP-031), crane control interfaces | 15 min | 0-5 min | Edge-hosted, local HA cluster, 72-hour autonomy without WAN/cloud | Semi-annually |
| Tier 1 | HSP (APP-022), Customs Filing Gateway (APP-060), Harbourline Connect (APP-050), Event Backbone, API Gateway | 1 h | 15 min | Multi-zone in primary region + paired-region DR | Annually |
| Tier 2 | Salesforce CRM (APP-040), Manhattan Active WM (APP-070), SAP S/4HANA Finance (APP-010) | 8 h | 1 h | Zone-redundant; cross-region restore or vendor DR | Annually (tabletop minimum) |
| Tier 3 | Internal tools, reporting utilities | 72 h | 24 h | Backup and restore | Restore test every 2 years |

### 4.2 Tier assignment

1. Every production service MUST have a tier recorded against its configuration item in ServiceNow (APP-110) and in the `hlg.service_tier` telemetry attribute (STD-OBS-010).
2. The business owner proposes the tier from a business impact assessment; the Principal Cloud Architect confirms it. Customer-facing or regulatory-filing services MUST NOT be below Tier 1 without ARB approval.
3. A service MUST NOT have a synchronous runtime dependency on a service of a lower tier. Where such a dependency exists, the dependency MUST be raised to the higher tier or decoupled asynchronously via the Event Backbone.

## 5. Tier 0 — Terminal Edge

1. Tier 0 systems MUST run at the terminal on a local cluster of at least two nodes with automatic failover (ADR-0027, RA-03).
2. Tier 0 systems MUST operate with full functionality for at least 72 hours with WAN and all cloud services unavailable. Authentication, time synchronisation, name resolution and licensing MUST all be locally available.
3. Local database replication between edge nodes MUST be synchronous or near-synchronous to meet an RPO of 0-5 minutes.
4. Replication of operational data to the cloud for analytics and off-site recovery MUST flow one-way through the IT/OT DMZ (STD-NET-011 §9) and MUST NOT be on the critical path of terminal operations.
5. Edge sites MUST have UPS capacity for orderly operation for at least 30 minutes and generator backup for 72 hours.
6. Each terminal MUST maintain an off-site encrypted backup of Tier 0 configuration and data, restorable to replacement hardware within 24 hours from spare stock held on site.

## 6. Tier 1 — Cloud Critical

1. Tier 1 services MUST be deployed across three availability zones in the primary region, with no single-zone component.
2. Tier 1 services MUST have a DR capability in the paired region, using only approved region pairs that keep data within its jurisdiction (STD-DAT-005):

| Primary | DR | Data scope |
|---|---|---|
| East US 2 | Central US | US and aggregated data |
| West Europe | North Europe | EU personal data |
| Canada Central | Canada East | Canadian contractual data |
| UAE North | None approved | See rule 3 |

3. UAE North has no in-jurisdiction DR region in the approved list. Tier 1 workloads in UAE North MUST use zone redundancy plus immutable backups held in UAE North; any cross-region DR design requires ARB Tier 1 approval with DPO sign-off.
4. Databases MUST use geo-replication or cross-region read replicas (for example, PostgreSQL Flexible Server geo-redundant backup or read replica) sized to meet a 15-minute RPO.
5. The Event Backbone MUST replicate Tier 1 topics to the DR cluster via cluster linking; consumers MUST be able to resume from replicated offsets.
6. DR MAY be warm standby (scaled-down, running) or pilot light, provided the RTO of 1 hour is proven in test. Failover SHOULD be automated and MUST be executable from a documented runbook.
7. Infrastructure and application configuration MUST be fully reproducible from Terraform and GitOps repositories in the DR region (STD-CTR-012).

## 7. Backup

1. All services MUST have backups meeting their tier's RPO.
2. Backups for Tier 0 and Tier 1 MUST be immutable (write-once, retention-locked) for at least 30 days and logically separated from production credentials, to withstand ransomware.
3. Backups MUST be encrypted per STD-SEC-009 and stored in the same jurisdiction as the source data.
4. Restores MUST be tested at least quarterly for Tier 0 and Tier 1 on a sample basis.

## 8. DR Testing

1. Tier 0 DR tests MUST be performed semi-annually per terminal, including a WAN-isolation test demonstrating local operation, and an edge-node failover.
2. Tier 1 DR tests MUST be performed annually per service, including a regional failover and failback, and MUST measure achieved RTO and RPO.
3. Test plans, results and remediation actions MUST be recorded in ServiceNow; a failed test MUST have a remediation plan approved within 30 days and a re-test within 90 days.
4. The Principal Cloud Architect reports DR test status to the ARB quarterly.

## 9. SaaS and Third-Party Services

1. For SaaS services, the contract MUST specify RTO/RPO at least equal to the service's tier, or the gap MUST be accepted by the business owner and recorded as an exception.
2. Harbourline MUST retain the ability to export its data from any Tier 1 or Tier 2 SaaS service in a usable format.

## 10. Compliance & Exceptions

1. Tier assignment and resilience design are assessed at ARB Tier 1 and Tier 2 reviews under GOV-01. No Tier 0 or Tier 1 service may go live without a completed DR runbook.
2. Deviations MUST follow the GOV-01 exception process and be recorded in GOV-02, with a remediation plan and a maximum duration of 12 months, renewable once. Nordhaven TMS DR on AWS is governed by EXC-2025-003 until migration into HSP.

## 11. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2023-09-11 | Kenji Watanabe | First issue; four tiers defined |
| 1.1 | 2024-04-22 | Kenji Watanabe | Tier 0 edge requirements aligned with ADR-0027 |
| 1.2 | 2024-11-04 | Kenji Watanabe | Region pairs aligned with STD-DAT-005; immutable backups |
| 1.3 | 2025-05-15 | Kenji Watanabe | Tier 0 RTO tightened to 15 min; semi-annual Tier 0 tests; UAE North DR rule (ARB-2025-029) |
