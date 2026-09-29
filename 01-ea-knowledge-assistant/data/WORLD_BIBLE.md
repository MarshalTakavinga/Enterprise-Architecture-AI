# Harbourline Logistics Group — Architecture Repository World Bible

> Internal authoring reference used to keep every synthetic corpus document consistent.
> **Harbourline Logistics Group is fictional.** Real vendor products are named only because real
> enterprises use them; nothing here describes a real company. It is NOT part of the indexed corpus.

"Today" in the corpus world is **September 2026**. Documents are dated 2023-2026.

## 1. The company

- **Name:** Harbourline Logistics Group ("Harbourline", "HLG"). HQ: Baltimore, Maryland, USA.
- **Business:** global freight forwarding, port & terminal operations, contract logistics, customs brokerage.
- **Size:** ~9,400 employees, ~USD 4.2B revenue, ~60 sites (offices, warehouses, terminals) in 11 countries.
- **Regions & legal entities:** North America (Harbourline Inc. — US; Harbourline Canada Ltd. — Halifax),
  Europe (Harbourline Europe B.V. — Rotterdam; Nordhaven Freight GmbH — Hamburg, acquired **March 2024**),
  Middle East (Harbourline Gulf FZE — Jebel Ali, Dubai).
- **Container terminals operated (4):** Baltimore (Seagirt-adjacent, "BAL-T1"), Halifax ("HFX-T1"),
  Rotterdam Maasvlakte ("RTM-T2"), Jebel Ali ("JEA-T4").
- **Business units:** Ocean & Air Forwarding; Port & Terminal Services; Contract Logistics & Warehousing;
  Customs Brokerage; Harbourline Digital (customer-facing digital products).
- **Strategy programme:** **Horizon 2028** (approved by the Board Nov 2024; USD 118M over 4 years). Goals:
  1. Consolidate three transport management systems into one cloud-native **Harbourline Shipment Platform (HSP)** by Q4 2027.
  2. Real-time shipment & container visibility for customers (target: 95% of shipments with milestone events < 5 minutes latency).
  3. Exit the Baltimore on-prem data centre by **30 June 2027**.
  4. Comply with EU NIS2 (Harbourline Europe is an "essential entity" as port operator), GDPR, Canada PIPEDA, UAE PDPL,
     US Coast Guard maritime cybersecurity rule (33 CFR Part 101 Subpart F, effective July 2025), US CBP ACE and EU ICS2 customs filing.
  5. Reduce IT run cost by 18% by FY2028 (baseline FY2024 IT run cost USD 96M).

## 2. People (use these names/roles consistently)

| Name | Role |
|---|---|
| Elena Marsh | Chief Information Officer (CIO) — executive sponsor of Horizon 2028 |
| David Okafor | Chief Architect; **Chair of the Architecture Review Board (ARB)** |
| Amara Osei | Lead Integration Architect (owns integration, API, event standards) |
| Priya Raman | Principal Security Architect (ARB member) |
| Lena Vogel | Lead Data Architect, based in Rotterdam (owns data standards) |
| Kenji Watanabe | Principal Cloud Architect (owns landing zone, container, resilience standards) |
| Tomasz Nowak | Lead Network & OT Architect (owns network/SD-WAN, terminal edge) |
| Hannah Brennan | Chief Information Security Officer (CISO) |
| Marieke de Vries | Group Data Protection Officer (DPO), Rotterdam |
| Samuel Adeyemi | Head of Enterprise Architecture Office / ARB Secretary (repository steward) |
| Grace Liu | Programme Director, Horizon 2028 / HSP |
| Omar Haddad | Head of IT, Harbourline Gulf (Jebel Ali) |
| Julia Brandt | Solution Architect, Customer Notification Service (Harbourline Digital) |
| Michael Torres | VP Port & Terminal Services (business stakeholder) |
| Rachel Kim | CFO (business stakeholder) |

## 3. Governance model

- **Architecture Review Board (ARB):** meets **every Thursday**; chaired by David Okafor; quorum = Chair + 3 voting members,
  one of whom must be the security architect or delegate. Voting members: Chief Architect, Lead Integration, Security, Data, Cloud, Network/OT architects.
