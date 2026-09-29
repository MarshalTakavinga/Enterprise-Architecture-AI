---
doc_id: STD-DAT-005
title: Data Residency & Cross-Border Transfer Standard
doc_type: standard
togaf_phase: Preliminary
version: "2.0"
status: Approved
owner: Lena Vogel, Lead Data Architect (with Marieke de Vries, Group DPO)
approved_by: Architecture Review Board (ARB-2025-006)
effective_date: 2025-02-01
next_review: 2026-11-01
classification: Internal
related: [AP-02, AP-06, AP-10, STD-DAT-004, STD-CLD-007, STD-EVT-003, RA-02, RA-04, GOV-01, GOV-02]
---

# STD-DAT-005 — Data Residency & Cross-Border Transfer Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard specifies where Harbourline Logistics Group MUST store and process personal data according to the jurisdiction of the data subject and the contracting legal entity, and the conditions under which personal data MAY be transferred across borders. It gives effect to principle AP-06 (Data Residency Follows Jurisdiction) and to Harbourline's obligations under the EU GDPR, Canada's PIPEDA and customer contracts, and the UAE Personal Data Protection Law (PDPL).

## 2. Scope

1. All personal data processed by any Harbourline legal entity: Harbourline Inc., Harbourline Canada Ltd., Harbourline Europe B.V., Nordhaven Freight GmbH and Harbourline Gulf FZE.
2. Storage, processing, backup, disaster recovery replicas, logs, analytics copies and AI processing (including prompts and documents sent to AI services).
3. Processing by SaaS providers and subprocessors (for example messaging, email and SMS providers).

Non-personal operational data (e.g. container telemetry with no personal data, vessel schedules) is not constrained by this standard beyond STD-CLD-007 region rules.

## 3. Related Principles and Normative References

- **AP-06 Data Residency Follows Jurisdiction**; **AP-02 Compliance by Design**; **AP-10 Cloud-Smart and Portable**.
- **STD-DAT-004** (classification — pseudonymised data remains personal data); **STD-CLD-007** (approved regions); **STD-EVT-003** §4 (EU topics on the West Europe cluster).
- **RA-02** Cloud-Native Application on the Azure Landing Zone (regional stamp model).
- **RA-04** Tidewater Enterprise Data Platform (West Europe workspace).

Normative terms follow RFC 2119.

## 4. Residency Rules

### 4.1 Region mapping

| Data subject / entity | Primary region | DR region | Condition |
|---|---|---|---|
| EU data subjects (all entities) | Azure **West Europe** | Azure **North Europe** | Always |
| Canadian customers | Azure **Canada Central** | Azure **Canada East** | Where contractually required; otherwise US rules MAY apply |
| UAE data subjects — Harbourline Gulf FZE | Azure **UAE North** | As approved by ARB | Always |
| US data subjects | Azure **East US 2** | Azure **Central US** | Default |
| UK data subjects | Azure **West Europe** | Azure **North Europe** | Treated as EU for storage |

### 4.2 Residency requirements

1. Personal data of EU data subjects MUST be stored and processed only in West Europe (primary) or North Europe (DR). This includes backups, read replicas, search indexes, caches and log workspaces holding personal data.
2. Canadian customer personal data MUST be stored in Canada Central/Canada East where the customer contract requires Canadian residency. The Customer domain MUST maintain a residency flag on the customer account in Salesforce (APP-040) so that applications can route correctly.
3. Personal data of UAE data subjects processed by Harbourline Gulf MUST be held in UAE North. Customer-facing applications serving Harbourline Gulf customers MUST provide a UAE North deployment before holding such data.
4. Multi-region applications SHOULD use the regional deployment stamp model described in RA-02: each stamp holds only the personal data of its jurisdiction, and global routing (Azure Front Door) directs users by account home region, not by browser location.
5. Global services (identity, API gateway control plane) MAY process minimal identifiers necessary for routing and authentication; they MUST NOT persist profile data outside the home region.

### 4.3 Analytics and aggregation

