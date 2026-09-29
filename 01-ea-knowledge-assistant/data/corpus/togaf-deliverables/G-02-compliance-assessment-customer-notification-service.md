---
doc_id: G-02
title: Compliance Assessment — Customer Notification Service (APP-055)
doc_type: togaf_deliverable
togaf_phase: G
version: "1.0"
status: Approved
owner: Samuel Adeyemi, Head of Enterprise Architecture Office / ARB Secretary
approved_by: Architecture Review Board (ARB-2026-031)
effective_date: 2026-08-20
next_review: 2026-10-15
classification: Internal
related: [GOV-01, GOV-02, AP-06, AP-08, AP-14, STD-INT-001, STD-EVT-003, STD-DAT-004, STD-DAT-005, STD-OBS-010, ADR-0015, ADR-0030, ADR-0038, RA-01]
---

# G-02 — Compliance Assessment — Customer Notification Service (APP-055)

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Review Summary

| Item | Value |
|---|---|
| ARB decision ID | ARB-2026-031 |
| Meeting date | 2026-08-20 (Thursday ARB) |
| Application | Customer Notification Service (CNS), APP-055 |
| Business owner | Harbourline Digital |
| Solution architect | Julia Brandt |
| Review tier | Tier 1 — new system processing personal data with a proposed cross-border transfer |
| ARB attendees | David Okafor (Chair), Priya Raman (Security), Amara Osei (Integration), Lena Vogel (Data), Kenji Watanabe (Cloud); Marieke de Vries (DPO, advisory); Samuel Adeyemi (Secretary) |
| Quorum | Met (Chair + 4 voting members incl. Security) |
| **Decision** | **Changes Requested** |

## 2. Purpose of the Assessment

CNS will send shipment alerts to customers by email, SMS and push notification when milestones occur (for example, "container discharged at RTM-T2" or "customs hold"). The service supports the Horizon 2028 visibility goal and principle AP-01. This assessment checks the submitted solution design (version 0.9, dated 2026-08-06) against the enterprise standards and principles before build approval.

## 3. Solution as Submitted

- Hosting: Azure Container Apps in the `hlg-online` landing zone, US region (East US 2), with a planned EU instance.
- Trigger: a scheduler polls the HSP shipment query API every 30 seconds per active subscription to detect new milestones.
- Channels: email via Azure Communication Services; SMS via Twilio (US region) for all customers, including EU phone numbers; push via the Harbourline Connect mobile app.
- Templating: email templates rendered by an existing MuleSoft flow reused from the legacy portal notifications.
- Data: customer contact preferences (email, mobile number) held in a PostgreSQL Flexible Server database; classification proposed as Confidential.
- Observability: OpenTelemetry SDK, W3C trace context, dashboards in Grafana, SLOs defined.

## 4. Findings

| Finding ID | Area | Standard clause | Verdict | Evidence | Required action |
|---|---|---|---|---|---|
| CNS-F1 | Integration | STD-INT-001 INT-P1 (Domain Event Publication); AP-08 | **Non-compliant** | Design §5.2 shows REST polling of HSP every 30 s. At 180,000 active subscriptions this generates about 6,000 requests/s against HSP, far above the 1,000 req/min per-client default in STD-API-002, and it duplicates change detection that HSP already performs. | Subscribe to `shipment.milestone.recorded.v1` on the Event Backbone as a consumer group, following RA-01 and ADR-0030. Consumer MUST be idempotent with a DLQ topic `shipment.milestone.recorded.v1.dlq` (STD-EVT-003). Remove the polling scheduler. |
| CNS-F2 | Data residency | STD-DAT-005 (cross-border transfer; TIA and SCCs) | **Needs review** | Twilio US region would process mobile numbers and message content of EU data subjects in the United States. Exception EXC-2026-004 has been requested but is **not approved**. No Transfer Impact Assessment has been submitted. | Complete a TIA for DPO approval, or use an SMS provider configuration that processes EU numbers in the EU. This finding requires human judgement by the DPO; the ARB will not decide it on standards alone. |
| CNS-F3 | Integration technology | ADR-0015; STD-INT-001 (no new MuleSoft flows after 2025-06-30); STD-TLC-014 (MuleSoft = Contain) | **Non-compliant** | Design §6.1 reuses a MuleSoft flow for email templating. Reuse would add a new consumer dependency to a platform being decommissioned on 2026-12-31. | Render templates inside CNS (or with Azure Communication Services templates). No dependency on APP-122 is permitted. |
| CNS-F4 | Observability | STD-OBS-010 | **Compliant** | OpenTelemetry SDK, W3C trace context, health endpoints and SLOs (delivery within 2 min of event receipt, 99.5%) documented; log sampling excludes phone numbers and email addresses. | None. Keep the log-redaction test in the pipeline. |

