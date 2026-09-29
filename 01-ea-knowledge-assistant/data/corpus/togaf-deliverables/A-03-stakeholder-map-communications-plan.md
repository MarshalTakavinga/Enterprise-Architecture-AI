---
doc_id: A-03
title: Stakeholder Map & Communications Plan — Horizon 2028 Shipment Platform
doc_type: togaf_deliverable
togaf_phase: A
version: "1.2"
status: Approved
owner: Samuel Adeyemi, Head of Enterprise Architecture Office
approved_by: Architecture Review Board (ARB-2024-063)
effective_date: 2025-11-14
next_review: 2026-11-14
classification: Internal
related: [A-01, A-02, A-04, GOV-01, F-01, AP-02, AP-04, AP-06, AP-16]
---

# A-03 — Stakeholder Map & Communications Plan — Horizon 2028 Shipment Platform

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This document identifies the people and groups who influence or are affected by the Shipment Platform Consolidation, records what each cares about, defines which architecture views each should receive, and sets out how and how often the EA Office will communicate with them. It supports the Architecture Vision (A-01) and the Statement of Architecture Work (A-02).

## 2. Approach

Stakeholders were identified in workshops held 2024-10-21 and 2024-11-04 with the sponsor, the Programme Director and domain architects. Each was classified on two scales:

- **Power** — ability to change scope, budget, or design decisions (High / Medium / Low).
- **Interest** — how much the outcome affects their objectives (High / Medium / Low).

The resulting quadrants drive engagement: *Manage closely* (high/high), *Keep satisfied* (high power, lower interest), *Keep informed* (lower power, high interest), *Monitor* (low/low).

## 3. Stakeholder Map

| Stakeholder | Power | Interest | Quadrant | Key concerns | Viewpoints / artefacts provided |
|---|---|---|---|---|---|
| Elena Marsh, CIO (sponsor) | High | High | Manage closely | Budget, milestones, run-cost goal | Vision, roadmap, KPI dashboard |
| Rachel Kim, CFO | High | Medium | Keep satisfied | Cost reduction, billing accuracy, SAP integrity | Cost model, benefits realisation view |
| Hannah Brennan, CISO | High | High | Manage closely | Regulator evidence, attack surface during migration | Security architecture view, exception list |
| David Okafor, Chief Architect / ARB Chair | High | High | Manage closely | Coherence with principles and standards | All views; ARB log |
| Grace Liu, Programme Director | High | High | Manage closely | Scope stability, dependency clarity | Roadmap, work packages, architecture contract |
| Michael Torres, VP Port & Terminal Services | Medium | High | Keep informed | Terminal autonomy, event feeds from Navis N4 | Terminal interface view, resilience view |
| Heads of Ocean & Air Forwarding (regional) | Medium | High | Keep informed | Booking workflow, cut-over timing, training | Business process and capability views |
| Head of Customs Brokerage | Medium | High | Keep informed | Filing continuity to CBP ACE, ICS2, CBSA CARM | Customs interface view |
| Marieke de Vries, DPO | Medium | High | Manage closely | Residency, TIAs, data subject rights | Data residency view, data flow diagrams |
| Omar Haddad, Head of IT Gulf | Medium | High | Keep informed | Gulf lane timing, UAE PDPL | Regional deployment view |
| Nordhaven Freight management | Medium | High | Keep informed | Migration off Nordhaven TMS, staff impact | Migration plan for TA2 |
| Domain architects (Osei, Vogel, Watanabe, Raman, Nowak) | Medium | High | Manage closely | Standards compliance, technical debt | Domain-specific views |
| Harbourline Digital product owners | Low | High | Keep informed | Portal visibility features, API availability | API catalogue, event catalogue |
| Finance operations (billing) | Low | Medium | Keep informed | Invoice data quality | Data lineage for billing |
| Service desk & operations support | Low | Medium | Monitor | Support model, runbooks | Operational view |
| Delivery partner (selected in Phase G) | Medium | High | Manage closely | Clear requirements, acceptance criteria | ARS-01, architecture contract |
| Key customers (top 40 accounts) | Low | High | Keep informed (via Sales) | Visibility, reliability, data protection | Customer-facing release notes |
| Regulators (via Compliance) | High | Low | Keep satisfied | Evidence of controls | Compliance summaries prepared by CISO/DPO |
| Works council, Nordhaven Freight GmbH | Medium | Medium | Keep satisfied | Consultation on process and system changes | Change impact summaries |

