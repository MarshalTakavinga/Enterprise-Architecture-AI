---
doc_id: STD-DB-006
title: Database Technology Selection Standard
doc_type: standard
togaf_phase: Preliminary
version: "1.3"
status: Approved
owner: Lena Vogel, Lead Data Architect
approved_by: Architecture Review Board (ARB-2025-022)
effective_date: 2025-06-01
next_review: 2026-12-01
classification: Internal
related: [AP-03, AP-07, AP-10, AP-11, STD-DAT-004, STD-DAT-005, STD-CLD-007, STD-SEC-009, STD-RES-015, STD-TLC-014, ADR-0012, ADR-0024, RA-02, GOV-01, GOV-02]
---

# STD-DB-006 — Database Technology Selection Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard tells solution teams which database technologies they MAY use, which is the default, and — in particular — **when a NoSQL database such as Azure Cosmos DB is allowed and when it is not**. It reduces the number of database engines Harbourline has to operate, secure and license, supports exit from the Baltimore data centre by 30 June 2027, and retires the Oracle estate that underpins FreightMaster TMS (APP-020).

## 2. Scope

- All new applications and all material changes to the data tier of existing applications, in every environment, on Azure, AWS and at the terminal edge.
- Databases embedded in vendor packages are in scope for hosting decisions (§4.2) but the engine is dictated by the vendor.
- Analytical storage within the Tidewater Data Platform (Delta tables in ADLS Gen2) is governed by RA-04 and is out of scope, except where noted.

## 3. Related Principles and Normative References

- **AP-11 Managed Services over Self-Managed Infrastructure** — PaaS databases are the default.
- **AP-10 Cloud-Smart and Portable** — favour open-source-compatible engines.
- **AP-07 One System of Record per Data Domain** — a database belongs to exactly one domain.
- **ADR-0024** PostgreSQL Flexible Server as Default Relational Database; **ADR-0012** Azure Cosmos DB for Container Telemetry Storage.
- **STD-DAT-004** (classification & encryption), **STD-DAT-005** (residency), **STD-SEC-009** (keys), **STD-RES-015** (RTO/RPO), **STD-TLC-014** (radar).

Normative terms follow RFC 2119.

## 4. Approved Database Technologies

### 4.1 Technology catalogue

| Technology | Radar status | Permitted use |
|---|---|---|
| **Azure Database for PostgreSQL – Flexible Server** | **Adopt (default)** | All new transactional/relational workloads |
| Azure SQL Database / Azure SQL Managed Instance | Adopt | Vendor packages that require SQL Server; existing .NET applications already on SQL Server |
| **Azure Cosmos DB (NoSQL API)** | **Adopt — specific workloads only** | Only for the workload profiles in §5.2, with a reviewed access-pattern and partition-key design |
| Azure Cache for Redis | Adopt — cache only | Caching, session state, rate-limit counters; **never a system of record** |
| pgvector extension on PostgreSQL Flexible Server | Trial | Approved for AI retrieval (vector search) use cases only |
| MongoDB Atlas | Trial — Nordhaven only | Nordhaven TMS (APP-021) until migration into HSP; no new Harbourline use |
| Oracle Database | Contain | Existing systems only; no new Oracle databases |
| Oracle Database 12c | Retire — **2027-03-31** | FreightMaster TMS only, under an approved exception recorded in GOV-02 |
| Self-managed MongoDB, Cassandra or any database engine installed on VMs | **Prohibited** | None |

### 4.2 General rules

1. New transactional workloads MUST use **PostgreSQL Flexible Server** unless one of the conditions in §5 or §6 is met and documented.
2. Databases MUST be PaaS services. Installing a database engine on a virtual machine or in a container that Harbourline operates is **prohibited** (AP-11); this includes MongoDB, Cassandra, MySQL and PostgreSQL on VMs or on AKS.
3. Every database MUST belong to exactly one domain and one application ID. Other domains MUST access its data through APIs or events (STD-INT-001), never through direct connections.
4. Databases MUST use private endpoints only; public network access MUST be disabled (STD-CLD-007).
5. Databases holding Restricted data MUST use customer-managed keys (STD-DAT-004, STD-SEC-009) and be deployed in the region required by STD-DAT-005.
6. High availability and backup configuration MUST meet the service tier in STD-RES-015; Tier 1 PostgreSQL workloads MUST use zone-redundant HA and geo-redundant backup to the paired region.

## 5. When NoSQL (Azure Cosmos DB) Is Allowed

### 5.1 Principle

Relational is the default because most Harbourline domains — shipments, bookings, customs, billing — have rich relationships, need ad hoc querying and benefit from transactional integrity. Cosmos DB is permitted where its scale and access model are a genuine fit, not as a way to avoid schema design.

### 5.2 Permitted workload profiles