- **Review tiers:** Tier 1 (full ARB review) — new systems, any Restricted data, cross-border data transfer, new technology not on the radar,
  or cost > USD 500k. Tier 2 (delegated review by two domain architects, reported to ARB) — changes to existing systems with no standards deviation.
  Tier 3 (self-certification checklist) — minor changes.
- **Decisions:** Approved, Approved with Conditions, Changes Requested, Rejected. Decisions recorded in the ARB log with ID format `ARB-YYYY-NNN`.
- **Exceptions / dispensations:** ID format `EXC-YYYY-NNN`; max duration 12 months, renewable once; must have a remediation plan; recorded in the Exceptions Register.
- **Change requests:** `CR-YYYY-NNN`.
- **Document IDs:** principles `AP-01..AP-16`; standards `STD-XXX-NNN`; ADRs `ADR-NNNN`; reference architectures `RA-0N`.
- **Technology radar statuses:** Adopt, Trial, Contain (no new use, existing may continue), Retire (removal date set).

## 4. Architecture principles (catalog doc: AP-01..AP-16)

| ID | Name | Domain |
|---|---|---|
| AP-01 | Customer Visibility by Default | Business |
| AP-02 | Compliance by Design | Business |
| AP-03 | Reuse, then Buy, then Build | Business |
| AP-04 | Business Continuity at the Quay (terminal ops must survive loss of WAN/cloud for 72 hours) | Business |
| AP-05 | Data Is an Asset with a Named Owner | Data |
| AP-06 | Data Residency Follows Jurisdiction | Data |
| AP-07 | One System of Record per Data Domain | Data |
| AP-08 | Event-First Integration Between Domains | Application |
| AP-09 | API-First for Synchronous Access | Application |
| AP-10 | Cloud-Smart and Portable (Azure primary, AWS secondary, avoid unnecessary lock-in) | Technology |
| AP-11 | Managed Services over Self-Managed Infrastructure | Technology |
| AP-12 | Zero Trust Access | Security |
| AP-13 | Separate IT and OT | Security |
| AP-14 | Observable by Default | Technology |
| AP-15 | Everything as Code | Technology |
| AP-16 | Accountable Use of AI (a named human is accountable for every AI-assisted decision) | Governance |

Each principle: Name, Statement, Rationale, Implications (TOGAF style), plus "Related standards".

## 5. Standards (15) — owners, versions, key rules

| ID | Title | Owner | Version / effective |
|---|---|---|---|
| STD-INT-001 | Integration Patterns Standard | Amara Osei | v2.1, 2025-03-01 |
| STD-API-002 | API Design & Management Standard | Amara Osei | v1.4, 2025-01-15 |
| STD-EVT-003 | Event Streaming Standard | Amara Osei | v1.2, 2025-05-01 |
| STD-DAT-004 | Data Classification & Handling Standard | Lena Vogel | v3.0, 2024-09-01 |
| STD-DAT-005 | Data Residency & Cross-Border Transfer Standard | Lena Vogel (with DPO) | v2.0, 2025-02-01 |
| STD-DB-006 | Database Technology Selection Standard | Lena Vogel | v1.3, 2025-06-01 |
| STD-CLD-007 | Cloud Landing Zone & Hosting Standard | Kenji Watanabe | v2.2, 2025-04-01 |
| STD-IAM-008 | Identity & Access Management Standard | Priya Raman | v2.0, 2024-11-01 |
| STD-SEC-009 | Encryption & Key Management Standard | Priya Raman | v1.5, 2025-01-01 |
| STD-OBS-010 | Observability & Logging Standard | Kenji Watanabe | v1.1, 2025-07-01 |
| STD-NET-011 | Network Security, SD-WAN & OT Segmentation Standard | Tomasz Nowak | v2.0, 2025-08-01 |
| STD-CTR-012 | Container Platform Standard | Kenji Watanabe | v1.2, 2025-03-15 |
| STD-AI-013 | AI & Generative AI Usage Standard | Priya Raman & Lena Vogel | v1.0, 2025-10-01 |
| STD-TLC-014 | Technology Lifecycle & Radar Standard | David Okafor | v3.1, 2026-01-15 |
| STD-RES-015 | Resilience & Disaster Recovery Standard | Kenji Watanabe | v1.3, 2025-05-15 |

Key facts that MUST be consistent:

