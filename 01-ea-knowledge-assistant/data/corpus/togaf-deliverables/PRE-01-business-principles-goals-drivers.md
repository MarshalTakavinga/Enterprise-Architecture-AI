---
doc_id: PRE-01
title: Business Principles, Goals and Drivers
doc_type: togaf_deliverable
togaf_phase: Preliminary
version: "1.2"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Elena Marsh, CIO; Architecture Review Board (ARB-2024-058)
effective_date: 2024-12-05
next_review: 2026-12-05
classification: Internal
related: [AP-CATALOG, GOV-01, PRE-02, A-01, A-04, F-01]
---

# PRE-01 — Business Principles, Goals and Drivers

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This deliverable records the business context that shapes Harbourline's architecture work: the external and internal drivers, the Board-approved Horizon 2028 goals, and the business principles from which the architecture principles in AP-CATALOG are derived. It is the reference point for Phase A of any Horizon 2028 initiative, beginning with PRE-02.

## 2. Business Context

Harbourline Logistics Group is headquartered in Baltimore, Maryland, employs about 9,400 people and generates roughly USD 4.2B in annual revenue across about 60 sites in 11 countries. It operates four business lines — Ocean & Air Forwarding, Port & Terminal Services, Contract Logistics & Warehousing, and Customs Brokerage — plus Harbourline Digital, which builds customer-facing products. It runs four container terminals: BAL-T1 (Baltimore), HFX-T1 (Halifax), RTM-T2 (Rotterdam Maasvlakte) and JEA-T4 (Jebel Ali).

The March 2024 acquisition of Nordhaven Freight GmbH in Hamburg added European road and ocean forwarding volume but also a third transport management system, hosted on AWS.

## 3. Business Drivers

### 3.1 External drivers

| ID | Driver | Description |
|---|---|---|
| D-01 | Customer expectations for real-time visibility | Large shippers now contract for milestone data within minutes; two tenders in 2024 were lost partly on visibility. |
| D-02 | Regulatory expansion | EU NIS2 designates Harbourline Europe an essential entity as a port operator; the US Coast Guard maritime cybersecurity rule (33 CFR Part 101 Subpart F) took effect in July 2025; EU ICS2 extends advance cargo filing. |
| D-03 | Data protection across jurisdictions | GDPR, Canada PIPEDA and UAE PDPL impose residency and transfer controls on customer and crew data. |
| D-04 | Margin pressure | Freight rates normalised after 2022; forwarding margins fell, putting IT cost under scrutiny. |
| D-05 | Cyber threat to ports | Ransomware incidents at other port operators demonstrated the operational impact of IT/OT compromise. |

### 3.2 Internal drivers

| ID | Driver | Description |
|---|---|---|
| D-06 | Fragmented shipment systems | FreightMaster TMS (APP-020), Nordhaven TMS (APP-021) and regional tools hold conflicting shipment records. |
| D-07 | Ageing on-premises estate | The Baltimore data centre hosts FreightMaster on Oracle 12c and Java 8, both approaching end of support. |
| D-08 | Integration debt | Over 300 MuleSoft flows in 2024, many point-to-point, created fragile dependencies. |
| D-09 | Acquisition integration | Nordhaven's platforms and processes must be absorbed without disrupting German customers. |

## 4. Horizon 2028 Business Goals

Approved by the Board in November 2024 with a budget of USD 118M over four years.

| Goal | Statement | Measure | Target date |
|---|---|---|---|
| G1 | Consolidate three TMS platforms into the Harbourline Shipment Platform (HSP) | Number of TMS in production | 1 by Q4 2027 |
| G2 | Real-time shipment and container visibility | % shipments with milestone events visible < 5 min latency | 95% |
| G3 | Exit the Baltimore on-premises data centre | Data centre closed | 30 June 2027 |
| G4 | Sustained regulatory compliance | Zero material findings from NIS2, USCG, GDPR/PIPEDA/PDPL and customs audits | Ongoing |
| G5 | Reduce IT run cost | Reduction versus FY2024 baseline of USD 96M | 18% by FY2028 |

## 5. Business Objectives

Goals are decomposed into objectives that architecture work must support:

- **OBJ-1:** Launch HSP for US lanes by November 2025 (supports G1, G3).
- **OBJ-2:** Migrate Nordhaven and EU lanes to HSP by Q2 2027 (G1).
- **OBJ-3:** Retire FreightMaster by Q3 2027 (G1, G3, G5).
- **OBJ-4:** Publish shipment milestones as events consumable by the customer portal and notification services (G2).
- **OBJ-5:** Decommission MuleSoft by 31 December 2026 (G5).
- **OBJ-6:** Demonstrate IEC 62443-aligned segmentation at all four terminals (G4).

## 6. Business Principles

The business principles below were agreed by the executive team and are elaborated as architecture principles in AP-CATALOG.

| Business principle | Meaning for Harbourline | Architecture principles |
|---|---|---|
| BP-1 Customer first | Customers see what we see about their cargo | AP-01 |
| BP-2 Licence to operate | Compliance and safety are non-negotiable | AP-02, AP-06, AP-13 |
| BP-3 Keep the quay moving | Terminals never stop because of IT | AP-04 |
| BP-4 One Harbourline | One process, one platform, one record per domain across entities | AP-03, AP-07 |
| BP-5 Spend where it differentiates | Buy commodity capability, build differentiation, run lean | AP-03, AP-10, AP-11 |
| BP-6 Trust through accountability | Named people own data, systems and AI-assisted decisions | AP-05, AP-16 |

## 7. Stakeholder Concerns

| Stakeholder | Primary concern |
|---|---|
| Elena Marsh, CIO | Delivery of Horizon 2028 on budget; data centre exit date |
| Rachel Kim, CFO | Run-cost reduction and billing accuracy |
| Michael Torres, VP Port & Terminal Services | Terminal uptime; no regression in gate throughput |
| Hannah Brennan, CISO | NIS2 and USCG compliance; OT risk |
| Marieke de Vries, DPO | Lawful processing and cross-border transfers |
| Grace Liu, Programme Director | Clear scope, fast decisions, stable standards |

## 8. Constraints Arising

- Terminal operating systems remain at the edge for continuity (later confirmed by ADR-0027).
- Azure is the primary cloud following the existing enterprise agreement; Nordhaven's AWS estate is transitional.
- EU personal data must remain in the EU.
- Programme funding is released in annual tranches subject to CFO review of benefits.

## 9. Use of This Document

Phase A deliverables (A-01, A-02) must trace every objective and KPI to a goal in §4. The capability assessment (A-04) prioritises capabilities that enable G1 and G2. Architecture principles that cannot be traced to a business principle in §6 are reviewed for removal at the next catalog revision.

## 10. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2024-09-12 | David Okafor | Initial draft for executive workshop |
| 1.1 | 2024-11-28 | David Okafor | Updated with Board-approved Horizon 2028 goals |
| 1.2 | 2024-12-05 | Samuel Adeyemi | Objectives OBJ-1 to OBJ-6 added; approved |
