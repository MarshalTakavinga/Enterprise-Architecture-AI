---
doc_id: ADR-0036
title: Replace MPLS WAN with Fortinet Secure SD-WAN
doc_type: adr
version: "1.1"
status: Accepted
owner: Tomasz Nowak, Lead Network & OT Architect
approved_by: Architecture Review Board (ARB-2023-041)
effective_date: 2023-10-17
next_review: 2026-10-17
classification: Internal
related: [AP-04, AP-12, AP-13, AP-14, STD-NET-011, STD-TLC-014, STD-RES-015, ADR-0027, RA-03, GOV-02]
---

# ADR-0036 — Replace MPLS WAN with Fortinet Secure SD-WAN

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted (implemented 2025) |
| Date | 2023-10-17 |
| ARB decision | ARB-2023-041 (session of Thursday 2023-10-12), Approved |
| Deciders | David Okafor (Chair), Tomasz Nowak, Priya Raman, Kenji Watanabe, Amara Osei |
| Consulted | Hannah Brennan (CISO), Rachel Kim (CFO office), regional IT managers incl. Omar Haddad |
| Review tier | Tier 1 (cost > USD 500k, all sites) |
| Revision 1.1 | Implementation status updated; last MPLS circuit (Halifax) decommissioned March 2025, closing EXC-2024-007 |

## 2. Context

Harbourline's wide-area network connects about 60 sites (offices, warehouses and the four container terminals) through MPLS contracts with three carriers. In 2023:

- MPLS costs USD 4.6M/year; the median site has 50 Mbps at ~USD 5,200/month.
- Over 70% of traffic now goes to SaaS and Azure, but is backhauled through Baltimore and Rotterdam hubs for internet breakout, adding 40-120 ms to Microsoft 365 and Salesforce sessions.
- New circuits take 60-90 days to provision; the Jebel Ali terminal waited 118 days in 2022.
- Terminals have a single MPLS circuit with ISDN-era backup; two terminal outages in 2023 exceeded 6 hours.
- Site security is a mix of branch routers with ACLs and three firewall vendors, making consistent policy impossible.

The major MPLS contracts expire between June 2024 and March 2025.

## 3. Decision Drivers

1. Cost reduction on WAN spend.
2. Direct, secured internet and cloud breakout at site.
3. Resilience at terminals (dual paths, cellular backup) supporting AP-04.
4. Consolidated network security with a single policy model and central management.
5. Segmentation capability for IT/OT separation at terminals (AP-13).
6. Network team skills: 11 engineers, 7 of whom hold Fortinet certifications from existing data centre firewalls.

## 4. Considered Options

- **Option A — Renew MPLS** with bandwidth uplift and a cloud-delivered security overlay for internet traffic.
- **Option B — Fortinet Secure SD-WAN (FortiGate)** at every site with FortiManager/FortiAnalyzer, dual broadband/DIA, and LTE/5G backup at terminals.
- **Option C — Cisco Catalyst SD-WAN** with separate branch firewalls.

### 4.1 Comparison

| Criterion | A — Renew MPLS | B — Fortinet SD-WAN | C — Cisco SD-WAN + firewalls |
|---|---|---|---|
| 5-year TCO (est.) | USD 24.5M | USD 13.8M | USD 17.9M |
| Local breakout with inspection | Via overlay; extra licence | Native NGFW with SSL inspection | Requires separate firewall |
| Terminal resilience | Single carrier dependence | Dual ISP + LTE/5G, sub-second path steering | Dual ISP + LTE/5G |
| Devices per site | Router + overlay | One FortiGate pair | Router + firewall |
| OT segmentation support | Limited | Industrial signatures, zone policies | Via firewalls |
| Provisioning time for new site | 60-90 days | 2-3 weeks (zero-touch) | 3-4 weeks |
| Team skills fit | High | High | Medium |

## 5. Decision Outcome

**Chosen option: B — Replace MPLS with Fortinet Secure SD-WAN at all ~60 sites.**

Design summary (details in STD-NET-011 and RA-03):

- **Offices and warehouses:** single or HA FortiGate depending on headcount; two diverse internet circuits (one DIA, one broadband) per site.
- **Terminals:** HA FortiGate pair, **dual ISP** (diverse physical entry) **plus LTE/5G backup**; application steering keeps Navis-related replication and voice on the best path; sub-second failover measured in the pilot.
- **Cloud:** SD-WAN overlay terminates on FortiGate virtual appliances in Azure hub VNets in East US 2 and West Europe.
- **Internet breakout:** local breakout at site with SSL inspection, except health and banking categories, which are exempted for privacy reasons.
- **Management:** FortiManager and FortiAnalyzer, with logs forwarded to Microsoft Sentinel.
- **OT:** terminal FortiGates enforce the IT/OT boundary and DMZ policies; no direct internet from OT levels 0-2.

Rollout in four waves over 2024-2025, sequenced by MPLS contract expiry; terminals last, each with a 30-day dual-running period.

## 6. Consequences

### 6.1 Positive

- Target WAN saving of ~USD 2.1M/year once MPLS is fully exited (FY2026 run rate).
- Microsoft 365 and Salesforce latency drops by 40-120 ms for sites that previously backhauled.
- Terminal connectivity becomes triple-path, removing single-carrier outages.
- One security policy model across sites, improving audit readiness for NIS2 and emerging maritime cybersecurity regulation.

### 6.2 Negative

- Heavy concentration on a single vendor for WAN and perimeter security; a critical FortiOS vulnerability would affect every site at once. Requires a tested emergency patch process (target: critical patches within 72 hours).
- Broadband circuits carry no carrier SLA comparable to MPLS; service quality now depends on path diversity and monitoring.
- SSL inspection raises privacy and certificate-management overhead and breaks some partner applications, requiring an exemption list.
- Hardware refresh obligations every 5-7 years; capital spend of ~USD 3.2M across 2024-2025.
- Local ISP procurement in 11 countries adds vendor management effort for the network team.

### 6.3 Neutral

- MPLS moves to Retire on the technology radar, with removal completed in 2025.

### 6.4 Follow-up actions

| Action | Owner | Due | Status |
|---|---|---|---|
| Pilot at Baltimore office and BAL-T1 | Tomasz Nowak | 2024-03-31 | Done |
| Wave rollout, offices and warehouses | Tomasz Nowak | 2024-12-31 | Done |
| Terminal cutovers (HFX-T1 under EXC-2024-007 until complete) | Tomasz Nowak | 2025-03-31 | Done |
| Publish network standard (STD-NET-011) | Tomasz Nowak | 2024-06-30 | Done |
| Emergency firmware patch runbook | Priya Raman / Tomasz Nowak | 2024-02-29 | Done |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-04 Business Continuity at the Quay | Supports; resilient WAN complements edge-hosted terminal systems (ADR-0027). |
| AP-12 Zero Trust Access | Partially; SD-WAN provides segmentation and inspection, identity-based access is enforced elsewhere. |
| AP-13 Separate IT and OT | Compliant; FortiGate enforces zones and conduits at terminals. |
| AP-14 Observable by Default | Compliant; FortiAnalyzer and Sentinel. |
| STD-NET-011 | This ADR is the basis for the SD-WAN clauses of that standard. |

## 8. Links

- STD-NET-011 Network Security, SD-WAN & OT Segmentation Standard
- RA-03 Terminal Edge & OT Connectivity
- ADR-0027 Edge-Hosted Terminal Operating System with Local Failover
- GOV-02 Architecture Exceptions Register (EXC-2024-007, closed)
- ARB log entry ARB-2023-041
