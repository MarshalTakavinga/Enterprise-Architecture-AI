---
doc_id: ADR-0027
title: Edge-Hosted Terminal Operating System with Local Failover
doc_type: adr
version: "1.0"
status: Accepted
owner: Tomasz Nowak, Lead Network & OT Architect
approved_by: Architecture Review Board (ARB-2024-015)
effective_date: 2024-04-09
next_review: 2026-04-09
classification: Confidential
related: [AP-04, AP-10, AP-13, STD-NET-011, STD-RES-015, STD-CLD-007, ADR-0036, RA-03, APP-030, APP-031]
---

# ADR-0027 — Edge-Hosted Terminal Operating System with Local Failover

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2024-04-09 |
| ARB decision | ARB-2024-015 (session of Thursday 2024-04-04), Approved |
| Deciders | David Okafor (Chair), Tomasz Nowak, Priya Raman, Kenji Watanabe, Amara Osei |
| Consulted | Michael Torres (VP Port & Terminal Services), terminal IT managers for BAL-T1, HFX-T1, RTM-T2, JEA-T4, Omar Haddad |
| Review tier | Tier 1 (Tier 0 service, OT impact) |

## 2. Context

Navis N4 (APP-030) is the terminal operating system at all four Harbourline container terminals. Gate automation (APP-031) and crane control interfaces depend on it. At RTM-T2, the busiest terminal, N4 processes ~9,000 container moves on a typical day and up to 1,100 moves/hour during peak discharge.

With cloud migration under way, the ARB was asked whether N4 should move to Azure as part of the data centre exit. Today each terminal runs N4 on ageing single servers with nightly backups; a hardware failure at HFX-T1 in November 2023 stopped quay operations for 3 hours 40 minutes, with two vessels delayed.

Constraints:

- Equipment dispatch requires round-trip latency under 50 ms between N4 and handheld/vehicle terminals; measured WAN latency from terminals to the nearest Azure region ranges from 12 ms (Rotterdam) to 38 ms (Jebel Ali) on a good day, with spikes above 200 ms.
- Terminals must keep working through loss of WAN or cloud for up to 72 hours (AP-04), e.g., during a regional cloud outage or a cable cut.
- Crane and gate interfaces sit in OT zones that must not have direct internet access (AP-13, STD-NET-011).

## 3. Decision Drivers

1. Operational continuity at the quay: Tier 0 targets of RTO 15 min, RPO 0-5 min, and 72-hour autonomy.
2. Deterministic low latency to equipment.
3. IT/OT separation and IEC 62443 zoning.
4. Vendor supportability of the chosen N4 deployment model.
5. Enable cloud analytics and customer visibility using terminal data.
6. Cost relative to the risk of a terminal stoppage (estimated at USD 180k-250k per hour at RTM-T2 in vessel delay, overtime and penalties).

## 4. Considered Options

- **Option A — Cloud-hosted N4 in Azure** per region, with terminals connected over SD-WAN.
- **Option B — Edge-hosted N4 on a 2-node cluster at each terminal**, with asynchronous replication to Azure for DR copy and analytics.
- **Option C — Status quo** (single server per terminal, nightly backup).

### 4.1 Comparison

| Criterion | A — Cloud-hosted | B — Edge 2-node cluster | C — Status quo |
|---|---|---|---|
| Survives 72-hour WAN/cloud loss | No | Yes | Yes, but no hardware resilience |
| Latency to equipment | 12-38 ms typical, unbounded spikes | < 2 ms (local) | < 2 ms |
| Local hardware failure RTO | N/A | ~5 min (automatic failover) | 4-8 h (restore) |
| RPO | Near-zero | Near-zero locally (synchronous replication between nodes) | Up to 24 h |
| Cost (4 terminals, 5 years) | USD 2.3M (compute, redundant WAN upgrades) | USD 1.9M (hardware, virtualisation, support) | USD 0.7M |
| Contribution to DC exit | Yes | Neutral (terminals are not in the Baltimore DC) | Neutral |
| Vendor support | Supported, but vendor recommends local deployment for quay-critical sites | Supported reference deployment | Supported |

## 5. Decision Outcome

**Chosen option: B — Navis N4 remains on-premises at each terminal on a 2-node edge cluster.** Cloud is used only for replication, DR copies and analytics.

Design elements (detailed in RA-03):

- Two hyperconverged nodes per terminal in separate rooms (different fire compartments), with synchronous storage replication and automatic failover; tested failover target under 5 minutes.
- N4 application and database servers are virtual machines on the cluster; UPS runtime of at least 4 hours plus generator.
- The cluster sits in the terminal operations zone (Purdue level 3); crane and gate interfaces connect through defined conduits. Nothing in levels 0-2 gains internet access.
- One-way replication of operational data (moves, container events, vessel visits) to Azure via a broker in the IT/OT DMZ (level 3.5); no inbound connections from cloud to the operations zone.
- Encrypted nightly backup copies to Azure in the terminal's jurisdiction (West Europe for RTM-T2, UAE North for JEA-T4, Canada Central for HFX-T1, East US 2 for BAL-T1).
- Semi-annual failover and 72-hour isolation drills per STD-RES-015.

## 6. Consequences

### 6.1 Positive

- Terminals continue operating through WAN or cloud outages, meeting AP-04.
- Hardware failure RTO falls from hours to minutes.
- Terminal events reach the cloud with a target lag under 2 minutes.

### 6.2 Negative

- Harbourline keeps owning physical infrastructure at four sites: hardware refresh every 5-6 years, spares, and on-site hands (estimated 0.5 FTE per terminal).
- Two operating models (edge and cloud) for infrastructure and patching; OT change windows limit patch cadence to monthly at best.
- Cloud analytics see terminal data only after DMZ replication; during an outage, customer visibility of terminal milestones stalls until replication catches up.
- Capital spend of ~USD 1.1M in FY2024-FY2025 must come from the Port & Terminal Services budget.

### 6.3 Neutral

- The Baltimore DC exit is unaffected because terminal servers are not hosted in the data centre.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Publish RA-03 Terminal Edge & OT Connectivity | Tomasz Nowak | 2024-06-30 |
| Deploy edge clusters: HFX-T1 first, then RTM-T2, BAL-T1, JEA-T4 | Tomasz Nowak | 2025-03-31 |
| Define DMZ broker topics and replication SLOs | Amara Osei | 2024-07-31 |
| First 72-hour isolation drill | Michael Torres / Tomasz Nowak | 2025-05-31 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-04 Business Continuity at the Quay | Directly satisfies the 72-hour autonomy requirement. |
| AP-13 Separate IT and OT | Compliant; DMZ-mediated, one-way replication. |
| AP-10 Cloud-Smart and Portable | Consistent: cloud-smart means not placing latency-critical Tier 0 workloads in cloud. |
| STD-NET-011 | IEC 62443 zones and conduits, no internet from levels 0-2. |
| STD-RES-015 | Meets Tier 0 RTO/RPO and semi-annual test cadence. |
| AP-11 Managed Services | Deviation accepted; no managed service meets the continuity requirement. |

## 8. Links

- RA-03 Terminal Edge & OT Connectivity
- STD-RES-015 Resilience & Disaster Recovery Standard; STD-NET-011
- ADR-0036 Replace MPLS WAN with Fortinet Secure SD-WAN
- APP-030 Navis N4; APP-031 Terminal Gate Automation
- ARB log entry ARB-2024-015
