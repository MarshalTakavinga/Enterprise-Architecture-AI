---
doc_id: A-01
title: Architecture Vision — Horizon 2028 Shipment Platform
doc_type: togaf_deliverable
togaf_phase: A
version: "1.1"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Elena Marsh, CIO (Architecture Board decision ARB-2024-058)
effective_date: 2024-11-28
next_review: 2025-11-28
classification: Internal
related: [PRE-01, PRE-02, A-02, A-03, A-04, ADD-01, ARS-01, F-01, GOV-01, AP-01, AP-02, AP-04, AP-06, AP-07, AP-08, AP-10, STD-INT-001, STD-DAT-005, STD-RES-015, ADR-0007, ADR-0015, ADR-0021, ADR-0024, ADR-0027]
---

# A-01 — Architecture Vision — Horizon 2028 Shipment Platform

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Document Purpose

This Architecture Vision sets out, at summary level, why Harbourline is replacing its three transport management systems with a single Harbourline Shipment Platform (HSP), what the target looks like, what value it must deliver and how that value will be measured. It responds to the Request for Architecture Work PRE-02 (sponsor Elena Marsh, 2024-10-07) and is the reference against which later phases (ADD-01, ARS-01, F-01) are checked for alignment. It was presented alongside the Horizon 2028 investment case that the Board approved in November 2024.

## 2. Problem Statement

Harbourline runs its core freight business on three transport management systems that were never designed to work together:

- **FreightMaster TMS (APP-020)** — built in-house from 2009, Oracle 12c and Java 8, hosted in the Baltimore data centre, used by Harbourline Inc., Harbourline Canada and Harbourline Gulf.
- **Nordhaven TMS (APP-021)** — inherited with the March 2024 acquisition of Nordhaven Freight GmbH, running on AWS eu-central-1 with MongoDB Atlas and Java 11.
- **FreightMaster Rotterdam instance** — a 2019 fork of APP-020 with its own Oracle 12c schema in the Rotterdam server room, used by Harbourline Europe B.V. and coupled to the Baltimore instance for cross-region shipments.

The three systems, SAP, Salesforce and the customs gateway are held together by 310 MuleSoft flows (APP-122) and a number of direct database links.

The consequences are visible to customers and to the finance function:

1. Shipment status reaches customers in batches. FreightMaster exports milestones every four hours; only 31% of shipments show a milestone to the customer within five minutes of it occurring.
2. A shipment moving from Hamburg to Baltimore is re-keyed between Nordhaven TMS and FreightMaster. Operations staff estimate 11,000 hours a year of duplicate entry.
3. Oracle 12c reaches end of extended support in 2027 and Java 8 in 2026; FreightMaster cannot be modernised in place without a near-total rewrite.
4. The Baltimore data centre lease ends in mid-2027 and renewal would require a USD 7.4M facility refresh.
5. Integration is brittle: in FY2024, 42% of Severity 1 incidents on customer-facing services originated in MuleSoft flows or point-to-point database links.
6. Regulatory scope is growing. Harbourline Europe is an essential entity under NIS2, and the US Coast Guard maritime cybersecurity rule applies to BAL-T1 from July 2025. Evidencing control over three TMS platforms with different security models is costly.

## 3. Business Goals and Drivers

| # | Business goal (from PRE-01) | Driver | Architecture response |
|---|---|---|---|
| G1 | One shipment platform for all lanes by Q4 2027 | Duplicate entry, inconsistent customer experience, acquisition integration | HSP as system of record for shipments (AP-07) |
| G2 | Real-time visibility for customers | Customer churn in mid-market accounts; competitor portals | Event-first milestone publication (AP-01, AP-08) |
| G3 | Exit Baltimore DC by 30 June 2027 | Lease expiry; facility refresh cost | Cloud-native build on Azure (AP-10, AP-11) |
| G4 | Compliance by design across five jurisdictions | NIS2, GDPR, PIPEDA, UAE PDPL, 33 CFR Part 101 Subpart F, CBP ACE, ICS2 | Regional data placement (AP-06), common controls (AP-02) |
| G5 | Reduce IT run cost 18% by FY2028 | Margin pressure in forwarding | Retire three TMS stacks, MuleSoft and DC hosting |

