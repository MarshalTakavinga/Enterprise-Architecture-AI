---
doc_id: ADR-0015
title: Sunset MuleSoft ESB and Freeze New Flows
doc_type: adr
version: "1.0"
status: Accepted
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2024-035)
effective_date: 2024-09-10
next_review: 2025-09-10
classification: Internal
related: [AP-03, AP-08, AP-09, AP-11, STD-INT-001, STD-API-002, STD-EVT-003, STD-TLC-014, ADR-0007, ADR-0019, ADR-0038, RA-01, APP-122, APP-120, APP-121]
---

# ADR-0015 — Sunset MuleSoft ESB and Freeze New Flows

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-09-10 |
| ARB decision | ARB-2024-035 (session of Thursday 2024-09-05), Approved |
| Deciders | David Okafor (Chair), Amara Osei, Priya Raman, Kenji Watanabe, Lena Vogel, Tomasz Nowak |
| Consulted | Elena Marsh (CIO), Rachel Kim (CFO), Grace Liu, MuleSoft platform team (4 FTE) |
| Review tier | Tier 1 (platform retirement affecting all domains) |

## 2. Context

MuleSoft Anypoint (APP-122) has been Harbourline's enterprise service bus since 2017. In September 2024 it runs 310 production flows on 38 vCores across two CloudHub regions, with an annual subscription of approximately USD 1.9M plus USD 0.7M in platform team cost. The current contract term ends 2026-12-31.

Since ADR-0007 (Confluent Cloud event backbone) and ADR-0019 (Azure API Management as single API gateway), Harbourline has two strategic integration platforms that together cover asynchronous and synchronous needs. MuleSoft now overlaps both. An inventory completed in August 2024 classified the 310 flows as:

| Category | Flows | Target pattern |
|---|---|---|
| Scheduled polling / data copy between domains | 142 | INT-P1 / INT-P2 via Event Backbone |
| Synchronous API façades over back-end systems | 71 | INT-P3 via Azure API Management |
| Partner EDI orchestration around Sterling B2B | 38 | INT-P4 (unchanged pattern, flow logic moved to Sterling or partner APIs) |
| Batch extracts to reporting | 34 | INT-P5 into Tidewater |
| Obsolete / no traffic in 90 days | 25 | Decommission |

Teams continue to request new MuleSoft flows because the platform is familiar and quick for simple mappings. Every new flow extends the tail of the migration.

## 3. Decision Drivers

1. Avoid renewing a USD 1.9M/year subscription for a platform that duplicates strategic capabilities.
2. Stop growth of point-to-point and polling integrations that conflict with AP-08.
3. Provide a firm, dated signal so delivery teams plan migrations into their roadmaps.
4. Keep business risk acceptable: 19 flows support Tier 1 processes (customs filing, invoicing).
5. Retain or redeploy MuleSoft platform skills.

## 4. Considered Options

- **Option A — Renew MuleSoft and keep it as a strategic platform** alongside Confluent and APIM.
- **Option B — Contain now, freeze new flows on 2025-06-30, decommission by 2026-12-31**, migrating to INT-P1/INT-P3.
- **Option C — Immediate freeze (2024-10-01) with decommission by 2025-12-31.**

### 4.1 Comparison

| Criterion | A — Renew | B — Freeze 2025-06-30, exit 2026-12-31 | C — Immediate freeze, exit 2025-12-31 |
|---|---|---|---|
| Subscription cost FY2027 onward | USD 1.9M/yr | USD 0 | USD 0 |
| One-off migration cost (est.) | None | USD 3.4M over 27 months | USD 3.9M over 15 months (premium for compressed schedule) |
| Alignment with AP-08 / STD-INT-001 | Poor | Good | Good |
| Delivery disruption | None | Moderate | High; clashes with shipment platform build |
| Risk to Tier 1 flows | Low | Low-moderate | High |
| Contract fit | Renewal needed 2026 | Matches contract end | Pays for 12 unused months |

## 5. Decision Outcome

**Chosen option: B.** MuleSoft Anypoint moves to **Contain** on the technology radar (STD-TLC-014) immediately, with these binding rules:

1. **No new MuleSoft flows after 2025-06-30.** Between now and that date, new flows require Tier 2 review and a named migration target.
2. **Decommission by 2026-12-31**, aligned with contract expiry. No renewal will be signed.
3. Replacement patterns: cross-domain asynchronous integration moves to **INT-P1 Domain Event Publication** (and INT-P2 where consumers need local state); synchronous façades move to **INT-P3 via the Harbourline API Gateway**. Batch reporting flows move to INT-P5; partner EDI stays on INT-P4.
4. Migration is sequenced in waves: obsolete flows first (Q4 2024), then polling flows whose source domain already publishes events, then Tier 1 flows last with parallel run of at least 4 weeks each.

Option C was rejected because the compressed schedule would compete for the same integration engineers needed for the shipment platform's first release, and the saving on the final contract year does not offset the premium or risk.

## 6. Consequences

### 6.1 Positive

- Projected run-cost saving of ~USD 2.6M/year from FY2027 (subscription plus platform team redeployed), contributing to the IT run-cost reduction target.
- Removes a large source of polling latency between systems.
- Integration estate converges on two platforms with clear roles.

### 6.2 Negative

- One-off migration budget of USD 3.4M must be found within programme funding; it is not self-funding until 2027.
- Dual running of MuleSoft, Confluent and APIM through 2026 raises integration run cost temporarily by an estimated 14%.
- Some flows embed undocumented business rules (e.g., carrier code mappings); each needs discovery before migration, and effort estimates carry ±30% uncertainty.
- Four MuleSoft specialists face role change; two have indicated they may leave, which would slow Tier 1 migrations.
- Hard contract date creates schedule risk: if migrations slip, a short-term extension would be negotiated from a weak position.

### 6.3 Neutral

- Templating and transformation logic currently in MuleSoft must find new homes inside owning domain services; no central transformation layer replaces it.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Publish flow inventory with owner and target pattern per flow | Amara Osei | 2024-10-15 |
| Update STD-INT-001 to prohibit new MuleSoft flows after 2025-06-30 | Amara Osei | next revision |
| Set radar status Contain, sunset 2026-12-31 | David Okafor | 2024-09-19 |
| Reskilling plan for MuleSoft team (Kafka, APIM) | Amara Osei | 2024-11-30 |
| Quarterly burn-down report to ARB | Samuel Adeyemi | quarterly |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-08 Event-First Integration Between Domains | Strengthens compliance by removing polling integrations. |
| AP-09 API-First for Synchronous Access | Synchronous façades move to the governed gateway. |
| AP-03 Reuse, then Buy, then Build | Reuses already-adopted platforms instead of buying more ESB capacity. |
| STD-INT-001 | Codifies the freeze as a prohibited practice. |
| STD-TLC-014 | MuleSoft Anypoint: Contain, sunset 2026-12-31. |

## 8. Links

- ADR-0007 Adopt Confluent Cloud as the Enterprise Event Backbone
- ADR-0019 Azure API Management as the Single API Gateway
- ADR-0038 Transactional Outbox for Publishing Domain Events from HSP
- STD-INT-001 Integration Patterns Standard; RA-01 Event-Driven Domain Integration
- ARB log entry ARB-2024-035
