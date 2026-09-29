---
doc_id: ADR-0007
title: Adopt Confluent Cloud as the Enterprise Event Backbone
doc_type: adr
version: "1.0"
status: Accepted
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2024-007)
effective_date: 2024-02-20
next_review: 2026-02-20
classification: Internal
related: [AP-08, AP-10, AP-11, STD-INT-001, STD-EVT-003, STD-TLC-014, ADR-0015, ADR-0021, ADR-0038, RA-01, APP-120, APP-122]
---

# ADR-0007 — Adopt Confluent Cloud as the Enterprise Event Backbone

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-02-20 |
| ARB decision | ARB-2024-007 (session of Thursday 2024-02-15), Approved with Conditions |
| Deciders | David Okafor (Chair), Amara Osei, Priya Raman, Kenji Watanabe, Lena Vogel |
| Consulted | Tomasz Nowak, Elena Marsh (CIO), Harbourline Digital engineering leads |
| Review tier | Tier 1 (new platform technology, cost > USD 500k over three years) |

## 2. Context

Harbourline integrates its operational systems mostly through MuleSoft Anypoint (APP-122), which in early 2024 carried roughly 310 flows. Around 70% of those flows are polling or scheduled jobs that copy shipment and container status between FreightMaster TMS (APP-020), Salesforce (APP-040), the customs gateway (APP-060) and the customer portal. Median end-to-end latency for a shipment milestone reaching the portal is 22 minutes, and the p95 is above 90 minutes.

Two further facts shaped the decision. First, the acquisition of Nordhaven Freight GmbH is expected to close in March 2024; Nordhaven's TMS (APP-021) runs on AWS eu-central-1, and any integration fabric must span Azure and AWS without a bespoke bridge. Second, the planned shipment platform consolidation will be built as event-producing microservices, so the organisation needs a durable, replayable log with schema governance rather than a message queue.

Projected load for the first three years: 6,000 events/s average, 25,000 events/s peak during vessel discharge windows.

## 3. Decision Drivers

1. **Schema governance** — a central registry with enforced compatibility rules so that producers cannot silently break consumers.
2. **Ecosystem** — managed connectors (CDC, Blob Storage, Salesforce, Databricks) to avoid hand-built adapters.
3. **Multi-cloud portability** — native replication between Azure and AWS for Nordhaven, consistent with AP-10.
4. **Managed operation** — no self-managed brokers, consistent with AP-11; the integration team has 9 engineers and no Kafka operations experience.
5. **Replay and retention** — consumers must be able to rebuild read models from history.
6. **Cost** — three-year total cost of ownership within the USD 2.1M envelope set by the CIO.

## 4. Considered Options

- **Option A — Confluent Cloud (Dedicated cluster) on Azure East US 2**, with Schema Registry, managed connectors and cluster linking.
- **Option B — Azure Event Hubs Premium with the Kafka protocol endpoint**, plus Azure Schema Registry.
- **Option C — Extend MuleSoft Anypoint** with Anypoint MQ and additional vCores.

### 4.1 Scoring

Weights agreed by the ARB before scoring; scores 1 (poor) to 5 (strong).

| Driver (weight) | A — Confluent Cloud | B — Event Hubs (Kafka API) | C — Extend MuleSoft |
|---|---|---|---|
| Schema governance (20%) | 5 — Schema Registry, BACKWARD/FULL modes, broker-side validation | 3 — Azure Schema Registry, weaker client tooling | 2 — no log-level schema enforcement |
| Ecosystem / connectors (20%) | 5 — 80+ managed connectors incl. Debezium CDC | 3 — Kafka Connect must be self-hosted | 3 — rich adapters, but point-to-point style |
| Multi-cloud portability (20%) | 5 — cluster linking to AWS | 2 — Azure only; AWS bridge needed | 3 — runtimes on both clouds, not a log |
| Managed operation (15%) | 4 | 5 | 3 |
| Replay / retention (15%) | 5 — tiered storage, compaction | 3 — 90-day max, partial compaction support | 1 — queue semantics only |
| 3-year cost (10%) | 3 — est. USD 1.85M | 4 — est. USD 1.2M + ~USD 0.3M Connect hosting | 2 — est. USD 2.4M incl. vCore uplift |
| **Weighted total** | **4.65** | **3.20** | **2.40** |

## 5. Decision Outcome

**Chosen option: A — Confluent Cloud on Azure**, branded internally as the **Harbourline Event Backbone** (APP-120).

Event Hubs scored well on simplicity and price, but lacks managed Kafka Connect, strong replay and native AWS replication. Extending MuleSoft would have deepened a platform whose licence renewal is already under question and would not give a replayable log.

Conditions attached by ARB-2024-007:

1. Private networking only (Azure Private Link); no public cluster endpoints.
2. Customer-managed encryption keys held in Azure Key Vault, per Priya Raman's condition.
3. Topic naming, schema and DLQ conventions to be codified in a new Event Streaming Standard (published as STD-EVT-003).
4. A capacity and cost review after 12 months of production traffic.

## 6. Consequences

### 6.1 Positive

- Enables INT-P1 and INT-P2 patterns under STD-INT-001 and the RA-01 building blocks.
- Schema Registry with BACKWARD compatibility prevents breaking changes reaching consumers.
- Cluster linking gives a supported path to Nordhaven on AWS (see ADR-0021).
- Managed Debezium CDC removes the need to host Connect workers (used later in ADR-0038).

### 6.2 Negative

- New commercial dependency on a third-party SaaS with committed annual spend of about USD 520k; exit would require re-platforming producers' client configuration.
- Dedicated clusters bill for capacity (CKUs), not usage; we will pay for peak headroom during the 18-month ramp when utilisation is expected to stay under 35%.
- Skills gap: none of the integration team holds Kafka experience. Training budget of USD 60k and 6 weeks of vendor enablement required.
- Two integration platforms run in parallel until MuleSoft retirement, increasing run cost in FY2024-FY2026.

### 6.3 Neutral

- Kafka client libraries are open source, so producer/consumer code remains portable to another Kafka-compatible service.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Draft Event Streaming Standard (STD-EVT-003) | Amara Osei | 2024-05-31 |
| Landing zone Private Link and Key Vault BYOK design | Kenji Watanabe | 2024-04-15 |
| Add Confluent Cloud to technology radar as Adopt (STD-TLC-014) | David Okafor | 2024-03-07 |
| Kafka training for integration team | Amara Osei | 2024-06-30 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-08 Event-First Integration Between Domains | Directly enables; provides the backbone the principle assumes. |
| AP-10 Cloud-Smart and Portable | Compliant; hosted on Azure (primary) with a standard Kafka protocol and AWS reach. |
| AP-11 Managed Services over Self-Managed Infrastructure | Compliant; fully managed service. |
| AP-14 Observable by Default | Compliant subject to exporting cluster metrics to Azure Monitor. |
| STD-SEC-009 Encryption & Key Management | Compliant via BYOK condition. |
| STD-CLD-007 Cloud Landing Zone & Hosting | Compliant; East US 2, private connectivity. |

## 8. Links

- STD-INT-001 Integration Patterns Standard; STD-EVT-003 Event Streaming Standard
- RA-01 Event-Driven Domain Integration
- ADR-0015 Sunset MuleSoft ESB and Freeze New Flows
- ADR-0021 Temporarily Retain Nordhaven TMS on AWS
- ADR-0038 Transactional Outbox for Publishing Domain Events from HSP
- ARB log entry ARB-2024-007