## 4. Stakeholders and Concerns

The full map is in A-03. The concerns that shape this Vision are:

| Stakeholder | Principal concern | How the Vision addresses it |
|---|---|---|
| Elena Marsh, CIO (sponsor) | Delivering G1-G5 within USD 118M | Phased transition architectures, KPI tracking |
| Rachel Kim, CFO | Run-cost reduction and billing accuracy | Decommissioning plan, single rating engine |
| Michael Torres, VP Port & Terminal Services | Terminal operations must not become cloud-dependent | Navis N4 remains at the edge (ADR-0027, AP-04) |
| Hannah Brennan, CISO | One security model; regulator evidence | Zero Trust, standard landing zone |
| Marieke de Vries, DPO | EU personal data residency and transfers | West Europe processing (AP-06, STD-DAT-005) |
| Grace Liu, Programme Director | Scope stability, clear acceptance criteria | A-02 scope and acceptance procedures |
| Omar Haddad, Head of IT Gulf | Gulf lanes not treated as an afterthought | Gulf lanes included in TA2 planning |

## 5. Vision Statement

> By the end of 2027, every Harbourline shipment — ocean, air or road, in any region — is booked, executed, tracked and billed on one cloud-native platform, and every customer can see what is happening to their freight within minutes of it happening, with their data held where their law requires.

## 6. Value Propositions and KPIs

| Value proposition | Stakeholder | KPI | Baseline (FY2024) | Target | Date |
|---|---|---|---|---|---|
| Customers see milestones in near real time | Customers, Harbourline Digital | % shipments with milestone events visible < 5 min (p95) | 31% | 95% | Q4 2027 |
| One booking, no re-keying | Operations | Duplicate-entry hours per year | ~11,000 | < 500 | Q4 2027 |
| Faster booking | Customers, Sales | Median booking confirmation time | 3.2 h | < 15 min | Q2 2027 |
| Lower run cost | CFO | IT run cost (USD) | 96M | ≤ 78.7M (−18%) | FY2028 |
| Simpler estate | CIO | Transport management systems in production | 3 | 1 | Q4 2027 |
| Retire legacy integration | CIO, Integration | Active MuleSoft flows | 310 | 0 | 2026-12-31 |
| Fewer integration outages | Customers, Operations | Sev 1 incidents from integration per year | 26 | ≤ 8 | FY2028 |
| Accurate billing | CFO | Invoice adjustments as % of invoices | 4.8% | ≤ 1.5% | FY2028 |
| Evidence-ready compliance | CISO, DPO | Open high audit findings on TMS estate | 9 | 0 | Q4 2027 |

KPI data will be sourced from Tidewater (APP-080) and reported monthly by the Programme Office.

## 7. Baseline Architecture Summary

- **Business:** separate booking and operations procedures per legal entity; manual hand-offs for cross-region shipments; customer status via email and a portal refreshed every four hours.
- **Data:** shipment records held in three stores (Oracle 12c, MongoDB Atlas, regional SQL Server databases); no agreed system of record; customer master in Salesforce but duplicated in each TMS.
- **Application:** FreightMaster (Baltimore and Rotterdam instances), Nordhaven TMS; Customs Filing Gateway (APP-060) integrated to FreightMaster by database link; SAP S/4HANA Finance (APP-010) fed by nightly files.
- **Technology:** Baltimore on-premises data centre; AWS eu-central-1 for Nordhaven; MuleSoft ESB; early Azure landing zone; MPLS WAN being replaced by SD-WAN (ADR-0036).

## 8. Target Architecture Summary