**STD-INT-001 Integration Patterns.** Approved patterns:
- **INT-P1 Domain Event Publication** — a domain publishes business events (facts) to the Event Backbone; mandatory for cross-domain asynchronous integration. Transactional outbox required when the event must be consistent with a DB write.
- **INT-P2 Event-Carried State Transfer** — events carry the full state needed by consumers so consumers maintain a local read model; used for high-read consumers such as the customer portal.
- **INT-P3 Synchronous Request/Response via API Gateway** — for queries/commands needing an immediate answer; all through Azure API Management.
- **INT-P4 Managed File Transfer / EDI** — for external partners (carriers, customs brokers) using EDIFACT/X12 via the B2B gateway (IBM Sterling B2B Integrator, status Contain → target partner APIs).
- **INT-P5 Batch Data Ingestion** — into Tidewater data platform only; not for operational integration.
- **Prohibited:** new point-to-point database links across domains; shared databases across domains; new MuleSoft flows after **2025-06-30**; synchronous call chains deeper than 3 hops.

**STD-API-002.** REST + OpenAPI 3.1 contracts; URI major versioning `/v1/`; deprecation notice ≥ 6 months; all APIs published through Azure API Management ("Harbourline API Gateway"); OAuth 2.0 client credentials / auth code + PKCE via Entra ID; rate limits default 1,000 req/min per client; GraphQL = Trial (portal BFF only); SOAP = Contain.

**STD-EVT-003.** Confluent Cloud (Kafka) on Azure is the "Harbourline Event Backbone". Topic naming `<domain>.<entity>.<event>.v<major>` e.g. `shipment.milestone.recorded.v1`. Schemas in Confluent Schema Registry, Avro preferred, BACKWARD compatibility mode. Default retention 7 days; compacted topics for state. Consumers must be idempotent; DLQ topic `<topic>.dlq`. No Restricted data in event payloads unless field-level encrypted. Max message size 1 MB; larger payloads use claim-check pattern with Blob Storage.

**STD-DAT-004.** Four classifications: Public, Internal, Confidential, **Restricted**. Restricted = personal data of EU/UK/Canada/UAE data subjects in bulk, payment card data, customs declarations with personal data, security-sensitive OT/terminal configuration, crew passport data. Restricted requires encryption with customer-managed keys, access via PIM, no use in non-prod unless masked.

**STD-DAT-005.** Personal data of EU data subjects stored and processed in Azure **West Europe** (primary) / **North Europe** (DR) only; Canadian customer data in **Canada Central/Canada East** where contractually required; UAE personal data for Harbourline Gulf in **UAE North**; US in **East US 2** / Central US DR. Cross-border transfer requires a Transfer Impact Assessment (TIA) approved by the DPO and SCCs where applicable. Aggregated/anonymised data may be centralised in Tidewater (East US 2). Pseudonymised data is still personal data.

**STD-DB-006 (answers "can I use NoSQL?").** Default relational: **Azure Database for PostgreSQL Flexible Server** (Adopt). Azure SQL Database = Adopt (for vendor packages needing SQL Server). **Azure Cosmos DB (NoSQL API) = Adopt for specific workloads only**: high-volume telemetry/time-series with key-based access, globally distributed low-latency reads, schema-flexible documents with a single-partition access pattern. Requires a documented access-pattern and partition-key design reviewed by the data architect (Tier 2 review). MongoDB Atlas = Trial (Nordhaven only). Self-managed MongoDB/Cassandra on VMs = **Prohibited**. Oracle Database = **Contain** (Oracle 12c = Retire by 2027-03-31). Redis (Azure Cache for Redis) = Adopt as cache only, never system of record. pgvector extension = Trial (approved for AI retrieval use cases).

**STD-CLD-007.** Azure = primary cloud; AWS = secondary, permitted for (a) Nordhaven legacy workloads in eu-central-1 under EXC-2025-003, (b) DR-only workloads approved by ARB, (c) services with no Azure equivalent approved by ARB. Approved Azure regions: East US 2, Central US, Canada Central, Canada East, West Europe, North Europe, UAE North. Landing zone = Azure Landing Zones (CAF) with management groups `hlg-platform`, `hlg-corp`, `hlg-online`, `hlg-sandbox`. Mandatory tags: `owner`, `cost-centre`, `app-id`, `data-classification`, `environment`. Terraform for all IaC. No public IPs on VMs; ingress via Azure Front Door + WAF or Application Gateway.

