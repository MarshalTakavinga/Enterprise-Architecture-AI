---
doc_id: STD-DAT-004
title: Data Classification & Handling Standard
doc_type: standard
togaf_phase: Preliminary
version: "3.0"
status: Approved
owner: Lena Vogel, Lead Data Architect
approved_by: Architecture Review Board (ARB-2024-041)
effective_date: 2024-09-01
next_review: 2026-12-01
classification: Internal
related: [AP-02, AP-05, AP-06, AP-12, STD-DAT-005, STD-SEC-009, STD-IAM-008, STD-EVT-003, STD-OBS-010, RA-04, GOV-01, GOV-02]
---

# STD-DAT-004 — Data Classification & Handling Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines Harbourline Logistics Group's four data classifications and the minimum handling controls for each. It ensures that data is protected in proportion to the harm its disclosure, alteration or loss would cause to customers, employees, crews, terminal safety and Harbourline's regulatory standing under GDPR, NIS2, PIPEDA, UAE PDPL and the US Coast Guard maritime cybersecurity rule.

Every data set, application, topic, API and storage account MUST carry a classification from this standard.

## 2. Scope

- All data created, received, stored or processed by Harbourline and its legal entities, including Nordhaven Freight GmbH.
- All environments (production, pre-production, test, development, sandbox) and all hosting locations (Azure, AWS, SaaS, terminal edge).
- Data processed on Harbourline's behalf by suppliers and delivery partners.

Where to store and process data by jurisdiction is governed separately by STD-DAT-005.

## 3. Related Principles and Normative References

- **AP-02 Compliance by Design**, **AP-05 Data Is an Asset with a Named Owner**, **AP-06 Data Residency Follows Jurisdiction**, **AP-12 Zero Trust Access**.
- **STD-SEC-009** Encryption & Key Management; **STD-IAM-008** Identity & Access Management; **STD-DAT-005** Data Residency; **STD-EVT-003** §7 (event payloads); **STD-OBS-010** (logging restrictions).

Normative terms follow RFC 2119.

## 4. Roles

| Role | Responsibility |
|---|---|
| Data Owner | Business leader accountable for a data domain (AP-05); assigns classification and approves access to Restricted data |
| Data Steward | Maintains metadata, quality rules and classification tags in the catalogue |
| Application Owner | Implements the handling controls for data held in their application |
| Lead Data Architect | Owns this standard; arbitrates classification disputes |
| Group DPO | Advises on personal data classification and processing lawfulness |

## 5. Classification Levels

### 5.1 Public

Information approved for release outside Harbourline. Examples: published tariffs, press releases, public vessel schedules, the corporate website.

### 5.2 Internal

Default classification for business information not intended for public release, whose disclosure would cause limited harm. Examples: internal procedures, architecture standards, aggregated operational KPIs, organisation charts.

### 5.3 Confidential

Information whose disclosure would cause material commercial, contractual or individual harm. Examples:

- Customer contracts, negotiated rates, commercial pipeline in Salesforce (APP-040).
- Individual shipment records including consignee names and business contact details.
- Financial results before publication; supplier pricing.
- Personal data of individual data subjects handled in small volumes as part of normal business (for example a named contact on a booking).

### 5.4 Restricted

The highest classification. Data MUST be classified **Restricted** if it falls into any of the following categories:

| # | Restricted category | Typical systems |
|---|---|---|
| R1 | Personal data of EU, UK, Canadian or UAE data subjects **in bulk** (data sets of 1,000 or more individuals, or any full extract of a customer or contact master) | Harbourline Connect, Salesforce, Tidewater |
| R2 | Payment card data (PAN, card verification data) | Payment service provider integrations |
| R3 | Customs declarations containing personal data (e.g. importer of record who is a natural person, identity numbers) | Customs Filing Gateway (APP-060) |
| R4 | Security-sensitive OT and terminal configuration: PLC/crane control logic, OT network diagrams, firewall rule bases, gate automation configuration | Navis N4 edge, Terminal Gate Automation (APP-031) |
| R5 | Crew passport and identity document data | Terminal access, crew change processes |

Where a data set combines categories, the highest classification applies. Aggregation matters: a single consignee contact is Confidential, but an export of all consignee contacts is Restricted (R1).

## 6. Handling Requirements

### 6.1 Control matrix

