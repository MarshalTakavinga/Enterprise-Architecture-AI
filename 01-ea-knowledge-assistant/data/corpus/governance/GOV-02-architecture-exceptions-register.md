---
doc_id: GOV-02
title: Architecture Exceptions Register
doc_type: governance
togaf_phase: G
version: "2026.09"
status: Active
owner: Samuel Adeyemi, Head of Enterprise Architecture Office / ARB Secretary
approved_by: Architecture Review Board (maintained under GOV-01 §9)
effective_date: 2026-09-10
next_review: 2026-10-08
classification: Internal
related: [GOV-01, STD-CLD-007, STD-DB-006, STD-TLC-014, STD-DAT-005, STD-NET-011, ADR-0021, ADR-0036, G-02]
---

# GOV-02 — Architecture Exceptions Register

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This register records every architecture exception (dispensation) requested under the process in GOV-01 §9. An exception permits a named system to deviate from a named standard clause for a limited period, under compensating controls and with a remediation plan. The register is the authoritative source for exception status; ARB minutes and ADRs refer to it by `EXC-YYYY-NNN`.

## 2. Register Rules

- Exceptions last at most 12 months and may be renewed once (GOV-01 §9 step 6).
- Status values: *Requested*, *Approved*, *Approved with Conditions*, *Rejected*, *Expired*, *Closed*.
- A *Requested* exception grants no permission. The system must not go live in the non-conforming state until the exception is approved.
- The ARB Secretary reviews this register monthly and notifies owners 60 days before expiry.
- Gaps in the numbering sequence are requests withdrawn before registration was completed.

## 3. Register Summary (as at 2026-09-10)

| ID | System | Standard deviated from | Status | Expiry | Remediation owner | Decision |
|---|---|---|---|---|---|---|
| EXC-2025-003 | Nordhaven TMS (APP-021) | STD-CLD-007 §4 (Azure primary hosting) | Approved — renewed once | 2026-12-31 | Grace Liu | ARB-2025-003; renewal ARB-2025-088 |
| EXC-2026-001 | FreightMaster TMS (APP-020) | STD-TLC-014 (Oracle 12c and Java 8 = Retire); STD-DB-006 (Oracle = Contain) | Approved with Conditions | 2027-03-31 | Grace Liu | ARB-2026-012 |
| EXC-2026-002 | Terminal Gate Automation servers (APP-031) | STD-TLC-014 (Windows Server 2012 R2 = Retire, overdue) | Approved with Conditions | 2026-11-30 | Tomasz Nowak | ARB-2026-008 |
| EXC-2026-004 | Customer Notification Service (APP-055) | STD-DAT-005 (EU personal data processed outside EU without approved TIA) | **Requested — not approved** | n/a | Julia Brandt | Pending; linked to ARB-2026-031 |
| EXC-2024-007 | Halifax site WAN (HFX-T1 and Halifax office) | STD-NET-011 (SD-WAN at all sites) | Closed 2025-03 | 2025-03-31 (was) | Tomasz Nowak | ARB-2024-061 |

## 4. Active Exceptions

### 4.1 EXC-2025-003 — Nordhaven TMS hosted on AWS eu-central-1

| Field | Detail |
|---|---|
| System | APP-021 Nordhaven TMS (Java 11, MongoDB Atlas) |
| Standard and clause | STD-CLD-007 §4 — Azure is the primary cloud; AWS permitted only for approved cases. Also relies on STD-DB-006 MongoDB Atlas = Trial (Nordhaven only). |
| Requested by | Kenji Watanabe on behalf of the HSP programme |
| Original approval | ARB-2025-003, 2025-01-09, valid to 2025-12-31 |
| Renewal | ARB-2025-088, 2025-11-20, valid to 2026-12-31 (renewal limit reached) |
| Related decision record | ADR-0021 |

**Justification.** Re-platforming Nordhaven TMS to Azure ahead of its planned migration into HSP would duplicate effort. The system serves German and Central European lanes that move to HSP in Transition Architecture 2.

**Compensating controls.**
- Connectivity to Azure only via Confluent cluster linking and AWS PrivateLink; no public endpoints (ADR-0021).
- Workforce access federated to Entra ID with MFA; AWS IAM Identity Center local users disabled.
- Data remains in eu-central-1 (EU), satisfying STD-DAT-005 residency.
- AWS CloudTrail and GuardDuty findings forwarded to Microsoft Sentinel.
- No new functionality; changes limited to regulatory and defect fixes.

**Remediation plan.** Migrate Nordhaven lanes to HSP under F-01 work packages targeting Q2 2027; decommission the AWS account within 60 days of final cutover.

**Current position.** The migration target falls after the renewed expiry of 2026-12-31 and the exception cannot be renewed again. The ARB Chair escalated the gap to the CIO on 2026-09-03 under GOV-01 §10. The options before the CIO are to accelerate the cutover or to accept a time-bound CIO dispensation. Decision pending.

### 4.2 EXC-2026-001 — FreightMaster on Oracle 12c extended support

