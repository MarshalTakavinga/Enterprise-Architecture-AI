---
doc_id: F-01
title: Architecture Roadmap & Migration Plan — Horizon 2028
doc_type: togaf_deliverable
togaf_phase: F
version: "2.2"
status: Approved
owner: Grace Liu, Programme Director, Horizon 2028 / HSP
approved_by: Architecture Review Board (ARB-2026-029)
effective_date: 2026-08-06
next_review: 2027-02-04
classification: Internal
related: [A-01, A-02, ADD-01, ARS-01, G-01, GOV-02, AP-04, AP-06, AP-10, STD-INT-001, STD-DAT-005, STD-CLD-007, STD-RES-015, STD-TLC-014, ADR-0015, ADR-0021, ADR-0027, ADR-0041]
---

# F-01 — Architecture Roadmap & Migration Plan — Horizon 2028

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This plan sequences the work that moves Harbourline from the baseline described in ADD-01 (three transport management systems, MuleSoft, Oracle 12c, Baltimore data centre) to the target in which the Harbourline Shipment Platform (HSP, APP-022) is the single shipment system of record on Azure. It defines three transition architectures, ten work packages (WP-01 to WP-10), the migration waves by lane, the principal risks and the decommissioning plan. Status is as at the August 2026 ARB re-baseline.

## 2. Planning Constraints

| Constraint | Date | Source |
|---|---|---|
| MuleSoft Anypoint (APP-122) sunset | 2026-12-31 | ADR-0015, STD-TLC-014 |
| Nordhaven TMS AWS exception expiry (already renewed once) | 2026-12-31 | EXC-2025-003, ADR-0021 |
| Oracle 12c retirement; FreightMaster extended support ends | 2027-03-31 | EXC-2026-001, STD-TLC-014 |
| Baltimore data centre exit | 2027-06-30 | Horizon 2028 goal 3 |
| FreightMaster TMS (APP-020) retired | Q3 2027 | Application portfolio |
| Single TMS (target state) | Q4 2027 | Horizon 2028 goal 1 |

Terminal peak seasons (October to December for the US and EU retail trades) are change-freeze windows for lane cutovers unless the ARB approves otherwise.

## 3. Transition Architectures

### 3.1 TA1 — US Lanes on HSP (achieved November 2025)

HSP core services, the US regional stamp in East US 2 (DR Central US) and the outbox/CDC publication path went live on 2025-11-17 for Harbourline Inc. US ocean and air lanes. Harbourline Connect US consumes `shipment.milestone.recorded.v1` and `shipment.status.changed.v1` into its read model (ADR-0030). FreightMaster still serves Canada, Gulf and US road lanes; the Rotterdam instance and Nordhaven TMS are unchanged. Measured milestone latency for US lanes in July 2026: 2 min 40 s p95 (REQ-HSP-014 target < 5 min).

### 3.2 TA2 — EU Lanes and Nordhaven Migrated (target Q2 2027)

The EU stamp in West Europe (DR North Europe) carries all Harbourline Europe and Nordhaven lanes. The FreightMaster Rotterdam instance and Nordhaven TMS (APP-021) are read-only. Canada lanes run on the HSP CA data cell. MuleSoft is gone; all cross-domain integration uses the Event Backbone or the API Gateway. Customs Filing Gateway (APP-060) subscribes to HSP events for US, Canadian and EU filings. Gulf lanes are migrated to the UAE North data cell. FreightMaster no longer accepts bookings.

### 3.3 TA3 — Target Architecture (Q4 2027)

HSP is the only TMS. FreightMaster is formally retired (Q3 2027), Oracle 12c is gone, the Baltimore data centre is exited (2027-06-30), AWS eu-central-1 hosts no shipment workloads, and Sterling B2B carries only long-tail carrier EDI. Historical shipment data is available from Tidewater (APP-080) under RA-04.

## 4. Work Packages

