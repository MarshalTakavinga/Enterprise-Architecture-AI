---
doc_id: GOV-01
title: Architecture Governance Framework & ARB Charter
doc_type: governance
togaf_phase: Preliminary
version: "3.1"
status: Approved
owner: Samuel Adeyemi, Head of Enterprise Architecture Office / ARB Secretary
approved_by: Elena Marsh, CIO; Architecture Review Board (ARB-2026-002)
effective_date: 2026-01-15
next_review: 2027-01-15
classification: Internal
related: [AP-CATALOG, PRE-01, GOV-02, GOV-03, STD-TLC-014, G-01, G-02, H-01]
---

# GOV-01 — Architecture Governance Framework & ARB Charter

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This document establishes how architecture is governed at Harbourline Logistics Group. It defines the tailored architecture development method, the organisation of the Enterprise Architecture (EA) function, the charter of the Architecture Review Board (ARB), review tiers, the exception process, escalation routes, and the structure of the architecture repository. It is the authority referenced by every standard's "Compliance & exceptions" clause.

## 2. Scope

The framework applies to all Harbourline entities and to all change initiatives that introduce, modify or retire applications, data stores, integrations, infrastructure or OT systems, whether delivered internally, by a system integrator, or by a SaaS vendor. It applies to the Horizon 2028 programme in full.

## 3. Tailored Architecture Development Method

Harbourline uses the TOGAF ADM as its reference process, tailored as follows.

| ADM phase | Harbourline tailoring | Key deliverables |
|---|---|---|
| Preliminary | Performed once per strategy cycle; refreshed when principles change | GOV-01, AP-CATALOG, PRE-01 |
| A — Vision | Triggered by an approved Request for Architecture Work; must complete within 8 weeks | PRE-02, A-01, A-02, A-03 |
| B-D — Business, Data/Application, Technology | Run as one combined phase with a single ADD and ARS; domain architects contribute sections | A-04, ADD-01, ARS-01 |
| E-F — Opportunities & Migration Planning | Merged; output is one roadmap with transition architectures and work packages | F-01 |
| G — Implementation Governance | Architecture Contract signed with each delivery team; compliance assessments at each release gate | G-01, G-02 |
| H — Change Management | Change requests raised as CR-YYYY-NNN and assessed for impact | H-01, H-02 |
| Requirements Management | Continuous; requirements held in ARS with REQ-HSP-NNN style IDs | ARS-01 |

Small initiatives (under USD 500k, no Restricted data, no new technology) skip Phases A-F and enter directly at Phase G via a Tier 2 or Tier 3 review.

## 4. EA Organisation Model

The EA function is federated: a central EA Office sets principles and standards and runs the ARB, while domain architects own their standards and solution architects in delivery teams apply them.

| Role | Holder | Accountabilities |
|---|---|---|
| Executive sponsor | Elena Marsh, CIO | Approves this charter; final escalation point |
| Chief Architect & ARB Chair | David Okafor | Owns principles and STD-TLC-014; chairs ARB |
| Head of EA Office & ARB Secretary | Samuel Adeyemi | Runs ARB logistics, logs, repository stewardship, GOV-02 |
| Lead Integration Architect | Amara Osei | STD-INT-001, STD-API-002, STD-EVT-003 |
| Principal Security Architect | Priya Raman | STD-IAM-008, STD-SEC-009, co-owner STD-AI-013 |
| Lead Data Architect | Lena Vogel | STD-DAT-004, STD-DAT-005, STD-DB-006, co-owner STD-AI-013 |
| Principal Cloud Architect | Kenji Watanabe | STD-CLD-007, STD-OBS-010, STD-CTR-012, STD-RES-015 |
| Lead Network & OT Architect | Tomasz Nowak | STD-NET-011 |
| Solution architects | Per initiative (e.g., Julia Brandt for APP-055) | Prepare submissions; maintain conformance |

The CISO (Hannah Brennan) and Group DPO (Marieke de Vries) are standing advisers to the ARB and are consulted on security- and privacy-significant submissions.

## 5. ARB Charter

### 5.1 Mandate
The ARB approves or rejects solution architectures, standards, ADRs and exceptions; maintains the technology radar; and monitors conformance of in-flight programmes.

### 5.2 Membership
Voting members: Chief Architect (Chair), Lead Integration Architect, Principal Security Architect, Lead Data Architect, Principal Cloud Architect, Lead Network & OT Architect. The ARB Secretary is non-voting. Each voting member may nominate one named delegate.

