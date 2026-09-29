---
doc_id: STD-EVT-003
title: Event Streaming Standard
doc_type: standard
togaf_phase: Preliminary
version: "1.2"
status: Approved
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2025-019)
effective_date: 2025-05-01
next_review: 2026-11-01
classification: Internal
related: [AP-08, AP-05, AP-14, STD-INT-001, STD-DAT-004, STD-SEC-009, STD-OBS-010, ADR-0007, ADR-0021, ADR-0030, ADR-0038, RA-01, GOV-01, GOV-02]
---

# STD-EVT-003 — Event Streaming Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines how events are named, modelled, produced, consumed, secured and retained on the **Harbourline Event Backbone** (APP-120). It implements patterns INT-P1 (Domain Event Publication) and INT-P2 (Event-Carried State Transfer) from STD-INT-001 and supports the Horizon 2028 goal of milestone events reaching customers in under 5 minutes (REQ-HSP-014).

## 2. Scope

- All Kafka topics on the Event Backbone, in every environment.
- All producers and consumers, including managed connectors (e.g. Debezium CDC, sink connectors to the Tidewater Data Platform).
- Cluster-linked topics shared with Nordhaven TMS (APP-021) in AWS eu-central-1 under ADR-0021.

Messaging inside a single bounded context that does not use the Event Backbone (for example an in-process queue) is out of scope.

## 3. Related Principles and Normative References

- **AP-08 Event-First Integration Between Domains**; **AP-05 Data Is an Asset with a Named Owner**; **AP-14 Observable by Default**.
- **STD-INT-001** §4.1 and §4.2; **STD-DAT-004** (classification); **STD-SEC-009** (encryption); **STD-OBS-010** (tracing).
- **ADR-0007** Confluent Cloud as the Enterprise Event Backbone; **ADR-0038** Transactional Outbox; **ADR-0030** Event-Carried State Transfer to Harbourline Connect.
- **RA-01** Event-Driven Domain Integration.

Normative terms follow RFC 2119.

## 4. Platform

1. The Event Backbone is **Confluent Cloud (Apache Kafka) on Azure**. It is the only approved platform for cross-domain event streaming.
2. Production clusters are Dedicated clusters with private networking in East US 2 and West Europe; topics containing EU personal data MUST reside on the West Europe cluster (STD-DAT-005).
3. Azure Event Hubs MAY be used only as an ingestion buffer inside a single solution (for example IoT Hub routing for the Container Tracking Service, APP-090) and MUST NOT be used as a cross-domain backbone.
4. New MuleSoft or point-to-point messaging for cross-domain events is prohibited (STD-INT-001 §5).

## 5. Topic Design

### 5.1 Naming

Topic names MUST follow the pattern:

```
<domain>.<entity>.<event>.v<major>
```

- All lower case; words within a segment separated by hyphens.
- `<event>` is a past-tense verb for fact events.

| Example topic | Producer | Type |
|---|---|---|
| `shipment.milestone.recorded.v1` | HSP (APP-022) | Fact event |
| `shipment.status.changed.v1` | HSP (APP-022) | State (compacted) |
| `customs.declaration.accepted.v1` | Customs Filing Gateway (APP-060) | Fact event |
| `terminal.gate-transaction.completed.v1` | Terminal Gate Automation via DMZ broker | Fact event |
| `container.reefer-alarm.raised.v1` | Container Tracking Service (APP-090) | Fact event |

Environment and region MUST NOT be encoded in topic names; they are separated by cluster.

### 5.2 Ownership

1. Every topic MUST have exactly one owning (producing) domain, recorded as topic metadata (`owner`, `app-id`, `data-classification`).
2. Only the owning domain MAY write to a topic. Consumers MUST NOT publish to another domain's topic.
3. Topics MUST be created through Terraform (AP-15); manual creation in the Confluent console is prohibited outside the sandbox environment.

### 5.3 Partitioning

1. Topics MUST be keyed by the business identifier that requires ordering (e.g. `shipmentId`, `containerId`).
2. Default partition count is 12 for production topics; changes require the integration architect's approval, as repartitioning breaks key ordering.