| WP | Name | Scope | Depends on | Start | End | Cost estimate (USD M) | Status (Aug 2026) |
|---|---|---|---|---|---|---|---|
| WP-01 | HSP Core Platform | Domain services, 12-status model, landing zone stamps, outbox/CDC, customer reference to Salesforce | — | 2025-01 | 2025-11 | 14.2 | Complete |
| WP-02 | US Lanes Migration | Cutover of US ocean/air lanes; then US road lanes | WP-01 | 2025-05 | 2026-10 | 9.8 | Road lanes in progress |
| WP-03 | Integration Modernisation & MuleSoft Exit | Replace ~140 remaining flows with INT-P1/INT-P3; SAP charge events | WP-01 | 2025-03 | 2026-12 | 7.5 | 61 flows remaining |
| WP-04 | Customer Visibility | Connect read models per stamp incl. UAE stamp (CR-2026-014); milestone SLOs; CNS event feeds | WP-01, WP-03 | 2025-06 | 2027-06 | 6.1 | In progress |
| WP-05 | Customs Data Hand-off | Replace DB link with event subscription for APP-060; ICS2 and CARM data | WP-01 | 2025-09 | 2027-03 | 4.3 | US done; CA/EU in progress |
| WP-06 | EU Lanes & Nordhaven Migration | Rotterdam instance and Nordhaven lanes to EU stamp; 22→12 status mapping | WP-01, WP-05 | 2026-04 | 2027-06 | 12.6 | In progress |
| WP-07 | Canada & Gulf Lanes Migration | CA data cell (Canada Central) and UAE North data cell; FreightMaster booking freeze | WP-01, WP-05 | 2026-06 | 2027-03 | 8.9 | In progress |
| WP-08 | Data Migration & Archive | Open-shipment migration; closed history to Tidewater; 7-year retention (REQ-HSP-024) | WP-02, WP-06, WP-07 | 2026-01 | 2027-09 | 3.7 | In progress |
| WP-09 | Baltimore DC Exit | Remaining Baltimore workloads, network re-termination, hardware disposal | WP-03, WP-07, WP-08 | 2026-03 | 2027-06 | 11.4 | In progress |
| WP-10 | Carrier Connectivity | Partner APIs for top 25 carriers; Sterling reduced to long tail | WP-01, WP-03 | 2026-01 | 2027-12 | 5.2 | 9 carriers live |

Total HSP work package estimate: USD 83.7M. The balance of the USD 118M Horizon 2028 envelope covers programme contingency (12%), security and resilience uplift, and non-HSP items managed outside this plan.

## 5. Migration Waves

Lanes move in waves. A lane is cut over only when its open shipments can be migrated with less than 0.1% reconciliation variance and the customs hand-off for its jurisdiction is event-driven (WP-05).

| Wave | Lanes | Source system | Target stamp / cell | Window | Transition |
|---|---|---|---|---|---|
| 1 | US ocean and air | FreightMaster | US (East US 2) | 2025-11 | TA1 (done) |
| 2 | US road | FreightMaster | US (East US 2) | 2026-09 to 2026-10 | TA1→TA2 |
| 3 | Canada (all modes) | FreightMaster | CA (Canada Central) | 2026-11 to 2027-01 | TA2 |
| 4 | Gulf (all modes) | FreightMaster | UAE North | 2027-01 to 2027-03 | TA2 |
| 5 | Harbourline Europe | FreightMaster Rotterdam instance | EU (West Europe) | 2027-01 to 2027-03 | TA2 |
| 6 | Nordhaven | Nordhaven TMS (AWS) | EU (West Europe) | 2027-03 to 2027-06 | TA2 |

Waves 3 to 5 must finish before 2027-03-31 because both FreightMaster instances depend on Oracle 12c. Wave 3 overlaps the peak-season freeze; the ARB approved a Canada-only exception to the freeze on the grounds that Halifax volumes peak in Q1, not Q4 (ARB-2026-029).

Each wave follows the same pattern: dual-run for up to 90 days with HSP as the source of truth for new bookings, reconciliation daily, customs hand-off switched per jurisdiction, then the legacy lane is frozen read-only.

