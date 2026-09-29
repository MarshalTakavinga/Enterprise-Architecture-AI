---
doc_id: STD-INT-001
title: Integration Patterns Standard
doc_type: standard
togaf_phase: Preliminary
version: "2.1"
status: Approved
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2025-012)
effective_date: 2025-03-01
next_review: 2026-12-01
classification: Internal
related: [AP-07, AP-08, AP-09, AP-03, STD-API-002, STD-EVT-003, STD-TLC-014, ADR-0007, ADR-0015, ADR-0030, ADR-0038, RA-01, GOV-01, GOV-02]
---

# STD-INT-001 — Integration Patterns Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines the integration patterns that Harbourline Logistics Group ("Harbourline") solutions MAY use to exchange data between applications, domains and external partners, and the patterns that are prohibited. It exists so that the Horizon 2028 target state — one Harbourline Shipment Platform (HSP, APP-022), real-time customer visibility and the retirement of MuleSoft Anypoint (APP-122) — is not undermined by new tactical point-to-point integrations.

Solution architects MUST select one of the approved patterns in §4 for every integration flow and record the selection in the solution design submitted to the Architecture Review Board (ARB).

## 2. Scope

### 2.1 In scope

- All integrations between Harbourline applications owned by different business domains (for example Shipment, Customs, Terminal, Customer, Finance, Warehouse).
- Integrations with external parties: carriers, customs brokers, port community systems, customers and government customs platforms.
- Integrations built by Harbourline staff, Harbourline Digital, and delivery partners working under an architecture contract (for example G-01).

### 2.2 Out of scope

- Calls between microservices *inside* a single bounded context owned by one team (these follow team conventions, but STD-API-002 and STD-OBS-010 still apply).
- Analytical data sharing *within* the Tidewater Data Platform (APP-080), which is governed by RA-04.
- OT-level protocols inside terminal control zones (governed by STD-NET-011 and RA-03).

## 3. Related Principles and Normative References

| Reference | Relevance |
|---|---|
| AP-08 Event-First Integration Between Domains | Primary driver for INT-P1 and INT-P2 |
| AP-09 API-First for Synchronous Access | Primary driver for INT-P3 |
| AP-07 One System of Record per Data Domain | Basis for prohibiting shared databases |
| AP-03 Reuse, then Buy, then Build | Reuse of the Event Backbone and API Gateway before any new middleware |
| STD-API-002 | Detailed API design rules for INT-P3 |
| STD-EVT-003 | Topic, schema and consumer rules for INT-P1 and INT-P2 |
| STD-TLC-014 | Radar statuses for MuleSoft Anypoint and IBM Sterling B2B |
| ADR-0007, ADR-0015, ADR-0038 | Event Backbone adoption, MuleSoft sunset, transactional outbox |
| RA-01 | Reference implementation of INT-P1/INT-P2/INT-P3 |

The key words "MUST", "MUST NOT", "SHOULD", "SHOULD NOT" and "MAY" are to be interpreted as described in RFC 2119.

## 4. Approved Patterns

### 4.1 INT-P1 — Domain Event Publication

A domain publishes business events — immutable statements of fact such as "milestone recorded" or "customs declaration accepted" — to the Harbourline Event Backbone (APP-120).

1. INT-P1 is **mandatory** for all cross-domain asynchronous integration. A consuming domain MUST NOT poll a producing domain's API to detect change where an event exists or can reasonably be published.
2. Where the event must be consistent with a database write, the producer MUST use the **transactional outbox** pattern: the event is written to an outbox table in the same transaction as the business change and relayed to the Event Backbone by a managed change-data-capture connector (see ADR-0038).
3. Dual writes (committing to the database and separately calling the Kafka producer in application code) MUST NOT be used for events that downstream systems treat as authoritative.
4. Events MUST follow the naming, schema and payload rules of STD-EVT-003, e.g. `shipment.milestone.recorded.v1`, `customs.declaration.accepted.v1`.

### 4.2 INT-P2 — Event-Carried State Transfer

Events carry the full state that consumers need, so each consumer maintains a local read model and does not call back to the producer.

1. INT-P2 SHOULD be used for high-read consumers, for example the Harbourline Connect portal (APP-050) and the Customer Notification Service (APP-055). ADR-0030 is the canonical example.
2. State events SHOULD be published to compacted topics keyed by the business identifier (e.g. shipment ID) as set out in STD-EVT-003.
3. Consumers MUST treat the local read model as a derived copy; the producer remains the system of record (AP-07).
4. Consumers MUST be able to rebuild the read model from the compacted topic without requesting a bulk extract from the producer.

### 4.3 INT-P3 — Synchronous Request/Response via API Gateway

Used for queries and commands that need an immediate answer, such as a rate quote, a booking submission or a customs status lookup initiated by a user.

