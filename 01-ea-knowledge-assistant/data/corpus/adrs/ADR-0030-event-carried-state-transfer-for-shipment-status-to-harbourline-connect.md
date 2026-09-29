---
doc_id: ADR-0030
title: Event-Carried State Transfer for Shipment Status to Harbourline Connect
doc_type: adr
version: "1.0"
status: Accepted
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2025-016)
effective_date: 2025-04-22
next_review: 2027-04-22
classification: Internal
related: [AP-01, AP-07, AP-08, AP-09, AP-14, STD-INT-001, STD-EVT-003, STD-API-002, STD-OBS-010, ADR-0007, ADR-0038, ADR-0041, RA-01, APP-022, APP-050, APP-120]
---

# ADR-0030 — Event-Carried State Transfer for Shipment Status to Harbourline Connect

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2025-04-22 |
| ARB decision | ARB-2025-016 (session of Thursday 2025-04-17), Approved |
| Deciders | David Okafor (Chair), Amara Osei, Lena Vogel, Priya Raman, Kenji Watanabe |
| Consulted | Harbourline Digital portal team, Grace Liu (HSP programme), Kestrel Digital Partners |
| Review tier | Tier 2 escalated to Tier 1 (sets the pattern for all HSP read consumers) |

## 2. Context

Harbourline Connect (APP-050) is the customer portal (web and mobile), with a React front end and a .NET 8 backend-for-frontend on AKS. Its most-used feature is shipment tracking: ~38,000 daily active users, ~2.4 million shipment-status reads per day, and peaks of ~450 reads/s on Monday mornings in the US and EU.

Today the portal obtains status by calling FreightMaster through MuleSoft façades, with a 15-minute cache. When the Harbourline Shipment Platform (APP-022) goes live for US lanes, the system of record for shipments moves to HSP. Horizon 2028 targets milestone events visible to customers in under 5 minutes for 95% of shipments (REQ-HSP-014).

HSP will publish `shipment.milestone.recorded.v1` (each milestone: booked, gated-in, loaded, departed, arrived, discharged, customs released, delivered) and `shipment.status.changed.v1` (the current aggregate status) on the Event Backbone.

## 3. Decision Drivers

1. Milestone latency < 5 minutes p95 end to end (REQ-HSP-014).
2. Portal availability must not depend on HSP availability; the portal is customer-facing and HSP releases frequently in its first year.
3. Read load (450 reads/s peak, growing) should not be placed on HSP's transactional PostgreSQL databases.
4. Keep HSP the single system of record (AP-07); the portal must not become a second source of truth.
5. Consistency with STD-INT-001 and the RA-01 reference architecture.
6. Portal team capacity (6 engineers).

## 4. Considered Options

- **Option A — Synchronous query** of the HSP shipment API through the API Gateway on each page view (INT-P3), with a short cache.
- **Option B — Event-Carried State Transfer** (INT-P2): portal consumes HSP events and maintains its own read model.
- **Option C — Thin notification + callback**: HSP emits "shipment changed" notifications with IDs only; portal calls the API to fetch state.

### 4.1 Comparison

| Criterion | A — Sync query | B — ECST read model | C — Notify + fetch |
|---|---|---|---|
| p95 latency, milestone → visible | Depends on cache TTL (60 s TTL ≈ 1 min) | ~15-40 s measured in PoC | ~20-60 s |
| Portal availability if HSP down | Degraded / stale cache only | Unaffected (serves last known state) | Degraded for changed shipments |
| Load on HSP | ~450 req/s peak, all reads | Near zero from portal | ~40 req/s (on change) |
| Data duplication | None | Full shipment status projection | Partial |
| Complexity for portal team | Low | Medium (consumer, idempotency, replay) | Medium-high |
| Additional cost | APIM units + HSP scale-out ~USD 4k/month | Portal read store ~USD 2.5k/month | ~USD 3k/month |

## 5. Decision Outcome

**Chosen option: B — Event-Carried State Transfer.** Harbourline Connect maintains a local shipment-status read model fed by `shipment.milestone.recorded.v1` and `shipment.status.changed.v1`. This applies **INT-P2** of STD-INT-001.

Rules:

1. Events MUST carry the full state the portal needs (status, milestone type, timestamp, location UN/LOCODE, vessel/voyage, ETA), so no callback to HSP is needed for display.
2. The read model lives in a PostgreSQL Flexible Server database owned by the portal team, in the same regional deployment as the portal. It is a **projection**, not a system of record; customers cannot edit shipment data through it.
3. Consumers MUST be idempotent (upsert keyed on `shipmentId` + event sequence number) and discard out-of-order events with a lower sequence number.
4. Failed messages go to `shipment.milestone.recorded.v1.dlq` / `shipment.status.changed.v1.dlq`, with alerting at > 50 messages in 15 minutes.
5. The read model MUST be rebuildable from the compacted `shipment.status.changed.v1` topic; a full rebuild target is under 2 hours.
6. Detailed shipment documents and commands (e.g., amending a booking) still use synchronous HSP APIs via the Harbourline API Gateway (INT-P3).

Option A couples portal availability to HSP and loads its transactional databases; Option C adds a synchronous call per change without benefit over B.

## 6. Consequences

### 6.1 Positive

- Measured milestone-to-portal latency of 15-40 s leaves ample margin against the 5-minute target.
- The portal keeps serving tracking pages during HSP maintenance or incidents.
- HSP services scale on transactional load only.
- The same events feed other consumers (e.g., notifications and Tidewater) without extra HSP work.

### 6.2 Negative

- The portal holds a duplicate projection of shipment status; eventual consistency means a customer can briefly see a milestone in an email before the portal shows it, or vice versa.
- HSP event schemas become a contract with a broad blast radius; schema changes need BACKWARD compatibility and consumer sign-off.
- The portal team must operate a Kafka consumer, DLQ handling and replay tooling, which is new to them (estimated 3 sprints).
- Rebuilding the read model after a defect requires a controlled replay and temporarily increased Confluent throughput.

### 6.3 Neutral

- Read-model data stays in the portal's regional deployment; regional placement is addressed separately in ADR-0041.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Register both event schemas (Avro) in Schema Registry | HSP shipment team | 2025-06-15 |
| Implement idempotent consumer and DLQ alerts | Harbourline Digital portal team | 2025-09-30 |
| End-to-end latency SLO dashboard (OpenTelemetry trace across producer and consumer) | Kenji Watanabe | 2025-10-31 |
| Add worked example to RA-01 | Amara Osei | 2025-07-31 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-08 Event-First Integration Between Domains | Compliant. |
| AP-07 One System of Record per Data Domain | Compliant; HSP remains system of record, portal holds a projection. |
| AP-01 Customer Visibility by Default | Directly supports near-real-time tracking. |
| STD-INT-001 INT-P2 / INT-P3 | Applies INT-P2 for status, INT-P3 for commands. |
| STD-EVT-003 | Topic names, Avro, BACKWARD compatibility, DLQ naming, idempotent consumers. |
| STD-OBS-010 | W3C trace context carried in event headers. |

## 8. Links

- RA-01 Event-Driven Domain Integration
- ADR-0038 Transactional Outbox for Publishing Domain Events from HSP
- ADR-0041 Serve EU Customer Data for Harbourline Connect from West Europe
- ARS-01 Architecture Requirements Specification (REQ-HSP-014)
- ARB log entry ARB-2025-016
