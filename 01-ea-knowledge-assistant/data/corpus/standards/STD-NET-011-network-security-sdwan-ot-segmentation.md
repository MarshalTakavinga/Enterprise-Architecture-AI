---
doc_id: STD-NET-011
title: Network Security, SD-WAN & OT Segmentation Standard
doc_type: standard
version: "2.0"
status: Approved
owner: Tomasz Nowak, Lead Network & OT Architect
approved_by: Architecture Review Board (ARB-2025-049)
effective_date: 2025-08-01
next_review: 2026-11-01
classification: Internal
related: [AP-04, AP-12, AP-13, AP-15, STD-SEC-009, STD-IAM-008, STD-CLD-007, STD-OBS-010, STD-RES-015, ADR-0036, ADR-0027, RA-03, GOV-01, GOV-02]
---

# STD-NET-011 — Network Security, SD-WAN & OT Segmentation Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines how Harbourline sites connect to each other and to the cloud, how traffic is segmented and inspected, and how terminal operational technology (OT) is separated from IT. Version 2.0 reflects the completed MPLS replacement (ADR-0036) and the obligations of the US Coast Guard maritime cybersecurity rule (33 CFR Part 101 Subpart F) and EU NIS2 for Harbourline's four container terminals.

## 2. Scope

- All ~60 Harbourline sites: offices, warehouses, the Baltimore data centre and the terminals BAL-T1, HFX-T1, RTM-T2 and JEA-T4, including Nordhaven Freight sites.
- SD-WAN hubs deployed in Azure hub virtual networks.
- Terminal OT networks: crane control interfaces, OCR gates (APP-031), reefer monitoring, and the Navis N4 edge cluster (APP-030, ADR-0027).
- Out of scope: Azure spoke virtual-network design (STD-CLD-007) and identity controls (STD-IAM-008).

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-13 Separate IT and OT | Basis for §9 and §10 |
| AP-12 Zero Trust Access | No implicit trust from network location; identity-aware policy |
| AP-04 Business Continuity at the Quay | Terminals must operate for 72 hours without WAN or cloud |
| AP-15 Everything as Code | FortiManager policy packages and Azure hub config under version control |
| IEC 62443-3-2 / 3-3 | Zones, conduits and security levels for terminal OT |
| STD-SEC-009 | IPsec and TLS cryptographic parameters |
| RA-03 | Reference design for terminal edge and OT connectivity |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Site Classes and Edge Platform

### 4.1 Site classes

| Class | Examples | FortiGate deployment | WAN links |
|---|---|---|---|
| A — Terminal | BAL-T1, HFX-T1, RTM-T2, JEA-T4 | HA pair (IT edge) + separate HA pair (IT/OT DMZ) | 2 diverse ISPs + 5G |
| B — Data centre / hub | Baltimore DC, Azure hubs | HA pair | 2 ISPs or ExpressRoute + Internet |
| C — Warehouse | Contract logistics sites | HA pair | 2 ISPs, or 1 ISP + 5G |
| D — Office | Regional offices | Single unit permitted if < 50 users | 1 ISP + LTE/5G |

### 4.2 Platform rules

1. Every site MUST terminate WAN connectivity on a FortiGate running a FortiOS release approved on the technology radar (STD-TLC-014); releases MUST be no more than one minor train behind the approved baseline.
2. Class A, B and C sites MUST deploy FortiGates as an FGCP active-passive HA pair with session pickup enabled, dedicated heartbeat links, and each unit powered from separate UPS-backed circuits.
3. HA failover MUST be tested at least semi-annually at Class A sites, aligned with Tier 0 DR tests in STD-RES-015.
4. All FortiGates MUST be managed centrally from FortiManager; local changes are prohibited outside a recorded emergency change. Configuration backups MUST be taken daily.

## 5. Underlay

1. Class A sites MUST have two wired Internet circuits from different providers with physically diverse building entry, plus a 5G cellular link (LTE fallback) on a different carrier from both wired providers.
2. At Class A and B sites, the FortiGate MUST run eBGP with each wired ISP, accepting a default route only and advertising only Harbourline provider-independent prefixes where held. BFD SHOULD be enabled where the provider supports it. Class C and D sites MAY use static defaults with link-health monitoring.
3. The 5G link MUST be configured as the lowest-priority SD-WAN member and MUST carry only traffic classified as Tier 0 operational or management traffic when both wired links are down, unless the site's link budget has been approved for full failover.
4. Underlay interfaces MUST NOT accept inbound management access; only IKE/IPsec and BGP from provider neighbours are permitted.

## 6. Overlay and Routing

