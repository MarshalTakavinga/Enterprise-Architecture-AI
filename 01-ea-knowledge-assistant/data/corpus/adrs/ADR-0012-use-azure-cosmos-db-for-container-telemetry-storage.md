---
doc_id: ADR-0012
title: Use Azure Cosmos DB for Container Telemetry Storage
doc_type: adr
version: "1.0"
status: Accepted
owner: Lena Vogel, Lead Data Architect
approved_by: Architecture Review Board (ARB-2024-019)
effective_date: 2024-05-14
next_review: 2026-05-14
classification: Internal
related: [AP-05, AP-07, AP-11, AP-14, STD-DB-006, STD-DAT-004, STD-RES-015, ADR-0024, RA-04, APP-090, APP-080]
---

# ADR-0012 — Use Azure Cosmos DB for Container Telemetry Storage

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-05-14 |
| ARB decision | ARB-2024-019 (session of Thursday 2024-05-09), Approved |
| Deciders | David Okafor (Chair), Lena Vogel, Kenji Watanabe, Priya Raman, Amara Osei |
| Consulted | Container Tracking Service product team, Michael Torres (VP Port & Terminal Services) |
| Review tier | Tier 1 (new data store for a new system) |

## 2. Context

The Container Tracking Service (APP-090) ingests telemetry from reefer controllers and smart-container gateways through Azure IoT Hub. Devices report temperature, door state, position and power every 5-15 minutes. With about 62,000 connected units in 2024, the service already handles ~40 million telemetry events per day and the reefer fleet is forecast to grow 20% a year.

Access patterns are narrow and well understood:

- **Write:** ~460 events/s average, bursts of ~2,500 events/s when vessels come alongside and gateways flush buffered readings.
- **Read (operational):** "latest state for container X" and "last 72 hours for container X" for the portal and reefer monitoring desk; p99 target < 50 ms.
- **Read (analytical):** fleet-wide trends, cold-chain excursion analysis and model training. These run in Tidewater (APP-080), not against the operational store.

Telemetry is classified Internal under STD-DAT-004; it contains no personal data. Data older than 90 days is never queried operationally.

## 3. Decision Drivers

1. Sustained write throughput with predictable latency during vessel bursts.
2. Point reads by container ID in single-digit milliseconds.
3. Automatic expiry of hot data without batch delete jobs.
4. Managed service with zone redundancy (AP-11; Tier 1 under STD-RES-015 for the reefer alarm path).
5. Low-effort export to the lakehouse for analytics.
6. Cost at forecast 2027 volume (~70M events/day).

## 4. Considered Options

- **Option A — Azure Cosmos DB for NoSQL**, container partitioned on `/containerId`, TTL for expiry, analytical store / change feed to ADLS.
- **Option B — Azure Database for PostgreSQL Flexible Server** with time-based partitioning.
- **Option C — Azure Data Explorer (ADX)** as the single store for operational and analytical access.

### 4.1 Comparison

| Criterion | A — Cosmos DB NoSQL | B — PostgreSQL Flexible Server | C — Azure Data Explorer |
|---|---|---|---|
| Sustained writes at 2,500/s burst | Yes; autoscale RU/s | Marginal; load test on 16 vCore peaked at ~1,900 inserts/s with indexes before WAL and vacuum pressure | Yes, via batched ingestion |
| Point read p99 | ~8 ms measured | ~12 ms, degrading as partitions grow | 200-800 ms (ingestion latency and query engine not designed for point reads) |
| Hot-data expiry | Native TTL per item | Partition drop jobs to operate | Retention policy (native) |
| Analytics | Change feed / export to ADLS | Export jobs required | Excellent (KQL) |
| Est. monthly cost at 2027 volume | ~USD 14,800 (autoscale, 1 region + zone redundancy) | ~USD 9,500 plus ~0.5 FTE DBA effort | ~USD 17,500 (cluster sized for freshness) |
| Team skill | Moderate; 2 engineers certified | High | Low |

## 5. Decision Outcome

**Chosen option: A — Azure Cosmos DB for NoSQL.**

Design parameters approved by the ARB:

- **Partition key:** `/containerId`. Every operational query is scoped to one container, giving single-partition reads and an even spread across ~62,000+ logical partitions. The largest expected logical partition (one container, 90 days at 5-minute intervals) is under 30 MB, well below the 20 GB limit.
- **Item id:** `<deviceId>-<epochMillis>` to make writes idempotent on replay from IoT Hub.
- **TTL:** 90 days on the hot container. A separate `latest-state` container holds one document per container, upserted on each reading, with no TTL.
- **Archive:** change feed processor writes to ADLS Gen2 (bronze layer of Tidewater, RA-04) within 15 minutes; archive retention 7 years.
- **Consistency:** Session.
- **Throughput:** autoscale 4,000-40,000 RU/s, reviewed quarterly.

PostgreSQL remained viable on cost, but the load test showed insufficient headroom for burst writes and the partition maintenance would have fallen on a thin DBA team. ADX is the better analytical engine and is **retained for analytics** (reefer excursion dashboards) fed from the archive, but it cannot meet the 50 ms point-read requirement.

## 6. Consequences

### 6.1 Positive

- Burst ingestion absorbed by autoscale without operational intervention.
- TTL removes manual purge jobs; storage stays roughly flat at ~1.1 TB hot.
- Clear split: Cosmos DB for operational access, Tidewater/ADX for analytics.

### 6.2 Negative

- Cosmos DB cost is the most sensitive line in the CTS budget; a poorly written cross-partition query can consume thousands of RUs. Query review is now required in the CTS pull-request template.
- No joins or ad-hoc SQL for operations staff; any new access pattern (for example "all containers on vessel V") needs a new materialised view fed by change feed.
- Adds a second operational database technology alongside PostgreSQL (see ADR-0024), with its own skills and on-call runbook.
- Proprietary API; migration off Cosmos DB would require application changes (partly mitigated by keeping the data model simple JSON).

### 6.3 Neutral

- Telemetry is Internal, so no customer-managed keys are required; service-managed keys are acceptable under STD-SEC-009.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Build `latest-state` and vessel-view materialised containers | CTS product team | 2024-07-31 |
| Change feed to ADLS bronze, with row-count reconciliation | Lena Vogel | 2024-08-30 |
| RU consumption alerts at 70% / 90% of max autoscale | Kenji Watanabe | 2024-06-14 |
| Record Cosmos DB workload criteria in STD-DB-006 | Lena Vogel | next revision |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| STD-DB-006 Database Technology Selection | This ADR is the reference case for "Cosmos DB for high-volume telemetry with key-based access"; partition-key design reviewed by the data architect. |
| AP-07 One System of Record per Data Domain | CTS is the system of record for telemetry; Tidewater holds derived copies only. |
| AP-11 Managed Services | Compliant. |
| AP-14 Observable by Default | Compliant; RU, throttling (429) and latency metrics in Azure Monitor. |
| STD-DAT-004 | Data classified Internal; no personal data. |

## 8. Links

- STD-DB-006 Database Technology Selection Standard
- RA-04 Tidewater Enterprise Data Platform
- ADR-0024 PostgreSQL Flexible Server as Default Relational Database
- APP-090 Container Tracking Service; APP-080 Tidewater Data Platform
- ARB log entry ARB-2024-019