Cosmos DB (NoSQL API) MAY be used only when the workload matches **at least one** of the following profiles **and** passes the review in §5.3:

| Profile | Description | Example |
|---|---|---|
| NS-1 High-volume telemetry / time series with key-based access | Very high write rates (sustained > 2,000 writes/s or > 10M records/day), read by a known key and time range | Container Tracking Service (APP-090): ~40M events/day, partition key `/containerId`, 90-day TTL (ADR-0012) |
| NS-2 Globally distributed low-latency reads | Read latency < 10 ms p99 required in multiple regions, with residency permitting replication | Reference data read by regional portal stamps (non-personal) |
| NS-3 Schema-flexible documents with a single-partition access pattern | Documents whose structure varies by type, always read and written within one partition key | Per-carrier configuration documents keyed by `/carrierId` |

### 5.3 Mandatory review

1. The solution team MUST produce an **access-pattern and partition-key design** listing every read and write operation, its expected rate, the partition key used, and estimated RU/s consumption.
2. The design MUST be reviewed and approved by the Lead Data Architect or delegate in a **Tier 2 review** before provisioning. The review outcome is reported to the ARB.
3. Cross-partition queries MUST NOT be on any critical or high-frequency path.
4. TTL MUST be set for telemetry containers, with archival to ADLS Gen2 where history is required.
5. Where the data holds EU personal data, multi-region writes and replicas MUST be confined to West Europe and North Europe (STD-DAT-005).

### 5.4 When NoSQL is NOT allowed

Cosmos DB MUST NOT be used when any of the following apply:

- The data is the **system of record for a core relational domain** (shipments, bookings, customs declarations, invoices, customer accounts).
- The workload needs multi-entity transactions, joins or ad hoc reporting queries across partitions.
- The main reason given is "schema flexibility" without a single-partition access pattern.
- The team cannot state its partition key and access patterns up front.
- The motivation is developer familiarity with a document model; this is not a sufficient justification.

MongoDB API on Cosmos DB, Cassandra API and Gremlin API are not approved for new use; requests are treated as new technology (Tier 1).

## 6. Other Technology Rules

### 6.1 Azure SQL

Azure SQL MAY be used when a vendor package certifies only on SQL Server, or when an existing SQL Server application is re-platformed from the Baltimore data centre without redesign. New custom-built applications SHOULD NOT choose Azure SQL.

### 6.2 Redis

Azure Cache for Redis MUST be used only as a cache or ephemeral store. Applications MUST continue to function correctly (with degraded performance) if the cache is flushed. Persisting business data only in Redis is prohibited.

### 6.3 pgvector

The pgvector extension is in Trial and MAY be used for AI retrieval (embedding storage and similarity search) on PostgreSQL Flexible Server. Each use MUST be registered as an AI use case (`AIU-NNN`) and reviewed by the data architect. Dedicated vector database products are not approved.

### 6.4 Oracle

1. No new Oracle databases MAY be created. Existing Oracle databases MUST have a documented migration or retirement plan.
2. Oracle 12c MUST be retired by **2027-03-31**; FreightMaster TMS MUST hold an approved exception in GOV-02 covering Oracle 12c extended support until then.

### 6.5 MongoDB Atlas

MongoDB Atlas is permitted only for Nordhaven TMS (APP-021) in AWS eu-central-1 until its data is migrated into HSP (target Q2 2027). No other application MAY adopt MongoDB Atlas.

## 7. Decision Flow

1. Is it a vendor package that dictates the engine? → Use the vendor engine as PaaS (Azure SQL if SQL Server).
2. Does the workload match NS-1, NS-2 or NS-3 **and** have a defined partition key? → Cosmos DB, subject to Tier 2 review (§5.3).
3. Is it caching only? → Azure Cache for Redis.
4. Otherwise → PostgreSQL Flexible Server.

## 8. Compliance and Exceptions

1. Database selection is verified at ARB review; Azure Policy denies creation of unapproved database resource types in `hlg-corp` and `hlg-online` management groups.
2. Deviations MUST be requested through the GOV-01 exception process and recorded in GOV-02 with an `EXC-YYYY-NNN` identifier, a maximum 12-month term (renewable once) and a remediation plan.

## 9. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2024-12-01 | Lena Vogel | Initial standard following ADR-0024; PostgreSQL Flexible Server default; Oracle Contain |
| 1.1 | 2025-02-15 | Lena Vogel | Cosmos DB workload profiles NS-1..NS-3 based on ADR-0012 experience; self-managed NoSQL prohibited |
| 1.2 | 2025-04-01 | Lena Vogel | MongoDB Atlas Trial restricted to Nordhaven; Redis cache-only rule |
| 1.3 | 2025-06-01 | Lena Vogel | pgvector added as Trial for AI retrieval; Tier 2 partition-key review made mandatory; decision flow; ARB-2025-022 |
