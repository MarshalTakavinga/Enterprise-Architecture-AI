---
doc_id: H-01
title: Change Request CR-2026-014 — Add UAE Deployment Stamp for Harbourline Connect
doc_type: togaf_deliverable
togaf_phase: H
version: "1.1"
status: Approved
owner: Omar Haddad, Head of IT, Harbourline Gulf
approved_by: Architecture Review Board (ARB-2026-024)
effective_date: 2026-07-16
next_review: 2027-01-14
classification: Internal
related: [H-02, ARS-01, F-01, ADD-01, AP-01, AP-06, STD-DAT-005, STD-CLD-007, STD-RES-015, ADR-0041, RA-02]
---

# H-01 — Change Request CR-2026-014 — Add UAE Deployment Stamp for Harbourline Connect

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Request Details

| Field | Value |
|---|---|
| Change request ID | CR-2026-014 |
| Title | Add UAE deployment stamp for Harbourline Connect (APP-050) |
| Raised by | Omar Haddad, Head of IT, Harbourline Gulf |
| Date raised | 2026-06-11 |
| Business sponsor | Michael Torres, VP Port & Terminal Services (JEA-T4 customers) |
| Affected application(s) | Harbourline Connect (APP-050); HSP (APP-022); Customer Notification Service (APP-055) |
| Change category | Architecture change — new deployment region for an existing Tier 1 system |
| Requested review tier | Tier 1 (new region, personal data residency, cost > USD 500k) |
| Assessment | H-02 Requirements Impact Assessment |
| Status | Approved with Conditions (ARB-2026-024, 2026-07-16) |

## 2. Description of the Change

Deploy a fourth regional stamp of Harbourline Connect in Azure UAE North, alongside the existing US, EU and CA stamps defined in ADR-0041. The UAE stamp will serve customer accounts whose home region is Harbourline Gulf FZE, including shippers and consignees using the Jebel Ali terminal (JEA-T4) and Gulf forwarding lanes. Azure Front Door will route authenticated users to the UAE stamp based on the account home region held in Harbourline Connect ID, as it does for the other stamps.

The stamp will contain the Connect web front end, the .NET 8 BFF on AKS, a PostgreSQL Flexible Server read model populated from HSP events, and the Harbourline Gulf subscriber data for the Customer Notification Service.

## 3. Drivers

1. **UAE Personal Data Protection Law (PDPL).** Customer user profiles, contact details and shipment party data for Gulf customers are currently served from the US stamp (East US 2). Harbourline Gulf's legal counsel advised in May 2026 that continued processing in the United States requires documented transfer safeguards and that local processing is the lower-risk position. STD-DAT-005 already states that UAE personal data for Harbourline Gulf is to be held in UAE North.
2. **Customer commitments.** Three of the ten largest Jebel Ali customers, including two government-linked shippers, have requested contractual confirmation that their users' data is hosted in the UAE. Two framework renewals worth a combined USD 14M annual revenue fall due in Q2 2027.
3. **Performance.** Median page load for Gulf users on the US stamp is 3.9 s, against a Connect target of 2.0 s; round-trip latency from Dubai to East US 2 accounts for most of the difference.
4. **Consistency with the roadmap.** F-01 wave 4 moves Gulf lanes to an HSP data cell in UAE North by March 2027. Without a local Connect stamp, milestone events for Gulf shipments would be produced in UAE North and consumed in the US, which reintroduces the cross-border transfer the wave is designed to remove.

## 4. Scope

**In scope**

- New Connect stamp in UAE North built from the RA-02 regional stamp pattern via Terraform.
- Front Door routing rule and Connect ID home-region attribute value `AE`.
- Migration of approximately 4,300 Gulf customer user profiles and preferences from the US stamp.
- Event Backbone consumption of `shipment.milestone.recorded.v1` and `shipment.status.changed.v1` for Gulf shipments in-region.
- CNS subscriber data for Gulf customers in the UAE stamp.

**Out of scope**

- HSP UAE North data cell (already delivered under WP-07).
- Arabic-language user interface (separate product backlog item).
- Changes to terminal systems at JEA-T4.

## 5. Expected Benefits

| Benefit | Measure | Target |
|---|---|---|
| Regulatory alignment | Gulf customer personal data held outside UAE | 0 records after migration |
| Customer retention | Framework renewals at risk | Both renewals secured |
| Performance | Median page load, Gulf users | ≤ 2.0 s |
| Visibility | Milestone latency for Gulf shipments | < 5 min p95 (REQ-HSP-014) |

## 6. Estimated Cost and Timeline (Requester's Estimate)

| Item | Estimate |
|---|---|
| Build and migration (one-off) | USD 1.2M |
| Run cost (Azure, Confluent, support) | USD 0.40M per year |
| Target go-live | 2027-04-30, after F-01 wave 4 |

The requester's estimate was refined in H-02.

## 7. Risks Identified by the Requester

- UAE North has no DR region approved in STD-CLD-007; Tier 1 paired-region DR may not be achievable as written.
- Some Azure services used by the other stamps may reach UAE North later than other regions; availability must be confirmed.
- Customers with users in several regions need a single home region; the rule for choosing it must be agreed with the DPO.

## 8. Decision Record

| Date | Event |
|---|---|
| 2026-06-11 | CR raised by Omar Haddad and logged by Samuel Adeyemi |
| 2026-06-18 | Triage at ARB: classified Tier 1; impact assessment assigned to Kenji Watanabe and Lena Vogel |
| 2026-07-09 | H-02 Requirements Impact Assessment completed |
| 2026-07-16 | ARB decision ARB-2026-024: **Approved with Conditions** (see H-02 §7) |

## 9. Document History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-06-11 | Change request submitted |
| 1.1 | 2026-07-16 | Status and decision recorded |
