---
doc_id: A-04
title: Business Capability Assessment — Horizon 2028 Shipment Platform
doc_type: togaf_deliverable
togaf_phase: A
version: "1.1"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Architecture Review Board (ARB-2025-004)
effective_date: 2025-01-24
next_review: 2026-01-24
classification: Internal
related: [A-01, A-02, A-03, ADD-01, ARS-01, F-01, PRE-01, AP-01, AP-02, AP-03, AP-04, AP-07, AP-16]
---

# A-04 — Business Capability Assessment — Horizon 2028 Shipment Platform

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This assessment establishes the capability baseline for the Shipment Platform Consolidation, sets target maturity levels aligned to the Horizon 2028 goals in A-01, and identifies the gaps that the architecture and the roadmap (F-01) must close. It is the bridge from Phase A into Phase B: the capability map below is the anchor for the business architecture in ADD-01 and for traceability of requirements in ARS-01.

## 2. Method

1. A Level 1 / Level 2 capability map was drafted from the existing Harbourline operating model and validated in six workshops (Baltimore, Rotterdam, Hamburg, Halifax, Dubai, virtual) between 2024-11-18 and 2025-01-10.
2. Each Level 2 capability in scope was scored for current maturity by business owners and architects jointly, using the five-level scale in §3. Where scores differed by more than one level, evidence (process documents, system reports, incident data) decided.
3. Target maturity was set by the sponsor's delegates against the goals and KPIs in A-01. Targets are for Q4 2027.
4. Strategic importance (High / Medium / Low) was taken from PRE-01 business drivers.

## 3. Maturity Scale

| Level | Name | Description |
|---|---|---|
| 1 | Ad hoc | Performed inconsistently; depends on individuals; largely manual |
| 2 | Repeatable | Performed consistently within a region or unit; multiple tools; limited data sharing |
| 3 | Defined | Standard process across regions; one primary system; measured periodically |
| 4 | Managed | Integrated, measured in near real time, exceptions managed proactively |
| 5 | Optimising | Self-service, predictive, continuously improved using data and automation |

## 4. Capability Map (L1 / L2)

| L1 Capability | L2 Capabilities |
|---|---|
| 1. Customer Management | 1.1 Account & Contract Management; 1.2 Quotation & Pricing; 1.3 Customer Self-Service |
| 2. Shipment Management | 2.1 Shipment Booking; 2.2 Shipment Planning & Routing; 2.3 Shipment Execution; 2.4 Shipment Visibility; 2.5 Exception Management |
| 3. Carrier & Partner Management | 3.1 Carrier Management; 3.2 Capacity Procurement; 3.3 Partner Connectivity |
| 4. Trade Compliance | 4.1 Customs Declaration; 4.2 Document Management; 4.3 Sanctions & Denied-Party Screening |
| 5. Terminal & Port Operations | 5.1 Terminal Operations; 5.2 Gate Management; 5.3 Container Condition Monitoring |
| 6. Warehousing & Fulfilment | 6.1 Inventory Management; 6.2 Order Fulfilment |
| 7. Financial Management | 7.1 Billing & Invoicing; 7.2 Cost Accrual & Settlement; 7.3 Financial Reporting |
| 8. Insight & Analytics | 8.1 Operational Reporting; 8.2 Performance Analytics |
| 9. Enterprise Support | 9.1 Identity & Access; 9.2 Master Data Management |

Capabilities 5.x and 6.x are outside the consolidation scope (A-02 §3) but are assessed at their interfaces because HSP depends on them.

## 5. Current vs Target Maturity

| L2 Capability | Importance | Current | Target | Gap | Primary systems today | Target system |
|---|---|---|---|---|---|---|
| 1.1 Account & Contract Management | Medium | 3 | 3 | 0 | Salesforce (APP-040) | Salesforce |
| 1.2 Quotation & Pricing | High | 2 | 4 | 2 | FreightMaster, spreadsheets, Nordhaven TMS | HSP rating service |
| 1.3 Customer Self-Service | High | 2 | 4 | 2 | Harbourline Connect (4-hour refresh) | Harbourline Connect on HSP events |
| 2.1 Shipment Booking | High | 2 | 4 | 2 | Three TMS; email bookings | HSP (APP-022) |
| 2.2 Shipment Planning & Routing | High | 2 | 4 | 2 | Three TMS; manual routing for cross-region | HSP |
| 2.3 Shipment Execution | High | 3 | 4 | 1 | Three TMS | HSP |
| 2.4 Shipment Visibility | High | 2 | 5 | 3 | Batch milestone export | HSP events, Event Backbone, Connect |
| 2.5 Exception Management | High | 1 | 4 | 3 | Email and phone | HSP exception workflow |
| 3.1 Carrier Management | High | 2 | 4 | 2 | Per-TMS carrier tables | HSP carrier domain |
| 3.2 Capacity Procurement | Medium | 2 | 3 | 1 | Spreadsheets, carrier portals | HSP allocations |
| 3.3 Partner Connectivity | Medium | 3 | 4 | 1 | IBM Sterling B2B, MuleSoft | Sterling (contained) then partner APIs via APIM |
| 4.1 Customs Declaration | High | 3 | 4 | 1 | Customs Filing Gateway (APP-060) fed by DB links | APP-060 fed by HSP events |
| 4.2 Document Management | Medium | 2 | 4 | 2 | Scanned documents, manual keying of bills of lading | Document store + assisted extraction |
| 4.3 Sanctions & Denied-Party Screening | High | 3 | 4 | 1 | Screening at booking in FreightMaster only | Screening service called by HSP for all lanes |
| 5.1 Terminal Operations | High | 4 | 4 | 0 | Navis N4 (APP-030) | Navis N4 (edge) |
| 5.2 Gate Management | Medium | 4 | 4 | 0 | Gate Automation (APP-031) | Unchanged |
| 5.3 Container Condition Monitoring | Medium | 3 | 4 | 1 | Container Tracking Service (APP-090) | CTS events to HSP |
| 7.1 Billing & Invoicing | High | 3 | 4 | 1 | TMS charges → nightly file → SAP | HSP charges → events/API → SAP |
| 7.2 Cost Accrual & Settlement | Medium | 2 | 4 | 2 | Manual accrual from carrier invoices | HSP cost events → SAP |
| 7.3 Financial Reporting | Medium | 4 | 4 | 0 | SAP S/4HANA (APP-010) | Unchanged |
| 8.1 Operational Reporting | Medium | 2 | 4 | 2 | Per-TMS reports | Tidewater gold products |
| 8.2 Performance Analytics | Medium | 2 | 4 | 2 | Quarterly spreadsheets | Tidewater (APP-080) |
| 9.2 Master Data Management | High | 2 | 4 | 2 | Customer, carrier and location data duplicated in three TMS | Single SoR per domain |