**STD-IAM-008.** Microsoft Entra ID is the single workforce IdP; customer identity via Entra External ID ("Harbourline Connect ID"). MFA mandatory for all users; phishing-resistant MFA (FIDO2) for admins. Privileged access via Entra PIM, just-in-time, max 8 hours. Workloads use managed identities; no secrets in code; no shared accounts. Access recertification quarterly for Restricted systems.

**STD-SEC-009.** TLS 1.2 minimum, TLS 1.3 preferred; AES-256 at rest; keys in Azure Key Vault (Premium/HSM for Restricted); customer-managed keys mandatory for Restricted data; key rotation 12 months; certificate lifetime ≤ 397 days, automated renewal.

**STD-OBS-010.** OpenTelemetry SDKs mandatory for new services; W3C trace context propagation; central platform = Azure Monitor / Log Analytics + Grafana; logs retained 13 months (security logs 24 months in Sentinel); **no personal data or secrets in logs**; every service exposes health endpoints; SLOs defined for Tier 0/1 services.

**STD-NET-011.** Fortinet Secure SD-WAN (FortiGate) at all sites (replaced MPLS, ADR-0036). Terminal OT networks follow IEC 62443 zones & conduits with Purdue model levels 0-3; **no direct internet access from OT zones (levels 0-2)**; IT/OT DMZ (level 3.5) mandatory; remote vendor access to OT only via the OT jump host with session recording and time-bound approval. Internet breakout at site via FortiGate with SSL inspection except for health/banking categories.

**STD-CTR-012.** Azure Kubernetes Service (AKS) is the standard container platform; images only from Azure Container Registry `hlgacr`; image signing (Notation) and vulnerability scanning mandatory, no critical CVEs in production; containers run as non-root; Helm + GitOps (Flux). Self-managed Kubernetes prohibited. Azure Container Apps = Adopt for simple event-driven services.

**STD-AI-013.** Approved LLM platform: **Azure OpenAI Service** deployed in approved regions (data stays in-region); AWS Bedrock = Trial for Nordhaven only. Public consumer AI tools must not receive Internal/Confidential/Restricted data. Every AI use case registered in the AI Use Case Register (ID `AIU-NNN`) with a risk tier; high-impact decisions (customs, safety, HR) require human review before action; RAG answers must cite sources; prompts/responses logged 90 days; EU AI Act assessment for EU-facing use cases.

**STD-TLC-014 radar (selected entries):** Adopt: PostgreSQL Flexible Server, AKS, Confluent Cloud, Azure API Management, Terraform, OpenTelemetry, .NET 8, Java 21, Python 3.11+, React 18. Trial: GraphQL (BFF), pgvector, AWS Bedrock (Nordhaven), Microsoft Fabric. Contain: Oracle Database, MuleSoft Anypoint (sunset **2026-12-31**), IBM Sterling B2B, SOAP, .NET Framework 4.8, Java 11. Retire: Oracle 12c (2027-03-31), Windows Server 2012 R2 (overdue — under EXC-2026-002), Java 8 (2026-06-30), MPLS circuits (done 2025), CentOS 7 (2025-12-31).

**STD-RES-015.** Service tiers: **Tier 0** (terminal operations — Navis N4, gate, crane control interfaces): RTO 15 min, RPO 0-5 min, must operate at the edge with 72-hour autonomy (AP-04). **Tier 1** (HSP, customs filing, customer portal): RTO 1 h, RPO 15 min, multi-zone + paired-region DR. **Tier 2** (CRM, WMS, finance): RTO 8 h, RPO 1 h. **Tier 3** (internal tools): RTO 72 h, RPO 24 h. DR tests annually for Tier 1, semi-annually for Tier 0.

## 6. Application landscape (IDs used in docs)

