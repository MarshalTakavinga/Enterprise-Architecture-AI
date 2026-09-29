---
doc_id: GOV-03
title: Glossary of Enterprise Architecture and Harbourline Terms
doc_type: governance
togaf_phase: Preliminary
version: "2.3"
status: Approved
owner: Samuel Adeyemi, Head of Enterprise Architecture Office / ARB Secretary
approved_by: Architecture Review Board (ARB-2026-006)
effective_date: 2026-02-12
next_review: 2027-02-12
classification: Internal
related: [GOV-01, GOV-02, AP-CATALOG, STD-TLC-014]
---

# GOV-03 — Glossary of Enterprise Architecture and Harbourline Terms

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This glossary gives the agreed meaning of architecture terms and Harbourline-specific names and acronyms used across the architecture repository. Where a term is defined more precisely in a standard, the standard prevails and is referenced. Definitions are written for Harbourline's use and are not quotations from any external framework.

## 2. Enterprise Architecture and Governance Terms

| Term | Definition |
|---|---|
| ADM (Architecture Development Method) | The phased cycle (Preliminary, A-H, plus Requirements Management) Harbourline uses to develop and govern architecture; tailored in GOV-01 §3. |
| ADR (Architecture Decision Record) | A short document recording one significant architecture decision, its options and consequences; numbered `ADR-NNNN`. |
| Architecture Building Block | A reusable, technology-neutral component of an architecture, such as "event backbone" or "API gateway". |
| Architecture Contract | A signed agreement between the EA Office and a delivery team on the architecture to be delivered and how compliance is checked; e.g., G-01 for HSP. |
| Architecture Definition Document (ADD) | The main Phase B-D deliverable describing baseline, target and gaps; for HSP, ADD-01. |
| Architecture Principle | A durable rule guiding design decisions; Harbourline's are AP-01 to AP-16 in AP-CATALOG. |
| Architecture Repository | The controlled store of all architecture documents, logs and models, structured per GOV-01 §11. |
| Architecture Requirements Specification (ARS) | The deliverable listing measurable requirements for an architecture; for HSP, ARS-01 with `REQ-HSP-NNN` IDs. |
| ARB (Architecture Review Board) | The governance body chaired by the Chief Architect that meets every Thursday to review designs and exceptions. |
| ARB log | The register of ARB decisions, each identified as `ARB-YYYY-NNN`. |
| Baseline Architecture | The architecture as it exists today. |
| Capability | An ability the business needs, independent of who or what performs it, such as Shipment Visibility; assessed for maturity 1-5 in A-04. |
| Change Request (CR) | A request to change an approved architecture, numbered `CR-YYYY-NNN`, handled in Phase H. |
| Compliance Assessment | A review of a solution against principles and standards at a gate, producing findings and a decision; e.g., G-02. |
| Dispensation | Synonym for exception. |
| Exception | Time-limited, approved permission to deviate from a standard clause, numbered `EXC-YYYY-NNN`; max 12 months, renewable once; recorded in GOV-02. |
| Gap Analysis | Comparison of baseline and target to identify what must be added, changed or removed. |
| RACI | Responsible, Accountable, Consulted, Informed — a matrix assigning roles to activities. |
| Request for Architecture Work | The sponsor's formal request that starts Phase A; for HSP, PRE-02. |
| Solution Building Block | A concrete product or service implementing an architecture building block, such as Confluent Cloud implementing the event backbone. |
| Stakeholder | A person or group with an interest in or influence over an architecture; mapped in A-03. |
| Standard | A mandatory, owned set of rules for a technology or practice area, numbered `STD-XXX-NNN`. |
| Statement of Architecture Work | The agreed scope, plan and acceptance criteria for architecture work; for HSP, A-02, signed 2024-12-02. |
| Target Architecture | The intended future-state architecture. |
| Technology Radar | The list of technologies classed Adopt, Trial, Contain or Retire, maintained under STD-TLC-014. |
| Tier 1 / 2 / 3 review | ARB review levels: full board, delegated to two domain architects, or self-certification. See GOV-01 §6. |
| Transition Architecture | An intermediate, stable state on the way to the target; HSP has TA1 (Nov 2025), TA2 (Q2 2027) and TA3 (Q4 2027). |
| Work Package | A unit of delivery work in the roadmap, numbered `WP-NN` in F-01. |

## 3. Radar Status Terms

| Term | Definition |
|---|---|
| Adopt | Approved default choice for new use. |
| Trial | Permitted for named use cases with ARB visibility, to gather evidence. |
| Contain | No new use; existing use may continue until a replacement is planned. |
| Retire | Removal date set; continued use after that date requires an exception. |

## 4. Integration, Data and Technology Terms

