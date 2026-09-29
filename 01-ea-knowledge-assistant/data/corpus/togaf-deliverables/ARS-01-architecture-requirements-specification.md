---
doc_id: ARS-01
title: Architecture Requirements Specification — Shipment Platform
doc_type: togaf_deliverable
togaf_phase: Requirements
version: "1.2"
status: Approved
owner: Grace Liu, Programme Director, Horizon 2028 / HSP
approved_by: Architecture Review Board (ARB-2025-047)
effective_date: 2025-11-20
next_review: 2026-11-20
classification: Internal
related: [A-01, A-02, ADD-01, F-01, G-01, AP-01, AP-04, AP-06, AP-07, AP-08, AP-09, AP-14, STD-INT-001, STD-API-002, STD-EVT-003, STD-DAT-004, STD-DAT-005, STD-DB-006, STD-CLD-007, STD-IAM-008, STD-SEC-009, STD-OBS-010, STD-CTR-012, STD-RES-015, ADR-0030, ADR-0038, ADR-0041]
---

# ARS-01 — Architecture Requirements Specification — Shipment Platform

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This specification lists the requirements that the Harbourline Shipment Platform (HSP, APP-022) and its immediate integrations must satisfy. Each requirement is uniquely identified (`REQ-HSP-NNN`), prioritised using MoSCoW, traced to a source and to the principles and standards that govern it. Requirements are the acceptance baseline for the Architecture Contract (G-01) and the compliance checkpoints run by the ARB. The architecture that satisfies them is described in ADD-01; the sequence of delivery is in F-01.

## 2. Conventions

- **Priority:** M = Must, S = Should, C = Could, W = Won't (this release).
- **Source:** the stakeholder or document from which the requirement was elicited.
- **Verification:** T = test, D = demonstration, I = inspection, A = analysis.
- Requirements use MUST/SHOULD in the RFC 2119 sense. A requirement may be changed only through a change request (`CR-YYYY-NNN`) assessed in Phase H.

## 3. Functional Requirements

| ID | Requirement | Source | Priority | Verif. | Traceability |
|---|---|---|---|---|---|
| REQ-HSP-001 | HSP MUST provide a single booking service for ocean, air and road shipments used by all Harbourline legal entities. | Horizon 2028 goal 1; Michael Torres | M | D | AP-07, A-04 (Shipment Booking 2→4) |
| REQ-HSP-002 | HSP MUST be the system of record for shipment, booking and milestone data; no other system may accept writes to these entities after cutover of a lane. | ADD-01 §4.2 | M | I | AP-05, AP-07 |
| REQ-HSP-003 | HSP MUST publish `shipment.milestone.recorded.v1` for every recorded milestone using the transactional outbox. | Grace Liu; ADR-0038 | M | T | AP-08, STD-INT-001 INT-P1, STD-EVT-003 |
| REQ-HSP-004 | HSP MUST publish `shipment.status.changed.v1` carrying full current shipment status for consumer read models. | ADR-0030 | M | T | STD-INT-001 INT-P2 |
| REQ-HSP-005 | HSP MUST implement the harmonised 12-status shipment model and maintain mappings from FreightMaster and Nordhaven statuses until both are retired. | Lena Vogel | M | T | AP-07 |
| REQ-HSP-006 | HSP MUST exchange carrier bookings through partner APIs where the carrier supports them and through the B2B gateway (EDIFACT/X12) otherwise. | Carrier Management capability | M | T | STD-INT-001 INT-P3, INT-P4 |
| REQ-HSP-007 | HSP MUST make customs-relevant shipment data available to the Customs Filing Gateway (APP-060) by event subscription, not by database link. | ADD-01 gap G-07 | M | I | STD-INT-001 (prohibited patterns), AP-08 |
| REQ-HSP-008 | HSP MUST publish `shipment.charge.raised.v1` so that charges reach SAP S/4HANA Finance (APP-010) within 4 hours. | Rachel Kim | M | T | AP-08 |
| REQ-HSP-009 | HSP MUST reference customer accounts by Salesforce account ID and MUST NOT maintain its own customer master. | Data owner, Customer | M | I | AP-07 |
| REQ-HSP-010 | HSP SHOULD correlate container telemetry from CTS (APP-090) to shipments by container ID to derive reefer alerts. | Harbourline Digital | S | D | AP-01 |
| REQ-HSP-011 | HSP MUST receive terminal milestones (gate-in, load, discharge) from Navis N4 only through the IT/OT DMZ broker. | Tomasz Nowak | M | I | AP-13, RA-03, STD-NET-011 |
| REQ-HSP-012 | Booking data extracted by DocIntel (APP-130) MUST be confirmed by a human validator before customs-relevant fields are committed. | Priya Raman; AIU-004 | M | D | AP-16, STD-AI-013, ADR-0033 |
| REQ-HSP-013 | All synchronous HSP interfaces MUST be REST APIs described in OpenAPI 3.1 and published via the Harbourline API Gateway. | Amara Osei | M | I | AP-09, STD-API-002 |

