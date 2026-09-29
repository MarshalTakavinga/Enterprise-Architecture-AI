---
doc_id: ADR-0038
title: Transactional Outbox for Publishing Domain Events from HSP
doc_type: adr
version: "1.0"
status: Accepted
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2025-022)
effective_date: 2025-06-10
next_review: 2027-06-10
classification: Internal
related: [AP-07, AP-08, AP-11, AP-14, STD-INT-001, STD-EVT-003, STD-DB-006, STD-OBS-010, ADR-0007, ADR-0024, ADR-0030, RA-01, APP-022, APP-120]
---

# ADR-0038 — Transactional Outbox for Publishing Domain Events from HSP

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2025-06-10 |
| ARB decision | ARB-2025-022 (session of Thursday 2025-06-05), Approved |
| Deciders | David Okafor (Chair), Amara Osei, Lena Vogel, Kenji Watanabe, Priya Raman |
| Consulted | HSP service teams, Kestrel Digital Partners, Grace Liu |
| Review tier | Tier 2 escalated to Tier 1 (binding on all HSP services) |

## 2. Context

The Harbourline Shipment Platform (APP-022) is being built as ~25 microservices on AKS, each owning a PostgreSQL Flexible Server database (ADR-0024). Services publish domain events to the Harbourline Event Backbone (ADR-0007) so that the portal (ADR-0030), notifications, customs and Tidewater can react.

During the first integration test cycle in May 2025, the booking and milestone services used a "write to DB, then publish to Kafka" approach. Under fault injection:

- 0.4% of milestone updates committed to the database without an event being published (process killed between commit and send).
- 0.1% of events were published for transactions that then rolled back.

For customer visibility (REQ-HSP-014) and downstream customs processing, both failure modes are unacceptable: a missing "customs released" event can hold a container, and a phantom event can mislead a customer. Expected event volume at US-lane go-live is ~350 events/s average and ~2,000 events/s peak, growing to ~5,000 events/s peak when EU lanes and Nordhaven migrate.

## 3. Decision Drivers

1. Atomicity: an event is published if and only if the business transaction commits.
2. Ordering per aggregate (per `shipmentId`).
3. Latency contribution < 5 s p95 from commit to topic, to protect the 5-minute end-to-end target.
4. Minimal bespoke infrastructure (AP-11); no self-hosted Kafka Connect.
5. Uniform pattern that Kestrel and internal teams can apply across 25 services.
6. Observability of the full path (AP-14).

## 4. Considered Options

- **Option A — Transactional outbox table in each service's PostgreSQL database, relayed by the Confluent-managed Debezium PostgreSQL CDC connector.**
- **Option B — Outbox table with an in-service polling publisher** (background worker reads unsent rows and publishes).
- **Option C — Kafka transactions / dual-write with retries** in application code.
- **Option D — CDC directly on business tables** (no outbox; consumers see table-change events).

### 4.1 Comparison

| Criterion | A — Outbox + managed Debezium | B — Outbox + polling publisher | C — Dual write | D — CDC on business tables |
|---|---|---|---|---|
| Atomic with DB commit | Yes | Yes | No (cannot span DB and Kafka) | Yes |
| Commit-to-topic latency (PoC p95) | 1.2 s | 2-10 s (poll interval dependent) | < 0.5 s | 1.1 s |
| Per-aggregate ordering | Yes (key = aggregate id) | Yes, with care | Not guaranteed on retry | Yes |
| Event is a business fact (not a row change) | Yes | Yes | Yes | No; leaks internal schema |
| Infrastructure to operate | Managed connector | Code in every service | None | Managed connector |
| DB load | Low (WAL read) | Polling queries every 1-2 s | None | Low |
| Est. connector cost | ~USD 350/month per connector task | None | None | Similar to A |

## 5. Decision Outcome

**Chosen option: A — Transactional outbox with the Confluent-managed Debezium CDC connector.** This is the mandatory implementation of **INT-P1** for HSP services whose events must be consistent with a database write.

Implementation rules:

1. Each service has an `outbox` table: `id (uuid)`, `aggregate_type`, `aggregate_id`, `event_type`, `topic`, `payload (bytea, Avro-encoded)`, `headers (jsonb, incl. traceparent)`, `created_at`. Rows are inserted in the same transaction as the business change.
2. The Debezium PostgreSQL connector (Confluent Cloud managed, `pgoutput` plugin) uses the outbox event router to route by `topic` and key by `aggregate_id`.
3. Topics follow STD-EVT-003 naming, e.g., `shipment.milestone.recorded.v1`, `shipment.status.changed.v1`.
4. Delivery is at-least-once; consumers MUST be idempotent using the event `id`.
5. Outbox rows are deleted by a scheduled job after 72 hours; WAL retention and replication-slot lag are monitored (alert at 2 GB slot lag).
6. Connectors reach PostgreSQL via Private Link; the replication user authenticates with a secret stored in Key Vault and rotated every 90 days (managed identity is not yet supported by the connector).
7. No Restricted data in payloads unless field-level encrypted, per STD-EVT-003.

## 6. Consequences

### 6.1 Positive

- Fault-injection rerun: zero lost and zero phantom events across 2.1 million test transactions.
- Commit-to-topic latency of ~1.2 s p95 leaves most of the 5-minute budget to consumers.
- One pattern for all services, documented in RA-01.

### 6.2 Negative

- Logical replication slots can cause WAL growth and disk exhaustion if a connector stalls; this is now an operational risk for Tier 1 databases and requires alerting and a runbook.
- Connector cost scales with the number of databases: ~25 connectors at ~USD 350/month is ~USD 105k/year.
- Major-version upgrades and failovers of PostgreSQL Flexible Server require replication slot handling; failover testing showed a 3-6 minute publication pause while the connector re-establishes its slot.
- The connector's use of a database password is a deviation from the managed-identity rule in STD-IAM-008, tracked for remediation when supported.
- Developers must write explicit event payloads, adding modest effort per feature.

### 6.3 Neutral

- Services with no transactional coupling (e.g., pure stream processors) may publish directly to Kafka.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Shared outbox library for Java 21 and .NET 8 | Kestrel Digital Partners | 2025-07-31 |
| Replication-slot lag alerts and runbook | Kenji Watanabe | 2025-07-15 |
| Update RA-01 with outbox building block | Amara Osei | 2025-08-31 |
| Track connector managed-identity support | Priya Raman | quarterly |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-08 / STD-INT-001 INT-P1 | Compliant; outbox mandated where consistency with a DB write is required. |
| AP-07 One System of Record per Data Domain | Events published by the owning service only. |
| STD-EVT-003 | Naming, Avro, idempotent consumers, payload rules. |
| AP-14 / STD-OBS-010 | Trace context carried in headers from HTTP request to consumer. |
| STD-IAM-008 | Minor deviation (connector secret); remediation tracked. |

## 8. Links

- RA-01 Event-Driven Domain Integration
- ADR-0007 Adopt Confluent Cloud as the Enterprise Event Backbone
- ADR-0024 PostgreSQL Flexible Server as Default Relational Database
- ADR-0030 Event-Carried State Transfer for Shipment Status to Harbourline Connect
- ARB log entry ARB-2025-022