## 6. Schemas and Compatibility

1. Every topic MUST have a registered schema in **Confluent Schema Registry**. Unregistered or schemaless payloads MUST be rejected by producer configuration.
2. **Avro** is the preferred format. JSON Schema MAY be used where a producer cannot support Avro; Protobuf requires integration architect approval.
3. The subject compatibility mode MUST be **BACKWARD**. Breaking changes require a new topic with an incremented major version (e.g. `.v2`) and a parallel-run period of at least 3 months.
4. Every event MUST carry a standard envelope: `eventId` (UUID), `eventType`, `eventTime` (UTC, ISO 8601), `source` (app ID), `correlationId`, `schemaVersion`.

## 7. Payload Rules

1. Maximum message size is **1 MB**. Larger payloads (documents, images, bulk manifests) MUST use the **claim-check pattern**: store the object in Azure Blob Storage and publish a reference (URI plus hash); consumers retrieve it using their managed identity.
2. **Restricted** data (STD-DAT-004) MUST NOT appear in event payloads unless the fields are **field-level encrypted** with keys managed per STD-SEC-009. Crew passport numbers and payment card data MUST NOT be published under any circumstances.
3. Events SHOULD carry identifiers rather than personal data where consumers do not need it; for example CNS needs a contact reference, not a full customer profile.
4. For INT-P2 state events, the payload MUST contain the full current state of the entity required by consumers, not a delta.

## 8. Retention and Compaction

| Topic type | Setting | Default |
|---|---|---|
| Fact events | `cleanup.policy=delete` | Retention **7 days** |
| State (INT-P2) | `cleanup.policy=compact` | Retained indefinitely per key; tombstones after 24 h |
| Dead-letter topics | `cleanup.policy=delete` | Retention 14 days |

Retention longer than 7 days for fact topics requires justification; long-term history belongs in the Tidewater Data Platform via a sink connector, not in Kafka.

## 9. Producers

1. Producers MUST use `acks=all` and idempotent producer settings.
2. Where an event must be consistent with a database write, the producer MUST use the transactional outbox with a managed CDC connector (ADR-0038).
3. Producers MUST propagate W3C trace context in Kafka headers (`traceparent`) per STD-OBS-010.

## 10. Consumers

1. Consumers MUST be **idempotent**: processing the same `eventId` twice MUST NOT produce a duplicate side effect (e.g. a second SMS to a customer).
2. Each consuming application MUST use its own consumer group named `<app-id>.<purpose>` (e.g. `app-055.notification-dispatch`).
3. Messages that fail after the configured retries (default 3, exponential backoff) MUST be written to a dead-letter topic named `<topic>.dlq`, e.g. `shipment.milestone.recorded.v1.dlq`, with the failure reason in headers.
4. DLQ depth MUST be monitored and alert the owning team when non-zero for more than 15 minutes.
5. Consumer lag SLOs MUST be defined for Tier 0/1 consumers; for REQ-HSP-014 the target is p95 end-to-end latency under 5 minutes.

## 11. Security

1. Clients MUST authenticate using OAuth via Microsoft Entra ID workload identities or Confluent service accounts bound to managed identities; long-lived API keys in code are prohibited (STD-IAM-008).
2. Access is granted per topic using role bindings; wildcard write access MUST NOT be granted.

## 12. Compliance and Exceptions

1. Topic definitions and schemas are validated in CI; the integration architect reviews new domains' topic designs during Tier 2 review.
2. Deviations require an exception through the GOV-01 process, recorded in GOV-02 with an `EXC-YYYY-NNN` identifier, a maximum 12-month term (renewable once) and a remediation plan.

## 13. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2024-04-01 | Amara Osei | Initial standard following ADR-0007; naming convention and Avro schemas |
| 1.1 | 2024-10-01 | Amara Osei | Added compacted state topics for INT-P2; DLQ naming; cluster linking for Nordhaven |
| 1.2 | 2025-05-01 | Amara Osei | BACKWARD compatibility mandatory; claim-check pattern for > 1 MB; field-level encryption rule for Restricted data; ARB-2025-019 |