## 4. Non-Functional Requirements

| ID | Requirement | Source | Priority | Verif. | Traceability |
|---|---|---|---|---|---|
| REQ-HSP-014 | End-to-end latency from milestone occurrence being recorded in HSP to availability in the Harbourline Connect read model MUST be **< 5 minutes at p95**, measured per calendar month, for at least 95% of shipments. | Horizon 2028 goal 2; A-01 KPI | M | T | AP-01, AP-08, AP-14, STD-EVT-003 |
| REQ-HSP-015 | HSP MUST meet service Tier 1: RTO 1 hour, RPO 15 minutes, zone-redundant deployment with paired-region DR, DR tested annually. | Kenji Watanabe | M | T | STD-RES-015 |
| REQ-HSP-016 | HSP MUST sustain 1,200 milestone events per second and 2,500 bookings per hour at peak without breaching REQ-HSP-014. | Capacity model (A-01) | M | T | AP-10 |
| REQ-HSP-017 | HSP query APIs SHOULD respond within 800 ms at p95 under peak load. | Harbourline Digital | S | T | STD-API-002 |
| REQ-HSP-018 | Every HSP service MUST emit OpenTelemetry traces, metrics and logs with W3C trace context, expose health endpoints and have published SLOs. Logs MUST NOT contain personal data or secrets. | Kenji Watanabe | M | I | AP-14, STD-OBS-010 |
| REQ-HSP-019 | Workforce access MUST use Entra ID with MFA; administrative access MUST use PIM just-in-time (≤ 8 hours); services MUST use managed identities. | Hannah Brennan | M | I | AP-12, STD-IAM-008 |
| REQ-HSP-020 | Restricted data MUST be encrypted at rest with customer-managed keys in Key Vault Premium; all traffic MUST use TLS 1.2 or higher. | Priya Raman | M | I | STD-DAT-004, STD-SEC-009 |
| REQ-HSP-021 | Personal data of EU data subjects MUST be stored and processed only in Azure **West Europe**, with North Europe as the DR region. | Marieke de Vries; GDPR | M | I | AP-06, STD-DAT-005 |
| REQ-HSP-022 | Canadian customer personal data MUST be stored in Canada Central/Canada East where a customer contract requires it. | Harbourline Canada legal | M | I | AP-06, STD-DAT-005 |
| REQ-HSP-023 | Personal data of UAE data subjects processed for Harbourline Gulf MUST be stored in UAE North. | Omar Haddad; UAE PDPL | M | I | AP-06, STD-DAT-005 |
| REQ-HSP-024 | Shipment records supporting customs filings MUST be retained for 7 years and be retrievable within 2 business days. | Customs Brokerage BU | M | D | AP-02 |
| REQ-HSP-025 | HSP SHOULD be deployable as independent regional stamps so that a new jurisdiction can be added without code change. | ADR-0041 | S | D | AP-06, AP-15 |

## 5. Constraints

| ID | Constraint | Source | Priority | Traceability |
|---|---|---|---|---|
| REQ-HSP-026 | HSP MUST run on AKS in the Azure landing zone (`hlg-online`) and use PostgreSQL Flexible Server as its relational store; Cosmos DB only with a Tier 2 partition-key review. | EA Office | M | STD-CTR-012, STD-DB-006, STD-CLD-007 |
| REQ-HSP-027 | HSP MUST NOT introduce MuleSoft flows, cross-domain database links or synchronous call chains deeper than 3 hops. | Amara Osei | M | STD-INT-001, ADR-0015 |
| REQ-HSP-028 | All HSP infrastructure MUST be provisioned with Terraform and deployed by Flux GitOps; resources MUST carry the five mandatory tags. | Kenji Watanabe | M | AP-15, STD-CLD-007 |
| REQ-HSP-029 | No HSP component or dependency MAY rely on the Baltimore data centre after 2027-06-30. | Horizon 2028 goal 3 | M | F-01 |

## 6. Assumptions

| ID | Assumption | Owner | Impact if false |
|---|---|---|---|
| REQ-HSP-030 | Navis N4 remains edge-hosted at each terminal (ADR-0027) and continues to emit milestones to the DMZ broker at current volumes. | Tomasz Nowak | Milestone ingestion redesign; REQ-HSP-014 at risk |
| REQ-HSP-031 | Salesforce remains the customer system of record for the life of the programme. | Elena Marsh | Customer master scope added to HSP |
| REQ-HSP-032 | Confluent Cloud dedicated cluster capacity can scale to 3x the 2025 baseline without re-architecture. | Amara Osei | Event backbone capacity work package required |

## 7. Requirement Change Log

| Version | Date | Change |
|---|---|---|
| 1.0 | 2025-02-20 | Initial baseline of functional, non-functional and constraint requirements |
| 1.1 | 2025-06-19 | Added REQ-HSP-003 outbox wording (ADR-0038); added REQ-HSP-028, -029 |
| 1.2 | 2025-11-20 | Added REQ-HSP-012 (DocIntel) and REQ-HSP-025; assumptions -030 to -032; table renumbered |