| App ID | Name | Notes |
|---|---|---|
| APP-010 | SAP S/4HANA Finance | RISE with SAP on Azure East US 2; system of record for finance |
| APP-020 | FreightMaster TMS | Legacy in-house TMS, Oracle 12c + Java 8, Baltimore DC; **Retire by Q3 2027** |
| APP-021 | Nordhaven TMS | Acquired; AWS eu-central-1; MongoDB Atlas + Java 11; to be migrated into HSP by Q2 2027 |
| APP-022 | Harbourline Shipment Platform (HSP) | Target TMS; cloud-native microservices on AKS; PostgreSQL; system of record for shipments; first release Nov 2025 (US lanes) |
| APP-030 | Navis N4 Terminal Operating System | One instance per terminal, on-prem edge servers; Tier 0 |
| APP-031 | Terminal Gate Automation (OCR gates) | Per terminal, OT zone |
| APP-040 | Salesforce Sales & Service Cloud | CRM, system of record for customer accounts |
| APP-050 | Harbourline Connect | Customer portal (web + mobile); React + .NET 8 BFF on AKS; served per region |
| APP-055 | Customer Notification Service (CNS) | New in 2026: email/SMS/push shipment alerts; solution architect Julia Brandt; under ARB review (see compliance assessment) |
| APP-060 | Customs Filing Gateway | Files to US CBP ACE, EU ICS2, Canada CBSA CARM; Tier 1 |
| APP-070 | Manhattan Active WM | Warehouse management (SaaS) |
| APP-080 | Tidewater Data Platform | Azure Databricks lakehouse on ADLS Gen2, Unity Catalog; East US 2 (+ West Europe workspace for EU personal data) |
| APP-090 | Container Tracking Service (CTS) | Reefer & smart-container IoT telemetry; Azure IoT Hub + Cosmos DB; ~40M telemetry events/day |
| APP-100 | Microsoft Entra ID | Workforce identity |
| APP-110 | ServiceNow | ITSM + CMDB (system of record for configuration items) |
| APP-120 | Harbourline Event Backbone | Confluent Cloud Kafka on Azure |
| APP-121 | Harbourline API Gateway | Azure API Management (Premium, multi-region) |
| APP-122 | MuleSoft Anypoint ESB | Legacy; Contain; sunset 2026-12-31; ~140 flows remaining (from 310 in 2024) |
| APP-123 | IBM Sterling B2B Integrator | EDI with carriers/customs brokers; Contain |
| APP-130 | DocIntel — Bill of Lading Extraction | Azure AI Document Intelligence + Azure OpenAI; AIU-004; human validation |

## 7. ADRs (12) — IDs, titles, decisions

| ID | Title | Status / date | Decision in one line |
|---|---|---|---|
| ADR-0007 | Adopt Confluent Cloud as the Enterprise Event Backbone | Accepted, 2024-02-20 | Confluent Cloud on Azure chosen over Azure Event Hubs (Kafka API) and extending MuleSoft; drivers: schema registry, ecosystem, multi-cloud portability for Nordhaven on AWS |
| ADR-0012 | Use Azure Cosmos DB for Container Telemetry Storage | Accepted, 2024-05-14 | Cosmos DB NoSQL API, partition key `/containerId`, TTL 90 days hot, archived to ADLS; chosen over PostgreSQL (write volume) and Azure Data Explorer (considered; ADX kept for analytics) |
| ADR-0015 | Sunset MuleSoft ESB and Freeze New Flows | Accepted, 2024-09-10 | No new flows after 2025-06-30; decommission by 2026-12-31; replacement by INT-P1/INT-P3 |
| ADR-0019 | Azure API Management as the Single API Gateway | Accepted, 2024-06-04 | APIM Premium multi-region over Kong Enterprise and AWS API Gateway |
| ADR-0021 | Temporarily Retain Nordhaven TMS on AWS | Accepted, 2024-07-02 | Keep in eu-central-1 until HSP migration; linked exception EXC-2025-003; connectivity via Confluent cluster linking + private link |
| ADR-0024 | PostgreSQL Flexible Server as Default Relational Database | Accepted, 2024-11-19 | Over Azure SQL and Oracle; open-source, portable, cost |
| ADR-0027 | Edge-Hosted Terminal Operating System with Local Failover | Accepted, 2024-04-09 | Navis N4 stays on-prem at each terminal on a 2-node edge cluster; cloud only for replication/analytics; satisfies AP-04 |
| ADR-0030 | Event-Carried State Transfer for Shipment Status to Harbourline Connect | Accepted, 2025-04-22 | Portal keeps a local read model fed by `shipment.milestone.recorded.v1` & `shipment.status.changed.v1`; applies INT-P2 |
| ADR-0033 | Azure OpenAI for Bill of Lading Extraction with Human Validation | Accepted, 2025-11-04 | In-region Azure OpenAI + Document Intelligence; human validator must confirm customs-relevant fields; AIU-004 |
| ADR-0036 | Replace MPLS WAN with Fortinet Secure SD-WAN | Accepted (implemented 2025), 2023-10-17 | FortiGate SD-WAN at ~60 sites; dual ISP + LTE/5G backup at terminals |
| ADR-0038 | Transactional Outbox for Publishing Domain Events from HSP | Accepted, 2025-06-10 | HSP services write events to an outbox table in PostgreSQL; Debezium CDC connector (Confluent managed) publishes to Kafka; applies INT-P1 |
| ADR-0041 | Serve EU Customer Data for Harbourline Connect from West Europe | Accepted, 2025-09-02 | Regional deployment stamps (US, EU, CA); EU stamp in West Europe; global routing via Front Door by account home region; satisfies AP-06 / STD-DAT-005 |