| Control | Public | Internal | Confidential | Restricted |
|---|---|---|---|---|
| Encryption in transit (TLS 1.2+) | SHOULD | MUST | MUST | MUST |
| Encryption at rest | — | MUST (platform keys) | MUST (platform keys) | MUST, **customer-managed keys** in Key Vault (HSM-backed) |
| Access model | Open | Entra ID authenticated | Role-based, owner-approved | Role-based **and** privileged access via Entra PIM |
| Access recertification | — | — | Annual | **Quarterly** |
| Use in non-production | Allowed | Allowed | Allowed if access-controlled | **Prohibited unless masked** |
| External sharing | Allowed | NDA required | Data Owner approval + contract | Data Owner + DPO/CISO approval + TIA where cross-border |
| Logging of content | Allowed | Allowed | Avoid | **Prohibited** |

### 6.2 Restricted data — additional requirements

1. Restricted data MUST be encrypted at rest with **customer-managed keys** held in Azure Key Vault Premium or Managed HSM per STD-SEC-009.
2. Administrative and bulk data access to systems holding Restricted data MUST be via **Entra Privileged Identity Management (PIM)**, just-in-time, as defined in STD-IAM-008.
3. Restricted data MUST NOT be used in non-production environments unless it has been **masked** (irreversibly substituted or tokenised) using the approved masking pipeline in the Tidewater Data Platform. Copying production databases into test is prohibited.
4. Any new system storing Restricted data requires Tier 1 ARB review (GOV-01).
5. Restricted data MUST NOT be placed in event payloads unless field-level encrypted (STD-EVT-003 §7), and MUST NOT be sent to any AI or machine-learning service that has not been approved by the ARB for that data.
6. Category R4 (OT configuration) MUST NOT be stored in general-purpose collaboration tools; it MUST be held in the OT document repository in the IT/OT DMZ with access logged.

### 6.3 Personal data

1. Pseudonymised personal data remains personal data and retains its classification; only effectively anonymised data MAY be downgraded.
2. Personal data MUST NOT be written to application or platform logs (STD-OBS-010).
3. Retention periods MUST be defined per data set by the Data Owner with the DPO and enforced technically (TTL, lifecycle policies or scheduled purge).

## 7. Labelling and Tagging

1. Every Azure resource MUST carry the `data-classification` tag with one of `public`, `internal`, `confidential`, `restricted` (STD-CLD-007).
2. Data sets in the Tidewater catalogue (Unity Catalog) MUST carry classification tags at table level, and column-level tags for Restricted fields.
3. Documents and emails SHOULD carry the matching sensitivity label.
4. Kafka topics and API contracts MUST declare classification metadata (STD-EVT-003 §5.2; STD-API-002 §4.2).

## 8. Examples

| Data | Classification | Reason |
|---|---|---|
| Public sailing schedule | Public | Published externally |
| HSP milestone event for one shipment (no personal data) | Internal | Operational fact, limited harm |
| Customer rate card | Confidential | Commercial harm |
| Harbourline Connect user table (EU users) | Restricted (R1) | Bulk personal data of EU data subjects |
| ICS2 entry summary declaration with natural-person importer | Restricted (R3) | Customs declaration with personal data |
| RTM-T2 crane PLC configuration backup | Restricted (R4) | Security-sensitive OT configuration |

## 9. Compliance and Exceptions

1. Application Owners MUST confirm classification and controls at each ARB review; the data architect verifies Restricted data handling in Tier 1 reviews.
2. The CISO's team scans cloud resources monthly for missing or inconsistent `data-classification` tags.
3. Where a control cannot be met, an exception MUST be requested through the GOV-01 process and recorded in GOV-02 (`EXC-YYYY-NNN`, maximum 12 months, renewable once, with remediation plan). Exceptions to §6.2(3) (unmasked Restricted data in non-production) require CISO and DPO endorsement.

## 10. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 2.0 | 2023-03-01 | Lena Vogel | Moved from three to four levels; introduced Restricted |
| 2.1 | 2023-11-15 | Lena Vogel | Added control matrix; clarified pseudonymised data remains personal data |
| 3.0 | 2024-09-01 | Lena Vogel | Defined Restricted categories R1–R5 incl. OT configuration (NIS2) and crew passport data; customer-managed keys and PIM mandatory; masking rule for non-production; extended to Nordhaven; ARB-2024-041 |
