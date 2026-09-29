---
doc_id: ADR-0024
title: PostgreSQL Flexible Server as Default Relational Database
doc_type: adr
version: "1.0"
status: Accepted
owner: Lena Vogel, Lead Data Architect
approved_by: Architecture Review Board (ARB-2024-044)
effective_date: 2024-11-19
next_review: 2026-11-19
classification: Internal
related: [AP-10, AP-11, AP-15, STD-DB-006, STD-SEC-009, STD-RES-015, STD-TLC-014, ADR-0012, ADR-0038, RA-02, APP-020, APP-022]
---

# ADR-0024 — PostgreSQL Flexible Server as Default Relational Database

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-11-19 |
| ARB decision | ARB-2024-044 (session of Thursday 2024-11-14), Approved |
| Deciders | David Okafor (Chair), Lena Vogel, Kenji Watanabe, Priya Raman, Amara Osei |
| Consulted | Grace Liu (HSP programme), Kestrel Digital Partners lead architect, DBA team (5 FTE), Rachel Kim (CFO office) |
| Review tier | Tier 1 (enterprise default technology) |

## 2. Context

Harbourline's relational estate is dominated by Oracle Database: 46 Oracle instances, including the FreightMaster TMS (APP-020) on Oracle 12c, with annual Oracle support of about USD 3.1M. There is also a scattering of SQL Server on VMs and a few Azure SQL databases from vendor packages. There is no stated default, so each project team picks its own engine, and DBA skills are spread thinly across three products.

The Harbourline Shipment Platform (APP-022), now funded under Horizon 2028, will introduce around 25 microservices, each owning its own database. The programme needs a default relational engine before the first services are built in Q1 2025. The expected profile per service is modest (under 500 GB, a few thousand transactions/s at peak), with the booking and milestone services the busiest at ~3,000 writes/s at peak season.

## 3. Decision Drivers

1. Managed service with zone-redundant HA and point-in-time restore (AP-11; Tier 1 RTO 1 h / RPO 15 min under STD-RES-015).
2. Portability across Azure and AWS, and freedom from proprietary licensing (AP-10).
3. Licence and run cost across ~25 new databases plus migrated ones.
4. Developer familiarity for Java 21 / .NET 8 teams and the systems integrator.
5. Extension ecosystem (JSONB, PostGIS for port geofences, pgvector for future retrieval workloads).
6. Support for the transactional outbox and logical-replication-based CDC.

## 4. Considered Options

- **Option A — Azure Database for PostgreSQL Flexible Server.**
- **Option B — Azure SQL Database** (vCore, General Purpose / Business Critical).
- **Option C — Oracle Database** (Oracle Database@Azure or Oracle on Azure VMs with existing licences).

### 4.1 Comparison

Cost figures are for a reference fleet of 30 databases, average 4 vCores, zone-redundant HA, over 3 years.

| Criterion | A — PostgreSQL Flexible Server | B — Azure SQL Database | C — Oracle |
|---|---|---|---|
| 3-year cost (est.) | USD 1.9M | USD 3.0M (General Purpose, zone-redundant) | USD 5.8M incl. licences and support |
| Managed HA / PITR | Zone-redundant HA, 35-day PITR | Built-in, strong | Depends on deployment model; VMs self-managed |
| Portability | High (open source; AWS RDS/Aurora compatible) | Low-moderate | Low |
| Logical replication for CDC | Native (pgoutput) | CDC feature; Debezium supported | LogMiner; licence and effort heavy |
| Extensions | JSONB, PostGIS, pgvector | Limited | Proprietary options, extra cost |
| Team skills | Integrator strong; internal DBAs moderate | Internal strong for SQL Server | Internal DBAs strongest |
| Max single-server write headroom | Adequate to 64 vCores | Higher on Business Critical | High |

## 5. Decision Outcome

**Chosen option: A — Azure Database for PostgreSQL Flexible Server is the default relational database** for new applications and for re-platformed in-house applications.

- **Azure SQL Database** remains Adopt for vendor packages that require SQL Server; it is not the default for in-house builds.
- **Oracle Database** moves to **Contain**: no new Oracle databases; existing ones may continue until their application is retired. Oracle 12c is set to Retire (2027-03-31) on the radar.
- Standard configuration: PostgreSQL 16, zone-redundant HA, private endpoint only, Entra ID authentication with managed identities, customer-managed keys for Restricted data, geo-redundant backup for Tier 1.
- Each HSP microservice owns its own database (or schema-isolated database on a shared server for services under 50 GB), never shared across domains.

Azure SQL was the strongest alternative on raw capability and existing skills, but costs ~58% more for the reference fleet and ties new builds to a proprietary engine. Oracle was rejected on cost and portability.

## 6. Consequences

### 6.1 Positive

- Estimated USD 1.1M saving over three years versus Azure SQL for the HSP fleet, and a path to eliminate most Oracle support spend when FreightMaster retires.
- Native logical replication supports the outbox + CDC approach later formalised in ADR-0038.
- pgvector and PostGIS available without new products.

### 6.2 Negative

- Internal DBA team is Oracle-centric; 5 DBAs need PostgreSQL training (~USD 40k, 3 months) and on-call confidence will lag for the first year.
- Flexible Server has limits relative to Oracle RAC (single writer; read replicas are asynchronous); the busiest services must be designed to shard by domain rather than scale up indefinitely.
- Major-version upgrades are customer-initiated and need a test cycle; a fleet of 25+ servers makes this recurring work.
- PL/SQL logic in FreightMaster (~180k lines) cannot be ported; it must be re-implemented in HSP services, not migrated.

### 6.3 Neutral

- Cosmos DB remains the choice for telemetry-style workloads as decided in ADR-0012; this ADR does not change that.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Update STD-DB-006 with default, Contain and Retire statuses | Lena Vogel | 2025-01-31 |
| Terraform module for standard Flexible Server configuration | Kenji Watanabe | 2025-01-15 |
| DBA PostgreSQL training and runbooks | Lena Vogel | 2025-03-31 |
| Update radar entries (STD-TLC-014) | David Okafor | 2024-11-28 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-10 Cloud-Smart and Portable | Strongly compliant; open-source engine available on both clouds. |
| AP-11 Managed Services | Compliant. |
| AP-15 Everything as Code | Provisioned via Terraform modules only. |
| STD-SEC-009 | CMK for Restricted data, TLS 1.2+. |
| STD-RES-015 | Zone-redundant HA and geo-backup meet Tier 1 targets. |

## 8. Links

- STD-DB-006 Database Technology Selection Standard
- RA-02 Cloud-Native Application on the Azure Landing Zone
- ADR-0012 Use Azure Cosmos DB for Container Telemetry Storage
- ADR-0038 Transactional Outbox for Publishing Domain Events from HSP
- ARB log entry ARB-2024-044