The six reference capabilities used in A-01 and in programme reporting are: Shipment Booking 2→4, Shipment Visibility 2→5, Customs Declaration 3→4, Terminal Operations 4→4, Carrier Management 2→4, and Billing & Invoicing 3→4.

## 6. Gap Analysis

### 6.1 Shipment Visibility (2 → 5)

The largest gap. Milestones exist in the TMS databases but reach customers only through a four-hour batch. Nordhaven customers see a different portal. Reaching level 5 requires event publication at source, a customer read model, proactive notifications and predictive ETA. Linked KPI: 95% of shipments with milestones visible in under 5 minutes.

### 6.2 Exception Management (1 → 4)

Exceptions (missed cut-offs, rolled bookings, customs holds) are handled by email and phone with no system record. Target requires exception events, assignment, and SLA tracking in HSP.

### 6.3 Shipment Booking, Planning and Quotation (2 → 4)

Three booking channels, three rating logics and email bookings for 38% of volume. Target: one booking API and UI, one rating engine, automated confirmation. Linked KPI: median booking confirmation < 15 minutes.

### 6.4 Carrier Management and Master Data (2 → 4)

Carrier contracts, SCAC codes and service levels are held separately in each TMS; 17% of carrier records conflict between systems. Target: HSP carrier domain as system of record (AP-07) with carrier performance scorecards from Tidewater.

### 6.5 Customs Declaration (3 → 4)

Filing is standardised through APP-060 and works, but it reads FreightMaster tables through database links, which will break when FreightMaster is retired. Target: APP-060 consumes shipment events from HSP. Filing to CBP ACE, EU ICS2 and CBSA CARM must not be interrupted during migration.

### 6.6 Document Management (2 → 4)

Bills of lading are keyed manually. An assisted-extraction capability is a candidate, subject to AP-16: a named human remains accountable for customs-relevant fields.

### 6.7 Billing & Invoicing and Cost Accrual (3 → 4, 2 → 4)

Billing works but relies on nightly files; 4.8% of invoices are adjusted. Accruals are manual. Target: charge and cost events from HSP to SAP within the same day.

### 6.8 Terminal Operations (4 → 4)

No maturity change is sought. The requirement is to preserve current maturity and the 72-hour autonomy of AP-04 while adding reliable event feeds from Navis N4 to HSP.

## 7. Prioritisation

Prioritisation combined gap size, strategic importance, and dependency (a capability that others depend on is scheduled earlier).

| Priority | Capabilities | Rationale | Transition |
|---|---|---|---|
| P1 | 2.1 Shipment Booking; 2.3 Shipment Execution; 9.2 Master Data (shipment, carrier, location); 3.1 Carrier Management | Foundation for all other capabilities; required for US lanes on HSP | TA1 (Nov 2025) |
| P1 | 2.4 Shipment Visibility (event publication, portal read model) | Highest-value customer outcome; A-01 headline KPI | TA1 core; level 5 features by TA3 |
| P2 | 1.2 Quotation & Pricing; 2.2 Planning & Routing; 7.1 Billing & Invoicing; 7.2 Cost Accrual | Needed before FreightMaster and Nordhaven lanes migrate | TA2 (Q2 2027) |
| P2 | 4.1 Customs Declaration re-integration; 4.3 Screening for all lanes | Hard dependency for FreightMaster retirement | TA2 |
| P3 | 2.5 Exception Management; 4.2 Document Management; 1.3 Self-Service booking | Improves efficiency after consolidation | TA2-TA3 |
| P3 | 8.1 / 8.2 Analytics; 3.2 Capacity Procurement; 3.3 Partner APIs | Benefits realisation and optimisation | TA3 (Q4 2027) |
| Hold | 5.x, 6.x, 7.3, 1.1 | No change in scope; interface work only | — |

## 8. Implications for Later Phases

1. ADD-01 business architecture MUST use this capability map as its structuring view.
2. Every requirement in ARS-01 MUST trace to at least one L2 capability in §5.
3. F-01 work packages MUST be sequenced consistent with §7; deviations require ARB approval.
4. Capability maturity will be re-scored at each transition architecture gate and reported to the steering committee (A-03).

## 9. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2025-01-17 | David Okafor | Workshop results consolidated |
| 1.1 | 2025-01-24 | Samuel Adeyemi | ARB approval (ARB-2025-004) recorded |
