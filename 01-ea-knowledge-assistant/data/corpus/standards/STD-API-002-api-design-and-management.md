---
doc_id: STD-API-002
title: API Design & Management Standard
doc_type: standard
togaf_phase: Preliminary
version: "1.4"
status: Approved
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2025-003)
effective_date: 2025-01-15
next_review: 2026-10-15
classification: Internal
related: [AP-09, AP-12, AP-14, AP-15, STD-INT-001, STD-IAM-008, STD-SEC-009, STD-OBS-010, STD-TLC-014, ADR-0019, RA-01, RA-02, GOV-01, GOV-02]
---

# STD-API-002 — API Design & Management Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard sets the rules for designing, securing, versioning, publishing and retiring application programming interfaces (APIs) at Harbourline Logistics Group. It gives consumers — internal teams, customers integrating with Harbourline Digital, and logistics partners — a predictable experience across every API, and it enables the Harbourline API Gateway to enforce security and traffic policy consistently.

It is the detailed companion to pattern INT-P3 (Synchronous Request/Response via API Gateway) in STD-INT-001.

## 2. Scope

This standard applies to:

- All APIs exposed across a domain boundary, whether consumed internally, by customers or by partners.
- All APIs consumed by Harbourline Connect (APP-050) and its backend-for-frontend (BFF).
- APIs provided by SaaS or packaged products where Harbourline controls the façade (the façade MUST comply even if the vendor's native API does not).

Service-to-service calls within a single bounded context are out of scope, except §6 (security) and §8 (observability), which always apply.

## 3. Related Principles and Normative References

- **AP-09 API-First for Synchronous Access** — synchronous access to another domain's data or functions is through a published, contract-first API.
- **AP-12 Zero Trust Access** — every call is authenticated and authorised; network location grants no trust.
- **AP-14 Observable by Default** and **AP-15 Everything as Code**.
- **STD-INT-001** (pattern INT-P3), **STD-IAM-008** (identity), **STD-SEC-009** (TLS and certificates), **STD-OBS-010** (telemetry), **STD-TLC-014** (radar status of GraphQL and SOAP).
- **ADR-0019** Azure API Management as the Single API Gateway.
- OpenAPI Specification 3.1; RFC 9457 (Problem Details for HTTP APIs); RFC 2119 for normative language.

## 4. API Style and Contract

### 4.1 Architectural style

1. APIs MUST be RESTful over HTTPS using JSON (`application/json`) unless an exception applies.
2. **GraphQL** is rated **Trial** and MAY be used **only** as a backend-for-frontend for the Harbourline Connect portal. GraphQL MUST NOT be exposed to partners or used for domain-to-domain integration.
3. **SOAP** is rated **Contain**: existing SOAP services (principally legacy FreightMaster TMS and some customs integrations) MAY continue, but new SOAP APIs MUST NOT be created.
4. gRPC MAY be used within a bounded context but MUST NOT be published through the gateway to external consumers.

| Style | Radar status | Permitted use |
|---|---|---|
| REST + OpenAPI 3.1 | Adopt | Default for all published APIs |
| GraphQL | Trial | Harbourline Connect BFF only |
| SOAP/WSDL | Contain | Existing services only; no new APIs |
| gRPC | — | Internal to a bounded context only |

### 4.2 Contract-first design

1. Every API MUST have an **OpenAPI 3.1** contract stored in the owning team's Git repository and reviewed before implementation starts.
2. Contracts MUST be linted in CI against the Harbourline API ruleset; a failing lint MUST block the merge.
3. Each contract MUST declare `info.contact` (owning team), `x-app-id` (CMDB application ID, e.g. `APP-022`) and `x-data-classification`.

### 4.3 Resource naming and URIs

1. Resource names MUST be plural nouns in kebab-case: `/v1/shipments`, `/v1/customs-declarations`, `/v1/containers/{containerId}/telemetry`.
2. Verbs MUST NOT appear in paths except for well-defined actions modelled as sub-resources, e.g. `POST /v1/bookings/{bookingId}/cancellation`.
3. Query parameters MUST use camelCase; collection endpoints MUST support cursor-based pagination (`limit`, `cursor`) with a maximum `limit` of 200.
4. Errors MUST be returned as RFC 9457 Problem Details with a Harbourline error code (e.g. `HLG-SHP-4041`).

## 5. Versioning and Lifecycle

1. APIs MUST use **URI major versioning** (`/v1/`, `/v2/`). Minor, backward-compatible changes (adding optional fields or endpoints) MUST NOT change the major version.
2. Breaking changes — removing or renaming fields, changing types, tightening validation — REQUIRE a new major version.
3. A deprecated version MUST remain available for at least **6 months** after the deprecation notice. Notice MUST be given through the developer portal, the `Deprecation` and `Sunset` HTTP response headers, and direct communication to registered consumers.
4. APIs consumed by external customers or partners SHOULD receive 12 months' notice where contractual terms permit.
5. No more than two major versions of an API SHOULD be live at once.

## 6. Security

1. All APIs MUST be published through the **Harbourline API Gateway** (Azure API Management Premium, APP-121). Backends MUST accept traffic only from the gateway via private networking; direct public exposure of a backend is prohibited.
2. Authentication MUST use **OAuth 2.0** tokens issued by Microsoft Entra ID (STD-IAM-008):
   - **Client credentials** flow for system-to-system and partner integration.
   - **Authorization code with PKCE** for user-facing applications, including customer users authenticated through Harbourline Connect ID (Entra External ID).
   - The implicit flow and resource-owner password flow MUST NOT be used.
3. API keys (APIM subscription keys) MAY be used for consumer identification and quotas but MUST NOT be the sole authentication mechanism.
4. The gateway MUST validate JWT signature, audience, issuer and expiry; backends MUST enforce fine-grained authorisation using scopes or app roles (e.g. `Shipments.Read`, `Bookings.Write`).
5. Transport MUST meet STD-SEC-009 (TLS 1.2 minimum, TLS 1.3 preferred).
6. Responses MUST NOT include Restricted data fields unless the caller's scope explicitly authorises them and the API contract declares the classification.

## 7. Traffic Management

1. The default rate limit is **1,000 requests per minute per client application**, enforced at the gateway.
2. Higher limits MAY be granted per product subscription on evidence of need, approved by the API product owner and recorded in the APIM product configuration (managed as code, AP-15).
3. When limits are exceeded the gateway MUST return HTTP 429 with a `Retry-After` header.
4. Commands that create or change state (`POST`, `PATCH`) SHOULD accept an `Idempotency-Key` header; APIs used by partners for booking or customs submission MUST support it.
5. Gateway caching MAY be used for reference data (ports, UN/LOCODEs, currency codes) with a maximum TTL of 15 minutes.

## 8. Observability and Documentation

1. APIs MUST propagate W3C trace context and emit OpenTelemetry telemetry per STD-OBS-010.
2. Every API MUST expose `/health/live` and `/health/ready` endpoints to the platform (not published externally).
3. Every published API MUST appear in the APIM developer portal with its OpenAPI contract, example requests, rate-limit tier and support contact.
4. Request and response bodies MUST NOT be logged at the gateway where they may contain personal data.

## 9. When to Use / When Not to Use an API

| Use an API (INT-P3) when | Do not use an API when |
|---|---|
| A user is waiting for a response (quote, booking confirmation) | A consumer only needs to know that something changed — subscribe to an event (INT-P1) |
| A command must be validated synchronously | A consumer needs high-volume reads of another domain's data — build a read model (INT-P2) |
| A partner requires on-demand lookups (e.g. `GET /v1/shipments/{id}/milestones`) | Bulk data is needed for analytics — use INT-P5 into Tidewater |

## 10. Compliance and Exceptions

1. API contracts are checked automatically in CI; the ARB or delegated reviewers verify gateway publication and security configuration during Tier 1 and Tier 2 reviews.
2. Non-compliance that cannot be remediated before go-live MUST be raised through the GOV-01 exception process. Approved exceptions (`EXC-YYYY-NNN`) are time-bound (maximum 12 months, renewable once), carry a remediation plan and are recorded in GOV-02.
3. Requests to use GraphQL outside the portal BFF will be treated as new technology and require Tier 1 review.

## 11. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2023-09-01 | Amara Osei | Initial standard: REST, OpenAPI 3.0, URI versioning |
| 1.2 | 2024-07-01 | Amara Osei | Aligned with ADR-0019: APIM as single gateway; OAuth 2.0 via Entra ID mandatory |
| 1.3 | 2024-10-15 | Amara Osei | Moved to OpenAPI 3.1; GraphQL set to Trial for portal BFF; SOAP set to Contain |
| 1.4 | 2025-01-15 | Amara Osei | Default rate limit 1,000 req/min per client; 6-month deprecation minimum; RFC 9457 errors; ARB-2025-003 |