1. All inter-site and site-to-cloud traffic MUST traverse the IPsec overlay. Overlay tunnels MUST use IKEv2 with AES-256-GCM and DH group 20 or higher, per STD-SEC-009.
2. The overlay is a hub-and-spoke ADVPN design with regional hubs in Azure (East US 2, Canada Central, West Europe, UAE North) plus the Baltimore DC hub until data-centre exit on 30 June 2027. Shortcut tunnels between spokes MAY be negotiated dynamically.
3. Overlay routing MUST use iBGP over the tunnels, with hub FortiGates acting as route reflectors. Each site MUST use a unique private 4-byte ASN from the Harbourline plan held in the network IPAM.
4. Sites MUST advertise summarised prefixes only. OT prefixes (Purdue levels 0-2) MUST NOT be advertised into the overlay under any circumstance.
5. Where a Class A or B site uses OSPF internally on the IT core, redistribution into BGP MUST be filtered by prefix list; default-route redistribution into OSPF MUST originate only from the site FortiGate pair.
6. SD-WAN rules MUST steer traffic using performance SLAs. Minimum SLA for Tier 0 and voice classes: latency ≤ 150 ms, jitter ≤ 30 ms, packet loss ≤ 1%. Navis N4 replication and customs traffic MUST be classed above bulk traffic.

## 7. IT Segmentation and Firewall Policy

1. Site LANs MUST be segmented into at least: user, server, printer/peripheral, building services, management and vendor-device segments, each with its own VLAN and firewall policy on the FortiGate.
2. Firewall policies MUST be default-deny, identity-aware where users are involved (Entra ID via FSSO or FortiClient EMS integration), and MUST NOT use `any` as source, destination and service simultaneously.
3. Policy packages MUST be defined in FortiManager, exported to source control and changed only through approved change records.

## 8. Internet Breakout and Inspection

1. Internet access from sites MUST break out locally through the FortiGate with web filtering, application control, IPS and antivirus profiles applied.
2. Server-originated Internet traffic MUST be restricted to an explicit allow-list of FQDNs.
3. SSL/TLS deep inspection MUST be applied to outbound user traffic, EXCEPT for the FortiGuard categories Health and Wellness and Finance and Banking, which MUST be exempt for privacy reasons, and for destinations on the certificate-pinning exemption list maintained by the Principal Security Architect.

## 9. OT Segmentation

### 9.1 Purdue levels

| Level | Content at Harbourline terminals |
|---|---|
| 0 | Sensors, actuators, crane drives, reefer plug controllers |
| 1 | PLCs, crane and gate controllers |
| 2 | HMIs, OCR gate servers (APP-031), crane control interfaces |
| 3 | Terminal operations: Navis N4 edge cluster (APP-030), historians |
| 3.5 | IT/OT DMZ: data broker, patch staging, OT jump host |
| 4-5 | Corporate IT and cloud |

### 9.2 Rules

1. OT zones at Purdue levels 0-2 MUST NOT have direct Internet access, inbound or outbound.
2. An IT/OT DMZ at level 3.5 is mandatory at every terminal. No traffic flow may traverse from level 4 to level 3 or below without terminating in the DMZ.
3. The DMZ MUST be enforced by a dedicated FortiGate HA pair separate from the IT edge pair.
4. Data from OT to IT and cloud MUST flow outbound through a DMZ broker; inbound flows into OT are permitted only for patch distribution from the DMZ staging server and approved remote access (§10).
5. Each terminal MUST maintain an IEC 62443 zone and conduit model. Zones MUST have an assigned target security level (SL-T); crane control and level 1 zones MUST be SL-T 3, other OT zones at least SL-T 2. Every conduit MUST be documented with its permitted protocols and ports.
6. Industrial protocols (Modbus/TCP, OPC UA, S7) crossing a conduit MUST be controlled with FortiGate industrial application signatures and IPS.
7. Legacy devices that cannot be patched or encrypted, including gate servers under EXC-2026-002, MUST be placed in a dedicated micro-zone with allow-listed conduits only.
8. OT zones MUST remain operable with the WAN down for at least 72 hours (AP-04); no OT function may depend on a cloud or overlay-reachable service.

## 10. Remote Access to OT

1. Remote vendor and engineer access to OT MUST go only through the OT jump host in the level 3.5 DMZ.
2. Sessions MUST be time-bound (approved window, maximum 8 hours), approved per session by the terminal OT owner, authenticated with phishing-resistant MFA (STD-IAM-008) and fully recorded; recordings are retained for 24 months.
3. Vendor-supplied remote access appliances, modems or cellular routers inside OT zones are prohibited.

## 11. Management and Monitoring

1. FortiGate logs MUST be sent to FortiAnalyzer and forwarded to Microsoft Sentinel per STD-OBS-010.
2. Management interfaces MUST reside in a dedicated management segment reachable only from privileged access workstations.

## 12. Compliance & Exceptions

1. Network designs for new sites and any change to OT conduits require ARB Tier 1 review with the Lead Network & OT Architect as reviewer, under GOV-01.
2. Deviations follow the GOV-01 exception process and are recorded in GOV-02 (maximum 12 months, renewable once). EXC-2024-007 (MPLS at Halifax) was closed in March 2025 after SD-WAN cutover.
3. Annual OT segmentation assessments per terminal provide evidence for 33 CFR Part 101 Subpart F and NIS2 audits.

## 13. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2023-11-20 | Tomasz Nowak | First issue after ADR-0036; SD-WAN pilot rules |
| 1.3 | 2024-10-01 | Tomasz Nowak | Nordhaven sites added; IEC 62443 zone model introduced |
| 2.0 | 2025-08-01 | Tomasz Nowak | MPLS retired; BGP underlay/overlay rules, 5G backup, SL-T targets, Coast Guard rule alignment (ARB-2025-049) |
