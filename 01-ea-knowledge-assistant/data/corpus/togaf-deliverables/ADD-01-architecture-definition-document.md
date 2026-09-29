---
doc_id: ADD-01
title: Architecture Definition Document — Shipment Platform
doc_type: togaf_deliverable
togaf_phase: B-D
version: "1.4"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Architecture Review Board (ARB-2025-047)
effective_date: 2025-11-20
next_review: 2026-11-20
classification: Internal
related: [A-01, A-02, A-04, ARS-01, F-01, G-01, AP-01, AP-04, AP-06, AP-07, AP-08, AP-10, STD-INT-001, STD-EVT-003, STD-DAT-005, STD-DB-006, STD-CLD-007, STD-RES-015, ADR-0007, ADR-0015, ADR-0021, ADR-0024, ADR-0027, ADR-0030, ADR-0038, ADR-0041, RA-01, RA-02, RA-03, RA-04]
---

# ADD-01 — Architecture Definition Document — Shipment Platform

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose and Scope

This document defines the baseline and target architectures for shipment management at Harbourline Logistics Group across the business, data, application and technology domains, and records the gaps that the Horizon 2028 programme must close. It is the architectural basis for the Harbourline Shipment Platform (HSP, APP-022) and is read together with the Architecture Requirements Specification (ARS-01), which holds the testable requirements, and the Architecture Roadmap & Migration Plan (F-01), which sequences the work packages named in the gap analysis.

In scope: shipment booking, planning, execution, milestone visibility, carrier interaction, customs data hand-off and charge capture for all five business units and all legal entities. Out of scope: terminal operations inside Navis N4 (APP-030), warehouse execution (APP-070) and general ledger processes (APP-010), except where they exchange data with shipment management.

The scope, stakeholders and acceptance criteria were agreed in the Statement of Architecture Work (A-02, signed 2024-12-02). The value case and KPIs are in the Architecture Vision (A-01).

## 2. Architecture Drivers

| Driver | Source | Architectural consequence |
|---|---|---|
| Consolidate three TMS into one by Q4 2027 | Horizon 2028 goal 1 | Single system of record for shipments (AP-07) |
| 95% of shipments with milestone events < 5 min latency | Horizon 2028 goal 2; REQ-HSP-014 | Event-first integration (AP-08), no polling or overnight batch |
| Exit Baltimore data centre by 2027-06-30 | Horizon 2028 goal 3 | All shipment workloads on Azure landing zone (STD-CLD-007) |
| NIS2, GDPR, PIPEDA, UAE PDPL, customs filing obligations | Horizon 2028 goal 4 | Regional data placement (AP-06, STD-DAT-005), Tier 1 resilience |
| 18% IT run-cost reduction by FY2028 | Horizon 2028 goal 5 | Retire Oracle, MuleSoft and duplicated TMS licences |

## 3. Business Architecture

### 3.1 Baseline

Shipment management is fragmented by legal entity. Harbourline Inc., Harbourline Canada and Harbourline Gulf book and execute shipments in FreightMaster TMS (APP-020) in the Baltimore data centre. Harbourline Europe B.V. uses a separate FreightMaster instance (the "Rotterdam instance", a 2019 fork of APP-020 with its own Oracle 12c schema hosted in the Rotterdam server room). Nordhaven Freight GmbH, acquired in March 2024, runs Nordhaven TMS (APP-021) on AWS eu-central-1. The three systems use different shipment status models (FreightMaster has 14 statuses, Nordhaven 22), so the same shipment moving from Hamburg to Baltimore is re-keyed at the hand-over point.

Customer service agents answer an estimated 38% of inbound contacts with "where is my shipment?" questions because milestone updates reach Harbourline Connect (APP-050) only through nightly MuleSoft batches.

### 3.2 Target

One set of shipment processes, owned by the Ocean & Air Forwarding business unit and used by every entity, with local variants limited to customs and tax rules. The capability targets from the Business Capability Assessment (A-04) apply: Shipment Booking maturity 2→4, Shipment Visibility 2→5, Carrier Management 2→4, Customs Declaration 3→4, Billing & Invoicing 3→4. Terminal Operations stays at 4 and is deliberately not re-platformed.

### 3.3 Business Process Changes

| Process | Baseline | Target |
|---|---|---|
| Book shipment | Three booking screens, manual rekey across entities | Single HSP booking service; Connect self-service booking via API |
| Track shipment | Nightly batch to portal; phone and email enquiries | Near-real-time milestones pushed to Connect and CNS (APP-055) |
| Book carrier capacity | EDI via Sterling plus email for smaller carriers | Partner APIs for top carriers; EDI (INT-P4) retained for the long tail |
| Hand off customs data | FreightMaster writes directly into Customs Filing Gateway tables | HSP publishes events consumed by APP-060 |
| Raise charges | Weekly extract to SAP | Charge events to SAP S/4HANA within the day |

## 4. Data Architecture

### 4.1 Baseline