- **Business:** one global shipment lifecycle process with regional variants only where regulation requires; customers self-serve bookings and tracking in Harbourline Connect (APP-050).
- **Data:** HSP is the system of record for shipments (AP-07); Salesforce remains the system of record for customer accounts; EU personal data processed in West Europe, Canadian in Canada Central where contracted, US in East US 2 (STD-DAT-005); analytics in Tidewater.
- **Application:** HSP (APP-022) as microservices on AKS, each domain owning its PostgreSQL database (ADR-0024); integration via the Harbourline Event Backbone (APP-120, ADR-0007) and the Harbourline API Gateway (APP-121); partner EDI via APP-123 until partner APIs mature.
- **Technology:** Azure primary in approved regions; AWS only for Nordhaven until migration (ADR-0021); terminals retain edge-hosted Navis N4 (ADR-0027) and publish events outward.

Transition architectures are summarised here and detailed in F-01:

| Transition | Target date | Outcome |
|---|---|---|
| TA1 | November 2025 | US lanes live on HSP; milestones published as events |
| TA2 | Q2 2027 | Nordhaven migrated; EU lanes live; EU stamp in West Europe |
| TA3 / Target | Q4 2027 | FreightMaster retired; Baltimore DC exited (by June 2027) |

## 9. Scope

**In scope:** shipment booking, rating, execution, milestone tracking, carrier management, billing hand-off to SAP, and customs data hand-off to APP-060 for Ocean & Air Forwarding and Customs Brokerage in all five legal entities; customer-facing visibility via Harbourline Connect; decommissioning of FreightMaster (both instances), Nordhaven TMS and MuleSoft.

**Out of scope:** Navis N4 replacement; warehouse management (APP-070); SAP S/4HANA Finance changes other than new interfaces; CRM replacement.

## 10. Constraints

1. Total programme budget USD 118M over FY2025-FY2028.
2. Baltimore DC exit no later than 30 June 2027.
3. MuleSoft contract ends 2026-12-31; no new flows after 2025-06-30 (ADR-0015).
4. Terminal operations must survive 72 hours without WAN or cloud (AP-04).
5. Personal data residency per STD-DAT-005; any cross-border transfer requires a DPO-approved TIA.
6. HSP is a Tier 1 service: RTO 1 h, RPO 15 min (STD-RES-015).
7. Peak season freeze from mid-October to mid-January: no cutovers of live lanes.

## 11. Key Risks and Mitigations

| ID | Risk | Likelihood / Impact | Mitigation | Owner |
|---|---|---|---|---|
| R1 | Nordhaven data model differs more than assessed, delaying TA2 | Medium / High | Data mapping spike in Phase C; keep Nordhaven on AWS under exception until migration | Lena Vogel |
| R2 | FreightMaster business rules undocumented | High / High | Rule-harvesting workstream; parallel run for each lane group | Grace Liu |
| R3 | DC exit date slips because of residual workloads | Medium / High | Early inventory; ARB tracks non-HSP workloads monthly | Kenji Watanabe |
| R4 | Customer-facing latency target missed due to polling-style integrations | Medium / Medium | Event-first standard and ARB compliance reviews | Amara Osei |
| R5 | Regulatory change (NIS2 transposition, UAE PDPL) alters residency needs | Medium / Medium | Regional stamp design allows new regions | Marieke de Vries |
| R6 | Systems integrator capacity or skill shortfall | Medium / High | Architecture Contract with delivery partner (G-01); internal platform team | Elena Marsh |
| R7 | Security incident during migration exposes dual-running data | Low / High | Zero Trust controls; restricted-data masking in non-prod | Hannah Brennan |

## 12. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Executive Sponsor | Elena Marsh, CIO | Approved | 2024-11-28 |
| Chief Architect / ARB Chair | David Okafor | Approved (ARB-2024-058) | 2024-11-28 |
| Business representative | Michael Torres, VP Port & Terminal Services | Endorsed | 2024-11-26 |
| Finance | Rachel Kim, CFO | Endorsed | 2024-11-26 |
| CISO | Hannah Brennan | Endorsed with note on R7 | 2024-11-27 |

## 13. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.9 | 2024-11-08 | David Okafor | Draft for stakeholder review |
| 1.0 | 2024-11-21 | David Okafor | KPI baselines confirmed by Finance |
| 1.1 | 2024-11-28 | Samuel Adeyemi | Approval record added |
