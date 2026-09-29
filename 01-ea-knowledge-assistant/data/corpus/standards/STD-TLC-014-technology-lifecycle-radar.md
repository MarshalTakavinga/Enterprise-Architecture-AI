---
doc_id: STD-TLC-014
title: Technology Lifecycle & Radar Standard
doc_type: standard
version: "3.1"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Architecture Review Board (ARB-2026-003)
effective_date: 2026-01-15
next_review: 2027-01-15
classification: Internal
related: [AP-03, AP-10, AP-11, STD-INT-001, STD-API-002, STD-DB-006, STD-CLD-007, STD-CTR-012, STD-AI-013, STD-NET-011, ADR-0015, ADR-0024, ADR-0036, GOV-01, GOV-02]
---

# STD-TLC-014 — Technology Lifecycle & Radar Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard governs how technologies enter, are used within, and leave the Harbourline estate. It defines the four statuses of the Harbourline Technology Radar, the obligations attached to each status, and the process for changing status. The radar is the single reference solution architects use to answer "may I use this technology?" and it is the basis for Tier 1 review triggers in GOV-01.

## 2. Scope

- Programming languages and runtimes, frameworks, databases, integration and messaging products, cloud services, infrastructure platforms, operating systems, network technologies and AI platforms used to build or run Harbourline systems.
- Commercial off-the-shelf and SaaS products are in scope when they introduce a new platform capability; business applications themselves are managed through the application portfolio.
- All Harbourline entities, including Nordhaven Freight GmbH and Harbourline Gulf FZE.

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-03 Reuse, then Buy, then Build | Prefer existing Adopt technologies before introducing new ones |
| AP-10 Cloud-Smart and Portable | Radar favours portable, standards-based technologies |
| AP-11 Managed Services over Self-Managed Infrastructure | Managed services preferred at Adopt |
| Domain standards (STD-DB-006, STD-CTR-012, STD-AI-013, etc.) | Domain-specific selection rules that the radar summarises |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Radar Statuses

| Status | Meaning | New use | Existing use |
|---|---|---|---|
| Adopt | Proven, supported, default choice | Permitted without further approval | Permitted |
| Trial | Approved for bounded use to gain evidence | Only within the scope stated on the radar | Permitted within scope |
| Contain | No longer strategic | MUST NOT be used for new solutions | MAY continue; no scope expansion |
| Retire | Removal date set | MUST NOT be used | MUST be removed by the Retire date |

### 4.1 Rules per status

1. Solutions MUST prefer Adopt technologies. Selecting a Trial technology outside its stated scope, or any technology not on the radar, triggers ARB Tier 1 review.
2. Each Trial entry MUST have a named sponsor, a stated scope, exit criteria and a decision date no more than 12 months after entry. At the decision date the ARB moves the entry to Adopt, Contain or Retire.
3. Contain technologies MAY receive patches, security fixes and minor version upgrades. Adding new integrations, modules, interfaces or users beyond the current population requires an exception.
4. Every Retire entry MUST have a removal date and a named remediation owner; applications using it MUST have a funded decommissioning or migration plan.
5. Continued use of a Retire technology after its removal date is non-compliant and MUST be covered by an approved exception in GOV-02.
6. Items prohibited outright by a domain standard (for example, self-managed MongoDB or Cassandra on VMs under STD-DB-006, or self-managed Kubernetes under STD-CTR-012) are not radar entries; they MUST NOT be used.

## 5. Harbourline Technology Radar (as at 2026-01-15)

