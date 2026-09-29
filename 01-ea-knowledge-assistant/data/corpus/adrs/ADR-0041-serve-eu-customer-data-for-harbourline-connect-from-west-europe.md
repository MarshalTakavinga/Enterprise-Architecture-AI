---
doc_id: ADR-0041
title: Serve EU Customer Data for Harbourline Connect from West Europe
doc_type: adr
version: "1.0"
status: Accepted
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2025-033)
effective_date: 2025-09-02
next_review: 2027-09-02
classification: Internal
related: [AP-02, AP-06, AP-10, AP-12, STD-DAT-005, STD-DAT-004, STD-CLD-007, STD-IAM-008, STD-RES-015, ADR-0019, ADR-0030, RA-02, H-01, APP-050, APP-022]
---

# ADR-0041 — Serve EU Customer Data for Harbourline Connect from West Europe

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2025-09-02 |
| ARB decision | ARB-2025-033 (session of Thursday 2025-08-28), Approved with Conditions |
| Deciders | David Okafor (Chair), Kenji Watanabe, Lena Vogel, Priya Raman, Amara Osei |
| Consulted | Marieke de Vries (DPO), Harbourline Digital portal team, Grace Liu, Harbourline Canada IT |
| Review tier | Tier 1 (cross-border data transfer, customer-facing Tier 1 service) |

## 2. Context

Harbourline Connect (APP-050) is currently deployed as a single instance in Azure East US 2. About 41% of its ~38,000 daily active users belong to EU customer accounts (Harbourline Europe B.V. and Nordhaven Freight GmbH customers), and 9% to Canadian accounts, several of whose contracts require Canadian data residency.

The portal stores user profiles (names, business emails, phone numbers), notification preferences and the shipment-status read model (ADR-0030), which includes consignee contact names. Under STD-DAT-005, personal data of EU data subjects must be stored and processed in West Europe (DR: North Europe). A DPO review in July 2025 concluded that relying on transfer mechanisms for bulk portal data is not acceptable, particularly as EU lanes moving to HSP in 2027 will greatly increase EU personal data in the portal. REQ-HSP-021 requires EU personal data for the shipment platform to reside in West Europe.

EU users see 95-110 ms latency to East US 2 (15-25 ms to West Europe); EU p95 page load is 3.4 s versus 1.9 s in the US.

## 3. Decision Drivers

1. Residency of EU (and contractually Canadian) customer data in its jurisdiction (AP-06, STD-DAT-005).
2. Avoid reliance on cross-border transfers for routine portal operation.
3. A single codebase and release pipeline for all regions.
4. Tier 1 resilience (RTO 1 h, RPO 15 min) in each region.
5. Improved latency for EU users.
6. Cost and operational effort for a 6-person portal team plus platform support.

## 4. Considered Options

- **Option A — Status quo with TIA and SCCs**: keep a single US deployment and document transfers.
- **Option B — Regional deployment stamps (US, EU, CA)**, each a full copy of the portal stack with its own data stores; global routing via Azure Front Door based on the account's home region.
- **Option C — Global single deployment with data partitioned by region** (EU data in West Europe databases, compute in US).

### 4.1 Comparison

| Criterion | A — Status quo + TIA | B — Regional stamps | C — Central compute, regional data |
|---|---|---|---|
| EU data at rest in EU | No | Yes | Yes |
| EU data processed in EU | No | Yes | No (compute in US) |
| DPO assessment | Not acceptable at 2027 volumes | Acceptable | Not acceptable (processing still transfers) |
| EU p95 page load (est.) | 3.4 s | 1.8 s | 3.6 s (cross-region DB calls) |
| Additional run cost | ~USD 0 | ~USD 21k/month (EU + CA stamps) | ~USD 9k/month |
| Operational complexity | Low | Medium (3 stamps, one pipeline) | High (cross-region data access logic) |
| Extensible to new jurisdictions | No | Yes | Partially |

## 5. Decision Outcome

**Chosen option: B — Regional deployment stamps for US, EU and CA.** The EU stamp runs in **Azure West Europe** with DR in North Europe; the US stamp stays in East US 2 (DR Central US); the CA stamp runs in Canada Central (DR Canada East).

Design rules:

1. Each stamp is an identical deployment of the RA-02 pattern (Front Door + WAF → private AKS → PostgreSQL Flexible Server via private endpoint, Key Vault, managed identities), provisioned from the same Terraform modules and released through one GitOps pipeline.
2. **Routing:** Azure Front Door routes each authenticated session to the stamp matching the account's **home region**, carried as a claim issued by Harbourline Connect ID (Entra External ID). Unauthenticated users receive static content only.
3. Each stamp's shipment-status read model consumes only events for accounts homed in that region; EU-homed events are consumed from the West Europe side of the Event Backbone.
4. No personal data replicates between stamps. Cross-region operational reporting uses aggregated or anonymised data in Tidewater only.
5. Group support staff access other regions' stamps only through PIM-approved, logged sessions.
6. Adding a stamp for a new jurisdiction requires a change request and Tier 1 review.

## 6. Consequences

### 6.1 Positive

- EU customer personal data is stored and processed in West Europe, satisfying AP-06, STD-DAT-005 and REQ-HSP-021.
- EU page-load p95 expected to fall from 3.4 s to about 1.8 s.

### 6.2 Negative

- Run cost rises by ~USD 21k/month (~USD 250k/year) for two extra stamps, including APIM units in additional regions.
- Three production stamps triple deployment verification, DR testing (annual Tier 1 test per stamp) and on-call surface.
- Customers with users in several regions (global shippers) must be assigned one home region; users outside it will see higher latency. About 60 enterprise accounts are affected.
- Moving an account between regions is a manual, DPO-approved migration.
- Staff covering accounts in several regions must switch stamps.

### 6.3 Neutral

- The Harbourline API Gateway (ADR-0019) already runs multi-region and is extended to Canada Central as part of this work.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Home-region claim in Harbourline Connect ID | Priya Raman | 2025-11-30 |
| Provision EU and CA stamps via Terraform | Kenji Watanabe | 2026-02-28 |
| Migrate EU accounts and verify no residual EU personal data in East US 2 | Lena Vogel / Marieke de Vries | 2026-05-31 |
| Update RA-02 with regional stamp model | Kenji Watanabe | 2025-12-31 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-06 Data Residency Follows Jurisdiction | Compliant. |
| STD-DAT-005 | EU in West Europe / North Europe DR; Canada in Canada Central / East; no cross-border transfer for routine operation. |
| AP-12 / STD-IAM-008 | Home-region claim from Entra External ID; PIM for cross-region support access. |
| STD-RES-015 | Each stamp meets Tier 1 targets with paired-region DR. |
| STD-CLD-007 | Approved regions only. |

## 8. Links

- RA-02 Cloud-Native Application on the Azure Landing Zone
- ADR-0030 Event-Carried State Transfer for Shipment Status to Harbourline Connect
- ADR-0019 Azure API Management as the Single API Gateway
- ARS-01 (REQ-HSP-021)
- Subsequent change request: H-01 CR-2026-014 (UAE deployment stamp)
- ARB log entry ARB-2025-033