### 5.3 Quorum
Quorum is the Chair (or the Chair's delegate) plus three voting members, one of whom MUST be the Principal Security Architect or her delegate. A meeting without quorum may discuss but not decide.

### 5.4 Cadence
The ARB meets every Thursday, 14:00-16:00 ET, with a 30-minute window reserved for attendees in Rotterdam and Jebel Ali. Extraordinary sessions may be called by the Chair with 48 hours' notice for urgent security or regulatory matters.

### 5.5 Decision-making
Decisions are made by consensus; if consensus fails, by simple majority of voting members present, with the Chair holding a casting vote. The Principal Security Architect may place a security hold on any decision, which can only be lifted by the CISO.

## 6. Review Tiers

| Tier | Type | Triggers (any one) | Reviewers | Outcome recorded |
|---|---|---|---|---|
| Tier 1 | Full ARB review | New system; any Restricted data; cross-border data transfer; technology not on the radar; cost > USD 500k | Full ARB | ARB-YYYY-NNN in ARB log |
| Tier 2 | Delegated review | Change to existing system with no standards deviation; Cosmos DB access-pattern designs under STD-DB-006 | Two domain architects | Reported to next ARB; logged |
| Tier 3 | Self-certification | Minor change: configuration, patch, dependency upgrade within approved versions | Solution architect via checklist | Checklist stored in repository |

Any standards deviation automatically escalates a submission to Tier 1 and requires an exception request. The ARB Secretary determines the tier on intake; disputes go to the Chair.

## 7. Submission Requirements and SLAs

### 7.1 Tier 1 packet contents
1. Solution overview and context diagram.
2. Principles conformance table (AP-01 to AP-16).
3. Standards conformance checklist, with clause references.
4. Data classification and residency statement, including any TIA status.
5. Integration inventory (events, APIs, files) with pattern IDs (INT-P1 to INT-P5).
6. Resilience tier and RTO/RPO per STD-RES-015.
7. Security threat model summary.
8. Cost estimate (build and 3-year run).
9. Exception requests, if any.

### 7.2 Service levels

| Step | SLA |
|---|---|
| Tier 1 packet due to ARB Secretary | Monday 12:00 ET for the same week's Thursday session |
| Completeness check and tier confirmation | By Tuesday 17:00 ET |
| Pre-read circulated to members | Tuesday 17:00 ET |
| Decision published in ARB log | Within 2 working days of the session |
| Tier 2 delegated review completed | 5 working days from submission |
| Tier 3 checklist spot-check | 10% sampled monthly by the EA Office |

Late or incomplete packets are deferred to the following week.

## 8. Decision Types

- **Approved** — proceed as submitted.
- **Approved with Conditions** — proceed; named conditions with owners and due dates must be closed, tracked by the ARB Secretary.
- **Changes Requested** — resubmit after addressing findings; no build beyond prototype. Example: ARB-2026-031 (APP-055).
- **Rejected** — the proposal must not proceed in its current form; a new submission requires a materially different approach.

## 9. Exception (Dispensation) Process

1. **Request.** The solution architect raises an exception request citing the standard and clause (e.g., STD-DB-006 §5), the system, the reason and the proposed duration.
2. **Registration.** The ARB Secretary assigns an `EXC-YYYY-NNN` ID and records it in GOV-02 with status *Requested*.
3. **Domain assessment.** The owning domain architect assesses risk and proposes compensating controls within 5 working days.
4. **Remediation plan.** The requester provides a remediation plan with a named owner, milestones and target end date. Requests without a plan are not scheduled.
5. **ARB decision.** The exception is heard at a Tier 1 session and approved, approved with conditions, or rejected, with the decision logged as ARB-YYYY-NNN.
6. **Duration.** Maximum 12 months, renewable once for up to a further 12 months. A second renewal is not permitted; the matter escalates to the CIO.
7. **Monitoring.** The ARB Secretary reviews GOV-02 monthly and notifies owners 60 days before expiry.
8. **Closure.** On remediation the owner submits evidence; the exception is marked *Closed*.

## 10. Escalation to the CIO

The following are escalated by the ARB Chair to Elena Marsh:
- disagreement between the ARB and a programme director (e.g., Grace Liu) on a Rejected or Changes Requested decision that affects a Horizon 2028 milestone;
- an exception that has reached its renewal limit;
- a security hold that the CISO does not lift within 10 working days;
- principle conflicts not resolved by the precedence rules in AP-CATALOG §4.

The CIO decides within 10 working days; the decision is recorded in the ARB log.

## 11. Architecture Repository

### 11.1 Structure

| Area | Contents |
|---|---|
| Architecture Metamodel & Governance | GOV-01, GOV-03 |
| Architecture Landscape | Baseline and target architectures, ADD-01, capability maps |
| Standards Information Base | AP-CATALOG, STD-XXX-NNN, technology radar |
| Reference Library | RA-01 to RA-04 |
| Governance Log | ARB log, GOV-02, compliance assessments, architecture contracts |
| Decision Records | ADR-NNNN |
| Requirements Repository | ARS-01 and related requirements |

### 11.2 Document lifecycle
Draft → In Review → Approved/Accepted → Superseded. Every document carries front matter with ID, version, owner, status and next review date. Standards are reviewed at least every 12 months. The ARB Secretary is the repository steward and flags overdue reviews monthly.

## 12. RACI

| Activity | CIO | ARB Chair | ARB members | EA Office | Solution architect | CISO / DPO |
|---|---|---|---|---|---|---|
| Approve principles | A | R | C | C | I | C |
| Publish standards | I | A | R | C | I | C |
| Tier 1 review | I | A | R | R | C | C |
| Tier 2 review | – | A | R | I | C | – |
| Approve exceptions | I | A | R | R | C | C |
| Maintain GOV-02 & ARB log | – | A | I | R | I | – |
| Escalation decisions | A/R | R | C | I | I | C |

## 13. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 2.0 | 2023-05-02 | David Okafor | Tiered review model introduced |
| 3.0 | 2024-12-05 | Samuel Adeyemi | Tailored ADM for Horizon 2028 |
| 3.1 | 2026-01-15 | Samuel Adeyemi | Security quorum rule; exception renewal limit clarified |
