---
doc_id: ADR-0019
title: Azure API Management as the Single API Gateway
doc_type: adr
version: "1.0"
status: Accepted
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2024-022)
effective_date: 2024-06-04
next_review: 2026-06-04
classification: Internal
related: [AP-09, AP-10, AP-11, AP-12, AP-14, STD-API-002, STD-INT-001, STD-IAM-008, STD-RES-015, ADR-0015, ADR-0041, RA-01, RA-02, APP-121]
---

# ADR-0019 — Azure API Management as the Single API Gateway

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-06-04 |
| ARB decision | ARB-2024-022 (session of Thursday 2024-05-30), Approved with Conditions |
| Deciders | David Okafor (Chair), Amara Osei, Priya Raman, Kenji Watanabe, Lena Vogel |
| Consulted | Harbourline Digital (portal team), Nordhaven IT, Hannah Brennan (CISO) |
| Review tier | Tier 1 (enterprise platform, cost > USD 500k) |

## 2. Context

Harbourline exposes roughly 180 APIs to internal consumers and about 40 to external parties (shippers, carriers, customs brokers). They are published through four different mechanisms: MuleSoft API Manager, a legacy Azure API Management Developer-tier instance used by the portal, AWS API Gateway at Nordhaven, and directly exposed application endpoints. Consequences observed in the last 12 months:

- Three incidents in which an unauthenticated endpoint was reachable from the internet.
- No consistent rate limiting; one shipper's integration generated 11,000 requests/min against FreightMaster during peak season, degrading booking for all users.
- No single developer portal or catalogue; partners receive credentials by email.

The ARB needs one gateway through which all synchronous APIs are published, as the enforcement point for STD-API-002 and INT-P3 in STD-INT-001. Expected load by 2026: 4,500 requests/s peak across all APIs, gateway latency overhead < 15 ms p95, deployed in at least US and EU regions.

## 3. Decision Drivers

1. Native integration with Microsoft Entra ID and Entra External ID for OAuth 2.0 (AP-12, STD-IAM-008).
2. Multi-region active-active deployment with private (VNet-injected) back ends.
3. Policy-based rate limiting, quotas, transformation and JWT validation without custom code.
4. Developer portal for partner onboarding.
5. Fit with the Azure-primary landing zone and Terraform (AP-10, AP-15).
6. Total cost and operational effort for a small platform team (3 FTE).

## 4. Considered Options

- **Option A — Azure API Management Premium, multi-region** (East US 2 primary, West Europe secondary, additional units per region).
- **Option B — Kong Enterprise** self-hosted on AKS with Kong Konnect control plane.
- **Option C — AWS API Gateway** as enterprise standard, extending Nordhaven's usage.

### 4.1 Comparison

| Criterion | A — APIM Premium | B — Kong Enterprise | C — AWS API Gateway |
|---|---|---|---|
| Entra ID / External ID integration | Native policies | Plugin; OIDC config per route | Via Cognito federation or Lambda authorisers |
| Multi-region + VNet back ends | Built-in (Premium) | Self-built across AKS clusters | Per-region; Azure back ends need cross-cloud connectivity |
| Gateway latency overhead (PoC, p95) | 9 ms | 5 ms | 14 ms (+ cross-cloud hop ~25 ms to Azure) |
| Developer portal | Included | Included (Konnect) | Basic; custom build needed |
| Operational effort | Low (managed) | High (upgrade, scaling, plugin lifecycle) | Low, but second cloud skill set |
| 3-year cost (est.) | USD 1.45M (4 units, 2 regions) | USD 1.1M licence + ~USD 0.6M ops effort | USD 0.9M + egress and connectivity ~USD 0.35M |
| Landing zone alignment | Full | Partial | Poor (Azure primary) |

## 5. Decision Outcome

**Chosen option: A — Azure API Management Premium, multi-region**, designated the **Harbourline API Gateway** (APP-121).

Kong offered the lowest latency and good portability, but running it ourselves conflicts with AP-11 and would need at least two additional platform engineers. AWS API Gateway would place the enforcement point on the secondary cloud while nearly all back ends are on Azure, adding cross-cloud latency and egress cost.

Rules and conditions:

1. **All** synchronous APIs, internal and external, MUST be published through the Harbourline API Gateway. Direct exposure of application endpoints is prohibited.
2. APIM runs in internal VNet mode; external traffic enters via Azure Front Door with WAF.
3. Default rate limit of 1,000 requests/min per client, overridable per product with ARB-registered justification.
4. APIM configuration managed as code (Terraform + APIOps pipeline); portal changes are not permitted in production.
5. Nordhaven's AWS API Gateway may continue for Nordhaven-internal APIs until the Nordhaven TMS is migrated; any API consumed outside Nordhaven MUST be fronted by APIM.
6. MuleSoft API Manager is not to be used for new APIs.

## 6. Consequences

### 6.1 Positive

- Single enforcement point for authentication, throttling and logging; closes the unauthenticated-exposure gap.
- Consistent partner onboarding via a developer portal with self-service subscription keys plus OAuth.
- Gateway logs flow into Log Analytics and Sentinel, supporting AP-14.

### 6.2 Negative

- Premium tier is expensive: ~USD 2,800 per unit per month; four units is ~USD 134k/year before scale-out, and each additional region adds at least one unit.
- Premium scale-out takes 30-45 minutes; sudden spikes rely on rate limiting rather than elastic scaling.
- APIM policy XML is Azure-specific; migrating policies to another gateway would be a rewrite (accepted lock-in, documented against AP-10).
- Migrating ~220 APIs is estimated at 14 engineer-months; teams must also adopt OpenAPI contracts where none exist today.

### 6.3 Neutral

- GraphQL pass-through is supported but GraphQL remains outside this decision; its status is governed by STD-API-002.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Provision APIM Premium in East US 2 and West Europe via Terraform | Kenji Watanabe | 2024-08-30 |
| Revise STD-API-002 to mandate gateway publication and rate-limit defaults | Amara Osei | 2024-12-31 |
| Migrate external partner APIs first (40 APIs) | Amara Osei | 2025-03-31 |
| Sentinel analytics rules for gateway anomalies | Priya Raman | 2024-10-31 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-09 API-First for Synchronous Access | Provides the governed channel the principle requires. |
| AP-12 Zero Trust Access | Every call authenticated and authorised at the gateway; no implicit network trust. |
| AP-10 Cloud-Smart and Portable | Partially; policy lock-in accepted, API contracts remain OpenAPI and portable. |
| AP-11 Managed Services | Compliant. |
| STD-IAM-008 | OAuth via Entra ID / External ID. |
| STD-RES-015 | Multi-region deployment supports Tier 1 consumers. |

## 8. Links

- STD-API-002 API Design & Management Standard; STD-INT-001 §INT-P3
- RA-01 Event-Driven Domain Integration; RA-02 Cloud-Native Application on the Azure Landing Zone
- ADR-0015 Sunset MuleSoft ESB and Freeze New Flows
- ADR-0041 Serve EU Customer Data for Harbourline Connect from West Europe
- ARB log entry ARB-2024-022