## 4. Stakeholder Concerns by Theme

| Theme | Stakeholders | How concerns are addressed |
|---|---|---|
| Continuity of terminal operations | Michael Torres, Tomasz Nowak | Terminals remain autonomous per AP-04; no HSP cut-over during peak freeze |
| Data protection | Marieke de Vries, Lena Vogel | Residency placement agreed in Phase C before build; AP-06 |
| Compliance evidence | Hannah Brennan, Compliance | Compliance by design (AP-02); controls mapped per regulation |
| Financial benefits | Rachel Kim, Elena Marsh | Benefits tracked monthly against A-01 KPIs |
| Workforce change | Regional forwarding heads, works council | Early process walk-throughs; training plan in F-01 |
| AI-assisted features | Priya Raman, business owners | Any AI feature follows AP-16 with a named accountable owner |

## 5. Communications Matrix

| Audience | Message / content | Channel | Frequency | Owner |
|---|---|---|---|---|
| Horizon 2028 Steering Committee (CIO, CFO, CISO, VP Port & Terminal Services) | Progress vs roadmap, KPI trend, top risks, decisions needed | Steering meeting + one-page brief | Monthly | Grace Liu |
| Board (via CIO) | Programme status, benefits, major risks | Board paper | Quarterly | Elena Marsh |
| Architecture Review Board | Deliverables for approval, exceptions, compliance results | ARB session | Weekly (Thursday) | Samuel Adeyemi |
| Domain architects | Design decisions, ADRs in draft, standards changes | Architecture guild meeting + repository notifications | Fortnightly | David Okafor |
| Business process owners (forwarding, customs) | Process changes, cut-over plans, UAT windows | Workshops, SharePoint programme site | Per phase; monthly minimum | Grace Liu |
| DPO and privacy team | Data flows, residency decisions, TIA requests | Review meeting | Monthly and on demand | Lena Vogel |
| CISO and security team | Threat models, security exceptions, test results | Security design review | Monthly | Priya Raman |
| Terminal management (four terminals) | Interface changes, integration test windows | Terminal operations call | Monthly | Tomasz Nowak |
| Harbourline Gulf IT | Gulf-specific scope, regional deployment decisions | Video call | Monthly | Omar Haddad / Kenji Watanabe |
| Nordhaven staff and works council | Migration timeline, role impacts | Town hall + written summary (German and English) | Quarterly | Grace Liu with Nordhaven HR liaison |
| All IT staff | Programme overview, standards to follow, wins | Intranet article, all-hands segment | Quarterly | Samuel Adeyemi |
| Key customers | Visibility improvements, release dates | Account manager briefings, release notes | Per release | Harbourline Digital product lead |
| Delivery partner | Requirements changes, compliance findings | Contract governance meeting | Fortnightly | David Okafor |

## 6. Feedback and Escalation

1. Stakeholder feedback is logged in the programme RAID log and reviewed at the monthly steering committee.
2. Architecture concerns that cannot be resolved by the domain architect are raised to the ARB.
3. Scope or budget conflicts escalate to Elena Marsh as sponsor.
4. The stakeholder map is reviewed at each phase gate and whenever a new region, legal entity, or regulator enters scope.

## 7. Measures of Communication Effectiveness

| Measure | Target |
|---|---|
| Steering pack issued ≥ 2 working days before meeting | 100% |
| Business owner sign-off on process changes before UAT | 100% |
| Stakeholder pulse survey "I understand what is changing and when" | ≥ 75% agree |
| Open stakeholder concerns older than 60 days | 0 |

## 8. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2024-12-13 | Samuel Adeyemi | Initial approved version |
| 1.1 | 2025-05-30 | Samuel Adeyemi | Delivery partner added after selection |
| 1.2 | 2025-11-14 | Samuel Adeyemi | Frequencies adjusted after TA1 go-live |