ADR format: Title, Status, Date, Deciders, Context, Decision Drivers, Considered Options, Decision Outcome, Consequences (positive/negative), Compliance with principles/standards, Links.

## 8. Reference architectures (4)

- **RA-01 Event-Driven Domain Integration** — Owner Amara Osei. Building blocks: domain service → outbox → CDC → Event Backbone → consumers (read models), schema registry, DLQ, API Gateway for queries. Worked example: shipment milestones to portal & CNS.
- **RA-02 Cloud-Native Application on the Azure Landing Zone** — Owner Kenji Watanabe. Front Door + WAF → AKS (private) → PostgreSQL Flex (private endpoint), Key Vault, managed identity, OTel, zone-redundant; regional stamp model.
- **RA-03 Terminal Edge & OT Connectivity** — Owner Tomasz Nowak. Purdue levels, IEC 62443 zones, edge cluster for Navis N4, IT/OT DMZ, one-way data replication to cloud via DMZ broker, OT jump host, FortiGate pairs, dual ISP + 5G.
- **RA-04 Tidewater Enterprise Data Platform** — Owner Lena Vogel. Medallion (bronze/silver/gold) in Databricks + Unity Catalog; ingestion via Kafka connectors & batch; EU personal data in West Europe workspace; data products per domain with named owners.

## 9. TOGAF-style deliverables (original content, TOGAF structure) — all about Horizon 2028 / HSP unless stated

