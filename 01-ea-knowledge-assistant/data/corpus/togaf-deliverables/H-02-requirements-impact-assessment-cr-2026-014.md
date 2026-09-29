---
doc_id: H-02
title: Requirements Impact Assessment — CR-2026-014
doc_type: togaf_deliverable
togaf_phase: H
version: "1.0"
status: Approved
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2026-024)
effective_date: 2026-07-09
next_review: 2027-01-14
classification: Internal
related: [H-01, ARS-01, ADD-01, F-01, GOV-01, GOV-02, AP-06, AP-10, STD-DAT-005, STD-CLD-007, STD-RES-015, STD-IAM-008, STD-SEC-009, ADR-0030, ADR-0041, RA-02]
---

# H-02 — Requirements Impact Assessment — CR-2026-014

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This assessment evaluates change request CR-2026-014 (H-01), raised by Omar Haddad on 2026-06-11, to add a UAE deployment stamp for Harbourline Connect (APP-050). It identifies the requirements, architecture domains and standards affected, estimates cost and schedule impact, and gives a recommendation to the ARB. Assessors: Kenji Watanabe (lead), Lena Vogel (data), Priya Raman (security), with input from Marieke de Vries (DPO).

## 2. Summary

The change is consistent with the target architecture and closes a residency gap that already exists: Gulf customer personal data is served from East US 2, while STD-DAT-005 places it in UAE North. The main issue is resilience. Harbourline Connect is a Tier 1 service under STD-RES-015, which requires paired-region DR, and STD-CLD-007 does not list a second UAE region. Using a non-UAE region for DR would move UAE personal data out of the country and defeat the purpose of the change.

## 3. Impacted Requirements

| Requirement | Impact | Assessment |
|---|---|---|
| REQ-HSP-023 (UAE personal data in UAE North) | Positive | Extends the requirement from HSP to the Connect read model and profiles; the CR is needed to satisfy it end to end. |
| REQ-HSP-025 (independent regional stamps) | Positive | First stamp added after the ADR-0041 set; validates the stamp pattern. |
| REQ-HSP-014 (milestone latency < 5 min p95) | Neutral to positive | Gulf events stay in-region; current US-routed path measures about 3 min 50 s p95 for Gulf shipments, close to the limit. |
| REQ-HSP-015 (Tier 1: RTO 1 h, RPO 15 min, paired-region DR) | **Conflict** | Paired-region DR cannot be met inside approved UAE regions. See §5. |
| REQ-HSP-019 (identity) | Minor | Connect ID needs home-region value `AE`; no change to workforce identity controls. |
| REQ-HSP-020 (encryption with customer-managed keys) | Minor | New Key Vault Premium instance in UAE North; keys must not be replicated outside the UAE. |

A new requirement is proposed for ARS-01 v1.3: *"Personal data of Harbourline Gulf customers MUST be served to Harbourline Connect users from UAE North."*

## 4. Impacted Architecture Domains

| Domain | Impact |
|---|---|
| Business | Gulf customer onboarding assigns home region `AE`; the rule for multi-region customers is to use the contracting entity's region. |
| Data | New regional read model; Gulf user profiles migrated from East US 2 and deleted there within 30 days, with a deletion certificate to the DPO. Tidewater receives only aggregated Gulf data (STD-DAT-005). |
| Application | No code change to Connect, as expected under REQ-HSP-025; configuration and routing only. CNS needs a Gulf subscriber store in the stamp. |
| Technology | New stamp in `hlg-online`; Confluent Cloud cluster in UAE North or cluster linking from the HSP data cell; APIM Premium gateway unit in UAE North. |

## 5. Impacted Standards

### 5.1 STD-DAT-005 Data Residency & Cross-Border Transfer

The change brings Connect into line with the standard. During migration, the copy of profiles in East US 2 continues under the current transfer safeguards and must be removed within 30 days of cutover. No TIA is needed for the target state because no UAE personal data leaves the UAE. A TIA would be needed for any design that uses a DR region outside the UAE.

### 5.2 STD-CLD-007 Cloud Landing Zone & Hosting

UAE North is an approved region, so the primary deployment conforms. The standard lists no second UAE region, and the Azure regional pair of UAE North is not approved. Kenji Watanabe, as owner, will assess adding UAE Central as a **DR-only** region in the next revision of STD-CLD-007, subject to service availability and landing-zone policy coverage.

### 5.3 STD-RES-015 Resilience & Disaster Recovery

Tier 1 requires RTO 1 h, RPO 15 min, multi-zone and paired-region DR. Options assessed:

| Option | Description | Residency | Resilience | Cost (per year) |
|---|---|---|---|---|
| A | Zone-redundant UAE North only; geo-redundant backups kept in-country | Compliant | Meets multi-zone; no paired-region DR; RTO for full regional loss about 24 h | USD 0.38M |
| B | DR in West Europe | Non-compliant without TIA and PDPL safeguards | Meets Tier 1 | USD 0.52M |
| C | DR in UAE Central after STD-CLD-007 is revised | Compliant | Meets Tier 1 | USD 0.49M |

Recommended: **Option A as interim, moving to Option C** once STD-CLD-007 is revised. Option A requires a time-bound exception to the paired-region DR clause of STD-RES-015, raised through the GOV-01 process and recorded in GOV-02, with Option C as its remediation plan.

## 6. Cost and Schedule Impact

| Item | Requester estimate | Assessed estimate |
|---|---|---|
| Build and migration | USD 1.2M | USD 1.35M (adds Confluent in-region cluster and DR design) |
| Annual run cost | USD 0.40M | USD 0.42M (Option A); USD 0.53M (Option C) |
| Go-live | 2027-04-30 | 2027-04-30, dependent on F-01 wave 4 finishing by 2027-03-31 |

Funding comes from WP-04 contingency; F-01 WP-04 scope is updated to include the UAE stamp. No change to TA2 or TA3 dates. The schedule risk is the dependency on wave 4, itself constrained by the Oracle 12c retirement on 2027-03-31.

## 7. Recommendation to the ARB

The assessors recommend **Approve with Conditions**:

1. Build the UAE stamp using the RA-02 regional stamp pattern and Terraform, with no application code fork.
2. Deploy Option A for go-live under a time-bound exception to STD-RES-015 (maximum 12 months), owner Kenji Watanabe, remediation Option C.
3. No UAE personal data may be replicated outside the UAE, including backups and logs; Log Analytics workspace for the stamp in UAE North.
4. The DPO confirms the home-region rule for multi-region customers before migration starts.
5. Delete Gulf profiles from East US 2 within 30 days of cutover and give the DPO the deletion evidence.
6. Add the new requirement in §3 to ARS-01 and update ADR-0041's consequences through the EA Office.

## 8. Outcome

At its meeting on 2026-07-16 the ARB accepted the recommendation as decision ARB-2026-024, **Approved with Conditions**, with Omar Haddad accountable for delivery and Kenji Watanabe for the resilience remediation.

## 9. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-07-09 | Kenji Watanabe | Assessment issued to ARB |