| Term | Definition |
|---|---|
| Claim-check pattern | Storing a large payload in Blob Storage and sending only a reference in the event, used for messages over 1 MB (STD-EVT-003). |
| Compacted topic | A Kafka topic retaining only the latest value per key, used to carry state. |
| CDC (Change Data Capture) | Reading database changes from the log; used with Debezium to publish HSP outbox events (ADR-0038). |
| Data Owner | The named business person accountable for a data domain or product (AP-05). |
| Data Product | A curated, owned dataset in Tidewater published for reuse (RA-04). |
| DLQ (Dead-Letter Queue) | A topic named `<topic>.dlq` holding messages a consumer could not process. |
| Event-Carried State Transfer | Integration pattern INT-P2, where events carry enough state for consumers to keep a local read model. |
| Idempotent consumer | A consumer that produces the same result if a message is processed more than once. |
| Medallion architecture | Bronze (raw), silver (cleaned), gold (business-ready) data layers in Tidewater. |
| Read model | A consumer-owned, query-optimised copy of another domain's data, never written back to the source. |
| Regional stamp | A complete, independently deployable copy of an application in one region, such as the EU stamp of Harbourline Connect (ADR-0041). |
| Restricted | The highest data classification in STD-DAT-004; requires customer-managed keys and PIM-controlled access. |
| RPO / RTO | Recovery Point Objective (maximum tolerable data loss) and Recovery Time Objective (maximum tolerable downtime), set by tier in STD-RES-015. |
| SCCs | Standard Contractual Clauses used as a transfer mechanism for personal data leaving the EU. |
| Service tier (0-3) | Resilience classification in STD-RES-015; Tier 0 is terminal operations. |
| SLO | Service Level Objective — a measurable reliability target for a service. |
| System of Record | The single authoritative source for a data domain (AP-07). |
| TIA (Transfer Impact Assessment) | Assessment of risks of a cross-border personal data transfer, approved by the DPO under STD-DAT-005. |
| Transactional outbox | Writing an event to an outbox table in the same transaction as the business change, then publishing it asynchronously. |

## 5. Security, Network and OT Terms

| Term | Definition |
|---|---|
| IEC 62443 | Industrial automation security standard series used for terminal OT zoning (STD-NET-011). |
| IT/OT DMZ | The Purdue level 3.5 zone through which all data between terminal OT and IT must pass. |
| OT (Operational Technology) | Systems that monitor or control physical equipment, such as gates and crane interfaces. |
| OT jump host | The only permitted path for remote vendor access to OT, with session recording and time-bound approval. |
| PIM | Entra Privileged Identity Management — just-in-time elevation, maximum 8 hours at Harbourline. |
| Purdue model | Layered reference model for industrial networks (levels 0-5) used to place terminal systems. |
| SD-WAN | Software-defined WAN; Fortinet Secure SD-WAN (FortiGate) at all sites since ADR-0036. |
| Zero Trust | Access model in which no request is trusted by network location (AP-12). |

## 6. Harbourline Names and Acronyms

| Term | Definition |
|---|---|
| AIU-NNN | ID of an entry in the AI Use Case Register (STD-AI-013), e.g., AIU-004 for DocIntel. |
| BAL-T1 / HFX-T1 / RTM-T2 / JEA-T4 | Harbourline's container terminals in Baltimore, Halifax, Rotterdam Maasvlakte and Jebel Ali. |
| CNS | Customer Notification Service (APP-055) — email, SMS and push shipment alerts. |
| CTS | Container Tracking Service (APP-090) — reefer and smart-container telemetry on IoT Hub and Cosmos DB. |
| DocIntel | Bill of lading extraction service (APP-130) using Azure AI Document Intelligence and Azure OpenAI with human validation. |
| EA Office | The central Enterprise Architecture team led by Samuel Adeyemi. |
| FreightMaster | Legacy in-house TMS (APP-020) on Oracle 12c; retiring by Q3 2027. |
| Harbourline API Gateway | Azure API Management Premium (APP-121), the single gateway for all APIs (ADR-0019). |
| Harbourline Connect | Customer portal, web and mobile (APP-050). |
| Harbourline Connect ID | Customer identity service on Entra External ID. |
| Harbourline Event Backbone | Confluent Cloud Kafka on Azure (APP-120), selected in ADR-0007. |
| HLG | Harbourline Logistics Group. |
| Horizon 2028 | Board-approved transformation programme (Nov 2024, USD 118M, four years). |
| HSP | Harbourline Shipment Platform (APP-022) — cloud-native target TMS and system of record for shipments. |
| INT-P1 to INT-P5 | Approved integration patterns in STD-INT-001. |
| Kestrel Digital Partners | System integrator delivering HSP under Architecture Contract G-01. |
| Nordhaven | Nordhaven Freight GmbH, Hamburg, acquired March 2024; its TMS is APP-021. |
| TMS | Transport Management System. |
| Tidewater | Tidewater Data Platform (APP-080) — Databricks lakehouse with Unity Catalog. |
| `hlgacr` | The Azure Container Registry from which all production images must be pulled (STD-CTR-012). |
| `hlg-*` management groups | Landing zone management groups: `hlg-platform`, `hlg-corp`, `hlg-online`, `hlg-sandbox` (STD-CLD-007). |

## 7. Regulatory and Customs Terms

| Term | Definition |
|---|---|
| ACE | US CBP Automated Commercial Environment, used for customs filing by APP-060. |
| CARM | Canada Border Services Agency Assessment and Revenue Management system. |
| EU AI Act | EU regulation on AI systems; EU-facing AI use cases require assessment under STD-AI-013. |
| GDPR / PIPEDA / UAE PDPL | Data protection laws of the EU, Canada and the UAE that drive STD-DAT-005. |
| ICS2 | EU Import Control System 2 for advance cargo information. |
| NIS2 | EU directive on network and information security; Harbourline Europe is an essential entity. |
| USCG cyber rule | US Coast Guard maritime cybersecurity rule, 33 CFR Part 101 Subpart F, effective July 2025. |

## 8. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 2.0 | 2024-12-05 | Samuel Adeyemi | Horizon 2028 terms added |
| 2.3 | 2026-02-12 | Samuel Adeyemi | AI, radar and residency terms updated with AP-CATALOG v4.0 |