- **GOV-01 Architecture Governance Framework & ARB Charter** (Preliminary) — tailored ADM, org model for EA, ARB tiers, exception process, repository structure.
- **PRE-01 Business Principles, Goals and Drivers** (Preliminary).
- **PRE-02 Request for Architecture Work — Shipment Platform Consolidation** (Preliminary → A), sponsor Elena Marsh, dated 2024-10-07.
- **A-01 Architecture Vision — Horizon 2028 Shipment Platform** (Phase A), incl. value propositions, KPIs, baseline/target summary, risks.
- **A-02 Statement of Architecture Work — Shipment Platform Consolidation** (Phase A), scope, roles, plan, acceptance criteria, signed 2024-12-02.
- **A-03 Stakeholder Map & Communications Plan** (Phase A).
- **A-04 Business Capability Assessment** (Phase A/B) — capability map with maturity 1-5 (e.g., Shipment Booking 2→4, Shipment Visibility 2→5, Customs Declaration 3→4, Terminal Operations 4→4, Carrier Management 2→4, Billing & Invoicing 3→4).
- **ADD-01 Architecture Definition Document — Shipment Platform** (Phases B-D): baseline (3 TMS, MuleSoft, Oracle), target (HSP), gap analysis table, building blocks.
- **ARS-01 Architecture Requirements Specification — Shipment Platform** (requirements, IDs `REQ-HSP-NNN`, incl. NFRs e.g., REQ-HSP-014 milestone latency < 5 min p95; REQ-HSP-021 EU personal data in West Europe).
- **F-01 Architecture Roadmap & Migration Plan — Horizon 2028**: Transition Architecture 1 (Nov 2025, US lanes live on HSP), TA2 (Q2 2027, Nordhaven migrated, EU lanes), TA3/target (Q4 2027, FreightMaster retired, Baltimore DC exit June 2027). Work packages WP-01..WP-10.
- **G-01 Architecture Contract — HSP Delivery Programme** between EA Office and HSP delivery (vendor partner: "Kestrel Digital Partners", fictional SI).
- **G-02 Compliance Assessment — Customer Notification Service (APP-055)**, ARB-2026-031, dated 2026-08-20: findings — (1) proposes direct REST polling of HSP every 30s instead of subscribing to events → non-compliant with STD-INT-001 INT-P1/AP-08; (2) uses Twilio SMS with EU phone numbers processed in US → needs TIA under STD-DAT-005 (needs human review); (3) plans to use MuleSoft for email templating → non-compliant (ADR-0015); (4) observability compliant. Decision: **Changes Requested**.
- **H-01 Change Request CR-2026-014 — Add UAE deployment stamp for Harbourline Connect** (driver: UAE PDPL + Jebel Ali customers), raised 2026-06-11 by Omar Haddad.
- **H-02 Requirements Impact Assessment — CR-2026-014**.
- **GOV-02 Architecture Exceptions Register** — active: EXC-2025-003 (Nordhaven TMS on AWS eu-central-1, expires 2026-12-31, renewed once), EXC-2026-001 (FreightMaster Oracle 12c extended support to 2027-03-31), EXC-2026-002 (Windows Server 2012 R2 on 14 terminal gate servers, ESU, expires 2026-11-30, remediation by Tomasz Nowak), EXC-2026-004 (CNS may use Twilio US region pending TIA — **status: Requested, not approved**). Closed: EXC-2024-007 (MPLS at Halifax until SD-WAN cutover — closed 2025-03).
- **GOV-03 Glossary** of EA and Harbourline terms.

## 10. Writing rules for all corpus docs

1. Markdown file, starting with YAML front matter:
```
---
doc_id: STD-INT-001
title: Integration Patterns Standard
doc_type: standard        # one of: principle_catalog, standard, adr, reference_architecture, togaf_deliverable, governance
togaf_phase: Preliminary  # optional: Preliminary, A, B, C, D, E, F, G, H, Requirements
version: "2.1"
status: Approved          # Approved | Accepted | Draft | Superseded | Active
owner: Amara Osei, Lead Integration Architect
approved_by: Architecture Review Board (ARB-2025-012)
effective_date: 2025-03-01
next_review: 2026-03-01
classification: Internal
related: [AP-08, AP-09, STD-EVT-003, ADR-0007, ADR-0038, RA-01]
---
```
2. Immediately after front matter: `# <doc_id> — <title>` then a one-line blockquote: `> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.`
3. Use **numbered headings** (`## 1. Purpose`, `## 4. Approved Patterns`, `### 4.1 INT-P1 — Domain Event Publication`) so clauses can be cited as `STD-INT-001 §4.1`.
4. Write like a real enterprise document: specific, normative ("MUST", "MUST NOT", "SHOULD" per RFC 2119 in standards), concrete numbers, named owners, dates. No filler, no marketing tone. Use tables where a real doc would.
5. Cross-reference other docs by ID only as listed in this bible. Do not invent new standards/ADR IDs beyond this bible (you may reference ARB decision IDs `ARB-YYYY-NNN`, requirement IDs `REQ-HSP-NNN`, work packages `WP-NN`, AI use case IDs `AIU-NNN`).
6. Length: standards 900-1,600 words; ADRs 600-1,000; principles catalog ~3,000; TOGAF deliverables 1,000-2,000; RAs 900-1,400.
7. Every standard includes: Purpose, Scope, Normative references/related principles, the rules (numbered), Compliance & exceptions (pointing to GOV-01 exception process), Document history table.
8. Never copy text from The Open Group's TOGAF publications or templates. Write original prose; TOGAF deliverable *names* and generic structure (e.g., Name/Statement/Rationale/Implications) are fine.
9. Do NOT cover these topics anywhere (they are reserved as deliberate out-of-corpus test questions): mainframe/COBOL, blockchain, quantum, travel & expense policy, mobile device management (MDM/Intune) policy, SAP upgrade roadmap details, office Wi-Fi guest network, specific salary/HR policies, and vessel bunker fuel procurement.