1. All synchronous cross-domain and external APIs MUST be exposed through the Harbourline API Gateway (Azure API Management, APP-121) and comply with STD-API-002.
2. A synchronous call chain MUST NOT exceed **3 hops** (caller → service A → service B → service C is the maximum). Designs needing deeper chains MUST be restructured using INT-P2 read models.
3. Callers MUST apply timeouts (default 5 seconds for user-facing calls) and circuit breakers, and MUST NOT retry non-idempotent commands without an idempotency key.

### 4.4 INT-P4 — Managed File Transfer / EDI

Used for external partners — carriers, customs brokers and port community systems — that exchange EDIFACT (e.g. IFTMIN, IFTSTA, COPARN) or ANSI X12 (e.g. 204, 214, 315) messages.

1. INT-P4 flows MUST run through the B2B gateway, IBM Sterling B2B Integrator (APP-123). Sterling is rated **Contain** in STD-TLC-014: existing partners may continue; onboarding a new EDI partner requires Tier 2 review.
2. The target state for partner integration is partner APIs under INT-P3. New partners that can consume REST APIs SHOULD be onboarded via the API Gateway instead of EDI.
3. Inbound EDI messages that represent business facts (for example carrier status IFTSTA/315) SHOULD be translated and republished as domain events under INT-P1 so internal consumers do not parse EDI.

### 4.5 INT-P5 — Batch Data Ingestion

1. INT-P5 is permitted **only** for loading data into the Tidewater Data Platform (APP-080) for analytics and reporting, via connectors or scheduled batch jobs as described in RA-04.
2. INT-P5 MUST NOT be used for operational integration between applications. A nightly file dropped from one operational system and loaded into another is a prohibited pattern under §5.

### 4.6 Pattern selection guide

| Need | Pattern | Example |
|---|---|---|
| Notify other domains that something happened | INT-P1 | HSP publishes `shipment.milestone.recorded.v1` |
| Consumer needs to query producer data at high volume | INT-P2 | Portal read model for shipment status |
| User needs an immediate answer or confirmation | INT-P3 | `POST /v1/bookings` via API Gateway |
| External partner only supports EDI/files | INT-P4 | Carrier IFTSTA status messages |
| Load data for analytics | INT-P5 | Daily finance extract to Tidewater bronze layer |

## 5. Prohibited Patterns

The following MUST NOT be used in any new or materially changed solution:

| # | Prohibited pattern | Rationale |
|---|---|---|
| 5.1 | New point-to-point database links across domains (DB links, linked servers, direct JDBC/ODBC reads of another domain's database) | Couples schemas; bypasses the owning domain; violates AP-07 |
| 5.2 | Shared databases across domains (two domains writing to or owning tables in the same database) | No single system of record; blocks independent change |
| 5.3 | New MuleSoft Anypoint flows after **2025-06-30** | ADR-0015 freeze; MuleSoft sunset 2026-12-31 |
| 5.4 | Synchronous call chains deeper than 3 hops | Latency and cascading failure risk |
| 5.5 | Polling another domain's API on a schedule to detect change | Replaced by INT-P1/INT-P2 |

Changes to existing MuleSoft flows are limited to defect fixes and regulatory changes until each flow is migrated to INT-P1 or INT-P3 under the HSP work packages. The EA Office reports the remaining MuleSoft flow count to the ARB monthly; each migration MUST be tracked in the ServiceNow CMDB (APP-110) against the flow identifier.

## 6. Cross-Cutting Requirements

1. All integration endpoints MUST emit OpenTelemetry traces with W3C trace context propagated across API calls and event headers (STD-OBS-010).
2. Payloads containing Restricted data MUST comply with STD-DAT-004 and STD-SEC-009; event payloads MUST NOT contain Restricted fields unless field-level encrypted (STD-EVT-003).
3. Cross-border flows of personal data MUST comply with STD-DAT-005 before go-live.
4. Every integration MUST be registered in the CMDB with producer, consumer, pattern ID (INT-P1..INT-P5) and data classification.

## 7. Compliance and Exceptions

1. Compliance with this standard is assessed during ARB review (Tier 1 or Tier 2) and in compliance assessments such as G-02, which found a proposed 30-second REST polling design non-compliant with INT-P1 and AP-08.
2. A solution that cannot meet a MUST requirement MUST request an exception under the GOV-01 exception process. Approved exceptions receive an `EXC-YYYY-NNN` identifier, a maximum duration of 12 months (renewable once), a remediation plan, and are recorded in the Architecture Exceptions Register (GOV-02).
3. Exceptions to §5.3 (MuleSoft freeze) will not be granted beyond 2026-12-31.

## 8. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2023-06-15 | Amara Osei | Initial standard; MuleSoft hub-and-spoke as default integration style |
| 2.0 | 2024-10-01 | Amara Osei | Rewritten around the Event Backbone (ADR-0007); introduced INT-P1..INT-P5; added MuleSoft freeze from ADR-0015 |
| 2.1 | 2025-03-01 | Amara Osei | Mandated transactional outbox for INT-P1; added 3-hop limit and pattern selection guide; ARB-2025-012 |