| Technology | Category | Status | Date / condition | Reference |
|---|---|---|---|---|
| Azure Database for PostgreSQL Flexible Server | Database | Adopt | Default relational DB | STD-DB-006, ADR-0024 |
| Azure SQL Database | Database | Adopt | Vendor packages needing SQL Server | STD-DB-006 |
| Azure Cosmos DB (NoSQL API) | Database | Adopt | Specific workloads only, Tier 2 data-architect review | STD-DB-006, ADR-0012 |
| Azure Cache for Redis | Database | Adopt | Cache only, never system of record | STD-DB-006 |
| Azure Kubernetes Service (AKS) | Platform | Adopt | Standard container platform | STD-CTR-012 |
| Azure Container Apps | Platform | Adopt | Simple event-driven services | STD-CTR-012 |
| Confluent Cloud (Kafka) | Integration | Adopt | Harbourline Event Backbone | STD-EVT-003, ADR-0007 |
| Azure API Management | Integration | Adopt | Single API gateway | STD-API-002, ADR-0019 |
| Terraform | Infrastructure as code | Adopt | All IaC | STD-CLD-007 |
| Helm + Flux (GitOps) | Deployment | Adopt | Kubernetes delivery | STD-CTR-012 |
| OpenTelemetry | Observability | Adopt | Mandatory for new services | STD-OBS-010 |
| Azure Monitor + Azure Managed Grafana | Observability | Adopt | Central platform | STD-OBS-010 |
| Azure OpenAI Service | AI | Adopt | Approved regions only | STD-AI-013 |
| Azure Databricks + Unity Catalog | Data platform | Adopt | Tidewater | RA-04 |
| Fortinet Secure SD-WAN (FortiGate) | Network | Adopt | All sites | STD-NET-011, ADR-0036 |
| .NET 8 | Runtime | Adopt | LTS until Nov 2026; .NET 10 evaluation under way | — |
| Java 21 | Runtime | Adopt | LTS | — |
| Python 3.11+ | Runtime | Adopt | 3.11, 3.12 | — |
| React 18 | Front-end | Adopt | Harbourline Connect and internal UIs | — |
| Windows Server 2022 | Operating system | Adopt | Where Windows is required | — |
| Ubuntu 22.04 LTS / 24.04 LTS | Operating system | Adopt | Linux VMs and edge servers | — |
| GraphQL | API | Trial | Portal BFF only; decision by 2026-09-30 | STD-API-002 |
| pgvector (PostgreSQL extension) | Database / AI | Trial | AI retrieval use cases only | STD-DB-006, STD-AI-013 |
| AWS Bedrock | AI | Trial | Nordhaven only | STD-AI-013 |
| Microsoft Fabric | Data platform | Trial | Finance reporting pilot; decision by 2026-12-31 | RA-04 |
| MongoDB Atlas | Database | Trial | Nordhaven only, until HSP migration | STD-DB-006 |
| Oracle Database | Database | Contain | No new use | STD-DB-006 |
| MuleSoft Anypoint | Integration | Contain | No new flows since 2025-06-30; sunset 2026-12-31 | ADR-0015 |
| IBM Sterling B2B Integrator | Integration | Contain | Target: partner APIs | STD-INT-001 |
| SOAP web services | API | Contain | No new SOAP interfaces | STD-API-002 |
| .NET Framework 4.8 | Runtime | Contain | Migrate to .NET 8 on next major change | — |
| Java 11 | Runtime | Contain | Nordhaven TMS until migration | — |
| Windows Server 2016 | Operating system | Contain | Plan upgrade before vendor end of support (2027-01) | — |
| React 16/17 | Front-end | Contain | Upgrade on next release | — |
| Oracle Database 12c | Database | Retire | 2027-03-31 (EXC-2026-001) | STD-DB-006 |
| Windows Server 2012 R2 | Operating system | Retire | Overdue; 14 gate servers under EXC-2026-002 until 2026-11-30 | STD-NET-011 |
| Java 8 | Runtime | Retire | 2026-06-30 | — |
| CentOS 7 | Operating system | Retire | 2025-12-31 | — |
| Node.js 18 | Runtime | Retire | 2025-06-30 | — |
| Python 3.9 and earlier | Runtime | Retire | 2025-12-31 | — |
| MPLS WAN circuits | Network | Retire | Completed 2025 | ADR-0036 |

## 6. Lifecycle Process

### 6.1 Proposing a change

1. Any architect MAY propose a new entry or a status change by submitting a radar proposal to the EA Office (Samuel Adeyemi) with: problem statement, alternatives considered against existing Adopt entries, cost, skills impact, security assessment and exit strategy.
2. Proposals for new technology are heard at the ARB (Thursday session) as Tier 1 items.

### 6.2 Review cadence

1. The ARB MUST review the full radar quarterly and publish the updated radar within 10 working days.
2. Vendor end-of-support announcements MUST be assessed within 30 days. A technology whose vendor support ends within 18 months MUST be moved to Contain; within 12 months, to Retire with a removal date no later than the end-of-support date.

### 6.3 Inventory

1. Technology use MUST be recorded against configuration items in ServiceNow (APP-110) so that the population of each Contain and Retire technology can be reported.
2. Application owners MUST confirm their technology inventory annually.

## 7. Compliance & Exceptions

1. Radar conformance is checked at every ARB review tier under GOV-01; Tier 3 self-certification includes a radar declaration.
2. Use of a Contain technology beyond its current scope, a Trial technology outside scope, or a Retire technology after its date MUST be covered by an exception raised through GOV-01 and recorded in GOV-02, with a remediation plan and a maximum duration of 12 months, renewable once.
3. The EA Office reports Retire-date breaches to the CIO, Elena Marsh, monthly.

## 8. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2023-04-03 | David Okafor | First radar with four statuses |
| 2.0 | 2024-06-17 | David Okafor | Nordhaven technologies added after acquisition; Trial entry rules |
| 3.0 | 2025-07-10 | David Okafor | MuleSoft to Contain with sunset date; Container Apps to Adopt; end-of-support triggers |
| 3.1 | 2026-01-15 | David Okafor | Q4 2025 radar review: MPLS retirement completed, CentOS 7 and Java 8 retire dates confirmed, Microsoft Fabric added to Trial (ARB-2026-003) |