## 6. Risks

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Nordhaven migration (wave 6) completes after EXC-2025-003 expires on 2026-12-31; the exception cannot be renewed a second time under GOV-01 | High | High | ARB to decide on the treatment of residual Nordhaven workload before 2026-11-30; accelerate Nordhaven status mapping | Samuel Adeyemi |
| R2 | MuleSoft flows not replaced by 2026-12-31 | Medium | High | Weekly burn-down; no new flows since 2025-06-30; priority on SAP and customs flows | Amara Osei |
| R3 | Oracle 12c support ends before waves 3-5 complete | Medium | High | Waves 4 and 5 run in parallel; booking freeze on FreightMaster from 2027-03-01 | Grace Liu |
| R4 | UAE North has no approved paired DR region in STD-CLD-007 | High | Medium | ARB decision on UAE DR pattern; zone-redundant deployment as interim | Kenji Watanabe |
| R5 | Milestone latency degrades as EU volume is added | Low | High | Load test at 3x baseline before wave 5; Confluent cluster scaling | Amara Osei |
| R6 | Baltimore network re-termination slips, delaying DC exit | Medium | High | SD-WAN hub in Azure (STD-NET-011) procured by 2026-12 | Tomasz Nowak |
| R7 | Kestrel Digital Partners resource churn on migration squads | Medium | Medium | Key-person clauses in Architecture Contract G-01 | Grace Liu |

## 7. Decommissioning Plan

### 7.1 MuleSoft Anypoint ESB (APP-122)

- 2026-10-31: all flows classified as replaced, migrating, or to be retired without replacement.
- 2026-11-30: last production flow switched off; runtimes kept idle for rollback for 30 days.
- 2026-12-31: subscription terminated; CloudHub and on-prem runtimes deleted; CMDB records in ServiceNow (APP-110) closed.

### 7.2 FreightMaster TMS (APP-020) — both instances

- 2027-03-01: booking freeze on all remaining lanes.
- 2027-03-31: last open shipments migrated; application set to read-only; Oracle 12c instances shut down after final export.
- 2027-04 to 2027-05: closed shipment history loaded to Tidewater bronze/silver layers, with EU personal data to the West Europe workspace (STD-DAT-005); reconciliation signed off by Lena Vogel and the Customs Brokerage BU.
- By 2027-06-30: Baltimore servers wiped and disposed; Rotterdam host decommissioned.
- Q3 2027: formal retirement — licences, support contracts and CMDB entries closed; retirement recorded at ARB.

### 7.3 Baltimore Data Centre

- 2026-12: inventory confirmed; every remaining workload assigned to migrate, retire, or relocate. Terminal systems at BAL-T1 remain on the terminal edge per ADR-0027 and are not in scope.
- 2027-01 to 2027-05: remaining workloads moved; Windows Server 2012 R2 hosts removed.
- 2027-06-30: power-down, network circuits terminated, colocation contract ended; media destroyed with certificates retained 7 years.

### 7.4 Nordhaven TMS (APP-021)

After wave 6, Nordhaven TMS is read-only for 60 days, its MongoDB Atlas data is exported to the Tidewater West Europe workspace, Confluent cluster link and private link are removed, and the AWS account is closed.

## 8. Governance

Progress against this plan is reported to the ARB monthly and to the Horizon 2028 steering committee (chair: Elena Marsh) quarterly. Changes to transition dates or work package scope require a change request (`CR-YYYY-NNN`) assessed under Phase H.

## 9. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2025-02-20 | Grace Liu | Initial roadmap, TA1-TA3 |
| 2.0 | 2025-12-11 | Grace Liu | Re-baseline after TA1 go-live |
| 2.1 | 2026-04-09 | Samuel Adeyemi | Waves split for Rotterdam instance and Nordhaven |
| 2.2 | 2026-08-06 | Grace Liu | Canada freeze exception; R1 escalated; cost update |