1. Aggregated or **anonymised** data MAY be centralised in the Tidewater Data Platform in East US 2.
2. **Pseudonymised data is still personal data** and MUST follow §4.2. Hashing a customer email or replacing names with surrogate keys does not make data anonymous.
3. EU personal data required for analytics MUST be processed in the Tidewater West Europe workspace; only outputs meeting the anonymisation criteria in §6 MAY flow to East US 2.

## 5. Cross-Border Transfers

### 5.1 Definition

A transfer occurs whenever personal data subject to a residency rule is stored in, processed in, or **accessible from** a location outside its permitted regions. Remote support access from another country, a SaaS provider processing in a third country, and sending data to an AI endpoint in another region are all transfers.

### 5.2 Requirements

1. Every cross-border transfer of personal data MUST have a **Transfer Impact Assessment (TIA)** approved by the Group DPO before production use.
2. Transfers of EU personal data to countries without an adequacy decision MUST be covered by **Standard Contractual Clauses (SCCs)** or another valid transfer mechanism, recorded in the Record of Processing Activities.
3. Transfers of Restricted data (STD-DAT-004 §5.4) additionally require Tier 1 ARB review.
4. Subprocessors MUST be configured to use in-region processing where the provider offers it (e.g. EU data centre selection for SMS or email providers). If only out-of-region processing is available, the TIA MUST document supplementary measures (encryption, minimisation, pseudonymisation).
5. Data minimisation applies: a transfer SHOULD include only fields strictly necessary — for an SMS notification, the phone number and message text, not the customer profile.

### 5.3 TIA process

| Step | Actor | Output |
|---|---|---|
| 1. Describe the flow (data categories, volume, destination, recipient) | Solution architect | Data flow description |
| 2. Assess destination law and provider safeguards | DPO office | Draft TIA |
| 3. Define supplementary measures | Solution architect + data architect | Measures list |
| 4. Approve or reject | Group DPO (Marieke de Vries) | Signed TIA reference |
| 5. Record in ARB submission | Solution architect | TIA ID in design |

Typical DPO turnaround is 15 working days. Solutions MUST NOT go live, and MUST NOT process real personal data in test, pending TIA approval.

## 6. Anonymisation Criteria

Data MAY be treated as anonymised only when all of the following hold, confirmed by the data architect:

1. Direct identifiers (name, email, phone, identity numbers, account IDs) are removed, not merely hashed.
2. Aggregates have a minimum cell size of 10 data subjects.
3. The re-identification risk assessment is documented in the Tidewater catalogue entry for the data product.

## 7. Worked Examples

| Scenario | Ruling |
|---|---|
| Harbourline Connect stores EU customer user profiles | EU deployment stamp in West Europe only |
| Customer notification service sends SMS to EU phone numbers via a US-hosted provider | Cross-border transfer; TIA and SCCs required before go-live; exception cannot substitute for DPO approval |
| Tidewater dashboard of monthly shipment volumes by country | Anonymised aggregate; MAY be in East US 2 |
| Support engineer in Baltimore queries EU customer records | Transfer by remote access; covered by the group TIA for support access; access via PIM only |
| Nordhaven TMS in AWS eu-central-1 | Within the EU; residency compliant; hosting governed by EXC-2025-003 under STD-CLD-007 |

## 8. Compliance and Exceptions

1. Residency is verified at ARB review against the region mapping, and continuously via Azure Policy assignments restricting resource locations per management group.
2. Deviations MUST be requested through the GOV-01 exception process and recorded in GOV-02. An architecture exception does **not** replace the legal requirement for a DPO-approved TIA; any exception touching personal data transfer MUST reference the TIA status and remains in "Requested" state until the TIA is approved.
3. Exceptions are time-bound (maximum 12 months, renewable once) and MUST include a remediation plan.

## 9. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2023-05-15 | Lena Vogel | Initial EU residency rules (West Europe / North Europe) |
| 1.1 | 2024-06-01 | Lena Vogel, Marieke de Vries | Added Nordhaven entity; TIA process formalised |
| 2.0 | 2025-02-01 | Lena Vogel, Marieke de Vries | Added Canada and UAE rules; regional stamp model; pseudonymisation clarification; anonymisation criteria; ARB-2025-006 |