Shipment, party and charge data exist in three physical models. FreightMaster uses Oracle 12c (Retire by 2027-03-31, extended support under EXC-2026-001). Nordhaven TMS uses MongoDB Atlas. Customer accounts are copied from Salesforce (APP-040) into each TMS monthly, producing an estimated 11% duplicate party records. Customs Filing Gateway reads FreightMaster tables through a cross-domain database link, a pattern now prohibited by STD-INT-001.

Gulf shipment data containing personal data of UAE data subjects is stored in Baltimore under a transfer impact assessment approved by the DPO in 2024.

### 4.2 Target

| Data domain | System of record | Store | Placement |
|---|---|---|---|
| Shipment, booking, milestone | HSP (APP-022) | PostgreSQL Flexible Server (ADR-0024) | Regional: East US 2, West Europe, Canada Central, UAE North |
| Customer account | Salesforce (APP-040) | SaaS | Referenced by account ID only |
| Container telemetry | CTS (APP-090) | Cosmos DB (ADR-0012) | Correlated to shipments by container ID |
| Charges and invoices | SAP S/4HANA (APP-010) | SAP HANA | East US 2 |
| Analytical shipment history | Tidewater (APP-080) | Delta Lake, Unity Catalog | East US 2; EU personal data in West Europe workspace (RA-04) |

Key rules applied: each data domain has one system of record and a named owner (AP-05, AP-07); personal data of EU data subjects is held in West Europe with North Europe as DR (AP-06, STD-DAT-005; REQ-HSP-021); shipment records containing customs declarations with personal data are classified Restricted and encrypted with customer-managed keys (STD-DAT-004, STD-SEC-009). Events carry business state, not raw personal data, unless field-level encrypted (STD-EVT-003).

### 4.3 Canonical Events

The target publishes `shipment.booking.confirmed.v1`, `shipment.milestone.recorded.v1`, `shipment.status.changed.v1` and `shipment.charge.raised.v1` to the Harbourline Event Backbone (APP-120) using Avro schemas in Schema Registry with BACKWARD compatibility. The status model is reduced to 12 harmonised statuses.

## 5. Application Architecture

### 5.1 Baseline

| Application | Role | Integration |
|---|---|---|
| FreightMaster TMS (APP-020), two instances | Booking, execution, charges | MuleSoft flows, DB links, Sterling EDI |
| Nordhaven TMS (APP-021) | Booking, execution for Nordhaven | REST to MuleSoft; Confluent cluster linking (ADR-0021) |
| MuleSoft Anypoint ESB (APP-122) | ~140 flows remaining, sunset 2026-12-31 | Hub for portal, SAP, customs feeds |
| IBM Sterling B2B (APP-123) | Carrier and broker EDI | EDIFACT/X12 |
| Harbourline Connect (APP-050) | Customer portal | Nightly batch feed |

### 5.2 Target

HSP is a set of domain microservices (booking, planning, execution, milestone, charge, partner) on AKS following RA-02. Each service owns its PostgreSQL schema and publishes domain events through the transactional outbox and managed Debezium CDC (ADR-0038, INT-P1). Consumers maintain their own read models: Harbourline Connect per ADR-0030 (INT-P2), the Customer Notification Service, Customs Filing Gateway and Tidewater. Synchronous queries and commands use REST APIs published through the Harbourline API Gateway (APP-121, STD-API-002), with call chains of no more than three hops. Carrier connectivity uses partner APIs where carriers support them and Sterling EDI (INT-P4) otherwise. Terminal milestones leave Navis N4 through the IT/OT DMZ broker described in RA-03; HSP never calls into OT zones.

AI-assisted bill of lading extraction (DocIntel, APP-130, AIU-004) feeds HSP booking data only after a human validator confirms customs-relevant fields (ADR-0033, AP-16).

## 6. Technology Architecture

### 6.1 Baseline

Baltimore data centre: Oracle 12c RAC on Linux, Java 8 application servers, Windows Server 2012 R2 file transfer hosts. Rotterdam server room: single Oracle 12c host with nightly backup to tape. AWS eu-central-1 for Nordhaven. Integration through MuleSoft CloudHub and on-prem runtimes.

### 6.2 Target

| Layer | Target technology | Governing standard |
|---|---|---|
| Hosting | Azure landing zone, `hlg-online` management group, regional stamps | STD-CLD-007, RA-02 |
| Compute | AKS (private cluster), Azure Container Apps for simple consumers | STD-CTR-012 |
| Database | PostgreSQL Flexible Server, zone-redundant HA | STD-DB-006 |
| Eventing | Confluent Cloud on Azure | STD-EVT-003, ADR-0007 |
| APIs | Azure API Management Premium | STD-API-002, ADR-0019 |
| Identity | Entra ID, managed identities, Connect ID for customers | STD-IAM-008 |
| Keys | Key Vault Premium, customer-managed keys for Restricted data | STD-SEC-009 |
| Observability | OpenTelemetry to Azure Monitor and Grafana | STD-OBS-010 |
| Resilience | Tier 1: RTO 1 h, RPO 15 min, multi-zone plus paired-region DR | STD-RES-015 |
| IaC | Terraform, Flux GitOps | AP-15 |