### 4.1 Observations (not findings)

- The data classification of Confidential is accepted for the contact-preference store as designed. If CNS stores message history containing shipment and personal details for EU customers in bulk, Lena Vogel will reassess against STD-DAT-004 Restricted criteria.
- The EU instance should be deployed as part of the Harbourline Connect EU stamp in West Europe, consistent with ADR-0041.

## 5. Decision

The ARB decided **Changes Requested** (ARB-2026-031). CNS may not proceed to build or production until the conditions below are met and the design is resubmitted.

### 5.1 Conditions

| # | Condition | Owner | Due |
|---|---|---|---|
| C1 | Replace polling with an event subscription to `shipment.milestone.recorded.v1` (resolves CNS-F1). | Julia Brandt | 2026-10-01 |
| C2 | Remove the MuleSoft templating dependency (resolves CNS-F3). | Julia Brandt | 2026-10-01 |
| C3 | Submit a TIA to the DPO for the Twilio US option, or a revised design processing EU numbers in the EU (resolves CNS-F2). Until then, SMS MUST NOT be enabled for EU phone numbers in any environment containing real data. | Julia Brandt with Marieke de Vries | 2026-10-01 |
| C4 | EXC-2026-004 remains at status Requested. The ARB will consider it only together with the DPO's TIA outcome. | Samuel Adeyemi | With resubmission |

### 5.2 Resubmission

Resubmission is scheduled for the ARB meeting on **Thursday 2026-10-15**. The resubmitted design will be reviewed as Tier 1. If C1 and C2 are met and the DPO approves a TIA or an EU-processing design, the expected outcome is Approved or Approved with Conditions.

## 6. Guidance for the Resubmitted Design

The ARB members offered the following guidance to Julia Brandt. It is advisory and does not add conditions.

- **Consumer design (Amara Osei):** use a dedicated consumer group `cns-notifier` and de-duplicate on the event ID so that redelivery after a rebalance does not send a second SMS. Notification preferences should be looked up from the local CNS database, not from HSP, to keep call chains within the three-hop limit of STD-INT-001.
- **Latency budget (Kenji Watanabe):** the end-to-end target for an alert is the HSP milestone latency (REQ-HSP-014, < 5 min p95) plus the CNS delivery SLO. The resubmission should show the combined budget and the alerting thresholds that protect it.
- **Personal data in events (Priya Raman):** milestone events do not carry phone numbers or email addresses, and CNS must not publish any events that do unless the fields are encrypted at field level (STD-EVT-003).
- **Regional deployment (Lena Vogel):** EU contact preferences belong in West Europe from the first release; the US instance must not hold EU subscribers, even temporarily during testing with real data.

## 7. Rationale

Polling contradicts the event-first principle (AP-08) and would place unnecessary load on a Tier 1 system. HSP already publishes the milestone facts CNS needs through the transactional outbox (ADR-0038), so subscribing is simpler and gives lower latency. Reusing MuleSoft would create a dependency on a platform that is being removed, and new MuleSoft use has been prohibited since mid-2025. The cross-border transfer question is a legal-risk judgement for the DPO, so the ARB records it as needing review and does not approve the requested exception in advance.

## 8. Record

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-08-20 | Samuel Adeyemi | Assessment and decision recorded |