| Field | Detail |
|---|---|
| System | APP-020 FreightMaster TMS, Baltimore data centre |
| Standard and clause | STD-TLC-014 radar: Oracle 12c = Retire (2027-03-31), Java 8 = Retire (2026-06-30); STD-DB-006: Oracle Database = Contain |
| Requested by | Grace Liu, Programme Director |
| Approval | ARB-2026-012, 2026-03-19, Approved with Conditions, valid to 2027-03-31 |

**Justification.** FreightMaster still processes lanes not yet migrated to HSP. Upgrading Oracle and Java for a system being retired offers no lasting value and would divert HSP engineering capacity.

**Compensating controls.**
- Oracle extended support contract in force to 2027-03-31; quarterly security patches applied within 30 days.
- Database hosts isolated in a dedicated data-centre segment; access only through PIM-elevated DBA accounts.
- Java 8 runtime pinned to the last vendor-supported build; no new libraries added.
- Change freeze except regulatory, security and migration-enabling changes.

**Conditions.** (1) Monthly migration burndown reported to ARB; (2) no new integrations to FreightMaster; (3) remaining MuleSoft flows serving FreightMaster decommissioned by 2026-12-31.

**Remediation plan.** Transactional use of FreightMaster ends as remaining lanes move to HSP. Historical records move to a read-only archive on PostgreSQL Flexible Server before 2027-03-31, removing Oracle 12c. Full application retirement is in Q3 2027 per F-01.

### 4.3 EXC-2026-002 — Windows Server 2012 R2 on terminal gate servers

| Field | Detail |
|---|---|
| System | APP-031 Terminal Gate Automation — 14 OCR gate servers (BAL-T1: 5, HFX-T1: 3, RTM-T2: 4, JEA-T4: 2) |
| Standard and clause | STD-TLC-014 radar: Windows Server 2012 R2 = Retire (overdue) |
| Requested by | Tomasz Nowak, Lead Network & OT Architect |
| Approval | ARB-2026-008, 2026-02-26, Approved with Conditions, valid to 2026-11-30 |

**Justification.** The gate OCR vendor certifies its current release only on Windows Server 2012 R2. The certified Windows Server 2022 release became available in Q1 2026 and requires on-site gate lane testing, which must be scheduled around vessel windows to protect Tier 0 throughput (AP-04).

**Compensating controls.**
- Paid Extended Security Updates applied monthly.
- Servers sit in the Purdue level 2 OT zone with no internet access (STD-NET-011); inbound management only via the OT jump host with session recording.
- Application allow-listing enforced; USB mass storage disabled.
- FortiGate IPS signatures for legacy SMB and RDP threats enabled on the zone conduit.
- Quarterly vulnerability scans reviewed by Priya Raman.

**Conditions.** Upgrade sequence approved by Michael Torres for each terminal; monthly status to ARB.

**Remediation plan.** Upgrade to Windows Server 2022 terminal by terminal: HFX-T1 (complete 2026-07), JEA-T4 (2026-09), RTM-T2 (2026-10), BAL-T1 (2026-11). Owner: Tomasz Nowak.

### 4.4 EXC-2026-004 — CNS use of Twilio US region for EU phone numbers

| Field | Detail |
|---|---|
| System | APP-055 Customer Notification Service |
| Standard and clause | STD-DAT-005 — EU personal data processed in West Europe/North Europe only; cross-border transfer requires DPO-approved TIA and SCCs |
| Requested by | Julia Brandt, Solution Architect |
| Status | **Requested — not approved.** Registered 2026-08-21 following ARB-2026-031 |

**Justification (as submitted).** Twilio's SMS service would process EU customer phone numbers in its US region. The team argues that an EU-region option adds cost and latency.

**Proposed compensating controls.** SCCs with the provider; message content limited to shipment reference and milestone; phone numbers not retained by the provider beyond delivery logs.

**Assessment status.** No Transfer Impact Assessment has been submitted to the DPO, Marieke de Vries. Lena Vogel has asked the team to evaluate an EU-region processing option before the ARB hears the request. Until a decision is recorded, CNS MUST NOT send SMS to EU data subjects through a US-region service.

**Remediation plan.** To be provided with the TIA.

## 5. Closed Exceptions

### 5.1 EXC-2024-007 — MPLS retained at Halifax until SD-WAN cutover

| Field | Detail |
|---|---|
| System | Halifax office and HFX-T1 terminal WAN |
| Standard and clause | STD-NET-011 (then v1.x) — Fortinet Secure SD-WAN at all sites |
| Approval | ARB-2024-061, 2024-09-26, valid to 2025-03-31 |
| Remediation owner | Tomasz Nowak |

**Justification.** Delivery of the second ISP circuit at HFX-T1 was delayed by the carrier, preventing a resilient SD-WAN cutover.

**Compensating controls.** MPLS circuit retained with existing encryption; FortiGate pair installed in parallel.

**Closure.** SD-WAN cutover completed and MPLS circuit terminated in March 2025, completing the ADR-0036 rollout. Closed by the ARB Secretary on 2025-03-27.

## 6. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 2026.08 | 2026-08-21 | Samuel Adeyemi | EXC-2026-004 registered |
| 2026.09 | 2026-09-10 | Samuel Adeyemi | EXC-2025-003 CIO escalation noted; EXC-2026-002 progress updated |