AWS remains in the picture only for Nordhaven TMS until its migration, under EXC-2025-003 and ADR-0021.

## 7. Gap Analysis

Gap types: **New** (target element with no baseline equivalent), **Eliminated** (baseline element with no target equivalent), **Changed** (element carried forward in altered form). Work packages are defined in F-01.

| # | Baseline element | Target element | Gap type | Resolving work package |
|---|---|---|---|---|
| G-01 | — | HSP core services on AKS, PostgreSQL | New | WP-01 |
| G-02 | FreightMaster NA (US lanes) | HSP US stamp (East US 2) | Changed | WP-02 |
| G-03 | MuleSoft flows for shipment status | Event Backbone topics via outbox/CDC | Changed | WP-03 |
| G-04 | MuleSoft ESB (APP-122) | — | Eliminated | WP-03 |
| G-05 | Nightly batch to Connect | Event-carried state read model (ADR-0030) | Changed | WP-04 |
| G-06 | — | Harmonised 12-status shipment model | New | WP-01 |
| G-07 | DB link FreightMaster → Customs Filing Gateway | Event subscription by APP-060 | Changed | WP-05 |
| G-08 | Nordhaven TMS (APP-021) on AWS | HSP EU stamp (West Europe) | Eliminated / Changed | WP-06 |
| G-09 | FreightMaster Rotterdam instance | HSP EU stamp (West Europe) | Eliminated | WP-06 |
| G-10 | FreightMaster NA (Canada, Gulf lanes) | HSP CA and UAE North data cells | Changed | WP-07 |
| G-11 | Monthly customer copies in each TMS | Account reference to Salesforce | Changed | WP-01 |
| G-12 | Oracle 12c schemas (both instances) | Archived history in Tidewater | Eliminated | WP-08 |
| G-13 | Baltimore DC hosting | Azure landing zone | Eliminated | WP-09 |
| G-14 | Email-based carrier booking | Partner APIs via API Gateway | New | WP-10 |
| G-15 | Sterling EDI for all carriers | Sterling EDI for long-tail carriers only | Changed | WP-10 |
| G-16 | Weekly charge extract to SAP | `shipment.charge.raised.v1` consumed by SAP integration | Changed | WP-03 |

Gaps G-08 and G-12 carry the highest delivery risk; see F-01 §6.

## 8. Building Blocks

### 8.1 Architecture Building Blocks

| ABB | Description | Principles |
|---|---|---|
| Shipment System of Record | Authoritative store of shipment, booking and milestone state | AP-05, AP-07 |
| Domain Event Publication | Reliable publication of business facts consistent with state changes | AP-08 |
| Customer Read Model | Consumer-owned projection of shipment state | AP-01, AP-08 |
| Managed API Access | Governed synchronous access for internal and partner consumers | AP-09, AP-12 |
| Regional Data Cell | Deployment unit keeping personal data in its jurisdiction | AP-06 |
| Edge Autonomy Boundary | Separation guaranteeing terminal operations survive cloud loss | AP-04, AP-13 |

### 8.2 Solution Building Blocks

| SBB | Realises ABB | Product / pattern |
|---|---|---|
| HSP shipment services | Shipment System of Record | .NET 8 and Java 21 services on AKS, PostgreSQL Flexible Server |
| Outbox + Debezium CDC | Domain Event Publication | ADR-0038, Confluent managed connector |
| Connect read model | Customer Read Model | ADR-0030, PostgreSQL per stamp |
| Harbourline API Gateway | Managed API Access | Azure API Management Premium |
| Regional stamp | Regional Data Cell | RA-02 stamp, Front Door routing (ADR-0041) |
| Terminal DMZ broker | Edge Autonomy Boundary | RA-03 one-way replication, ADR-0027 |

## 9. Architectural Risks and Open Issues

1. Nordhaven data migration requires mapping 22 statuses to 12; unmapped statuses block EU lane cutover. Owner: Lena Vogel.
2. The UAE North data cell has no approved paired region in STD-CLD-007; DR design is subject to ARB decision. Owner: Kenji Watanabe.
3. Customs Filing Gateway must support both the DB link and event subscription during migration; dual-running is limited to 90 days per lane. Owner: Amara Osei.

## 10. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2025-02-20 | David Okafor | Baseline and target approved at ARB |
| 1.1 | 2025-04-24 | Amara Osei | Added canonical events and ADR-0030 read model |
| 1.2 | 2025-05-15 | Lena Vogel | Regional data cells; Rotterdam instance gaps |
| 1.3 | 2025-06-19 | Amara Osei | Outbox publication per ADR-0038 |
| 1.4 | 2025-11-20 | Samuel Adeyemi | DocIntel (ADR-0033); regional stamps per ADR-0041; gap table aligned to F-01 |
