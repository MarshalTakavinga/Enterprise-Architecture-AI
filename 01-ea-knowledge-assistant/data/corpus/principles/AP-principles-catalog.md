---
doc_id: AP-CATALOG
title: Enterprise Architecture Principles Catalog
doc_type: principle_catalog
togaf_phase: Preliminary
version: "4.0"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Architecture Review Board (ARB-2026-006)
effective_date: 2026-02-12
next_review: 2027-02-12
classification: Internal
related: [GOV-01, PRE-01, STD-TLC-014, STD-INT-001, STD-DAT-004, STD-DAT-005, STD-CLD-007, STD-AI-013, STD-RES-015]
---

# AP-CATALOG — Enterprise Architecture Principles Catalog

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This catalog defines the sixteen architecture principles (AP-01 to AP-16) that govern how Harbourline Logistics Group designs, buys, builds, changes and retires business and IT capabilities. The principles translate the Horizon 2028 goals and the business drivers recorded in PRE-01 into durable design rules. They are deliberately few, stable and testable. Detailed, technology-specific rules live in the standards (STD-XXX-NNN); the principles explain *why* those standards exist and provide the basis for judgement where no standard yet applies.

Version 4.0 replaces version 3.2 (2024-11). The main changes are: AP-16 Accountable Use of AI is new; AP-04 now states the 72-hour autonomy requirement explicitly; AP-10 was reworded from "Cloud-First" to "Cloud-Smart and Portable" to reflect the Azure-primary / AWS-secondary position in STD-CLD-007; and every principle now lists its related standards.

## 2. Scope and Applicability

The principles apply to:

- all Harbourline legal entities: Harbourline Inc., Harbourline Canada Ltd., Harbourline Europe B.V., Nordhaven Freight GmbH and Harbourline Gulf FZE;
- all solution designs that enter ARB review at any tier (see GOV-01 §6), including SaaS procurements, vendor-hosted services and work delivered by system integrators such as Kestrel Digital Partners;
- architecture deliverables produced under the tailored ADM, including A-01, ADD-01, ARS-01 and F-01 for the Horizon 2028 programme.

They apply to operational technology at the four container terminals (BAL-T1, HFX-T1, RTM-T2, JEA-T4) where stated, notably AP-04 and AP-13.

## 3. How Principles Are Used in ARB Reviews

### 3.1 In submissions

Every Tier 1 and Tier 2 submission MUST contain a principles conformance table listing each principle as *Conforms*, *Partially conforms* or *Not applicable*, with a one-line justification. A "Not applicable" claim for AP-02, AP-05, AP-12 or AP-14 is rarely accepted and must be explained. Tier 3 self-certification checklists reference the principles implicitly through the checklist questions.

### 3.2 In the review

Reviewers test the submission against the principles first and the standards second. A standards deviation that nonetheless honours the underlying principle is usually a candidate for an exception (EXC-YYYY-NNN); a design that contradicts a principle outright normally results in *Changes Requested* or *Rejected*. For example, in ARB-2026-031 the Customer Notification Service (APP-055) was returned with *Changes Requested* primarily because polling HSP every 30 seconds contradicted AP-08, not merely because it breached STD-INT-001 INT-P1.

### 3.3 In decision records

ADRs record compliance with principles in their "Compliance with principles/standards" section. ARB decision minutes cite principles by ID (e.g., "AP-06 not satisfied — TIA outstanding"), which makes decisions traceable and searchable in the repository.

## 4. Precedence and Conflict Resolution

Principles occasionally pull in different directions — for instance, AP-11 (managed services) against AP-04 (terminal autonomy), or AP-01 (visibility) against AP-06 (residency). The ARB resolves conflicts in this order:

1. **Law and regulation first.** Where a principle expresses a legal obligation (AP-02, AP-06, and the regulatory parts of AP-12 and AP-13), it prevails. No business benefit justifies non-compliance with NIS2, GDPR, PIPEDA, UAE PDPL, 33 CFR Part 101 Subpart F or customs filing rules.
2. **Safety and operational continuity second.** AP-04 and AP-13 prevail over efficiency principles (AP-03, AP-10, AP-11) for Tier 0 terminal services.
3. **Domain-level principles next.** Data principles (AP-05 to AP-07) take precedence over application-level convenience (AP-08, AP-09) where they conflict, because data errors propagate further than integration errors.
4. **Efficiency principles last.** AP-03, AP-10, AP-11 and AP-15 are strong defaults but yield to the above.

Where the order does not settle the matter, the ARB Chair decides and records the rationale in the ARB log. Unresolved conflicts with business impact escalate to the CIO as set out in GOV-01 §9.

## 5. Principle Structure

Each principle has an ID, a name, a domain (Business, Data, Application, Technology, Security, Governance), a Statement, a Rationale, Implications and Related standards. Principle owners are the owners of the most closely related standard unless stated otherwise.

| ID | Name | Domain |
|---|---|---|
| AP-01 | Customer Visibility by Default | Business |
| AP-02 | Compliance by Design | Business |
| AP-03 | Reuse, then Buy, then Build | Business |
| AP-04 | Business Continuity at the Quay | Business |
| AP-05 | Data Is an Asset with a Named Owner | Data |
| AP-06 | Data Residency Follows Jurisdiction | Data |
| AP-07 | One System of Record per Data Domain | Data |
| AP-08 | Event-First Integration Between Domains | Application |
| AP-09 | API-First for Synchronous Access | Application |
| AP-10 | Cloud-Smart and Portable | Technology |
| AP-11 | Managed Services over Self-Managed Infrastructure | Technology |
| AP-12 | Zero Trust Access | Security |
| AP-13 | Separate IT and OT | Security |
| AP-14 | Observable by Default | Technology |
| AP-15 | Everything as Code | Technology |
| AP-16 | Accountable Use of AI | Governance |

## 6. AP-01 — Customer Visibility by Default

### 6.1 Statement
Any capability that changes the state of a customer's shipment, container or customs declaration must make that change visible to the customer, subject to authorisation, without the customer having to ask.

### 6.2 Rationale
Real-time visibility is Horizon 2028 goal 2 and the most frequent reason customers cite for choosing competitors. Visibility built in after the fact is expensive, inconsistent and late.

### 6.3 Implications
- Every shipment-affecting service in HSP (APP-022) publishes milestone events such as `shipment.milestone.recorded.v1` so that Harbourline Connect (APP-050) and CNS (APP-055) can consume them.
- The target of 95% of milestone events reaching customers within 5 minutes (REQ-HSP-014) is a design constraint, not a reporting metric.
- Terminal events from Navis N4 (APP-030) and container telemetry from CTS (APP-090) are designed for onward publication through the IT/OT DMZ from the start.
- Customer-facing visibility respects account-level authorisation enforced through Harbourline Connect ID.

### 6.4 Related standards
STD-INT-001, STD-EVT-003, STD-API-002, STD-IAM-008.

## 7. AP-02 — Compliance by Design

### 7.1 Statement
Regulatory, contractual and customs obligations are identified during design and implemented as architectural requirements, not retrofitted as controls after go-live.

### 7.2 Rationale
Harbourline Europe is an essential entity under NIS2; the US terminals fall under the US Coast Guard maritime cybersecurity rule; customs filing errors to CBP ACE, EU ICS2 and CBSA CARM carry penalties and cargo holds. Retrofitting compliance costs more and leaves gaps.

### 7.3 Implications
- Tier 1 submissions include a regulatory applicability section naming each obligation and the requirement ID that satisfies it.
- Changes to the Customs Filing Gateway (APP-060) always receive Tier 1 review.
- Data classification per STD-DAT-004 is assigned before design begins, and the `data-classification` tag is mandatory on every Azure resource.
- Security logs are retained 24 months in Sentinel to support NIS2 incident reporting and forensic obligations.
- The Group DPO, Marieke de Vries, is consulted on any design processing personal data of EU, UK, Canadian or UAE data subjects.

### 7.4 Related standards
STD-DAT-004, STD-DAT-005, STD-SEC-009, STD-OBS-010, STD-NET-011.

## 8. AP-03 — Reuse, then Buy, then Build

### 8.1 Statement
Before building a capability, teams first reuse an existing enterprise capability, then evaluate a commercial product or SaaS service, and only then build custom software.

### 8.2 Rationale
Harbourline runs three transport management systems today because previous programmes built rather than reused. Horizon 2028 goal 5 (18% run-cost reduction by FY2028) depends on consolidating duplicates.

### 8.3 Implications
- New shipment-related functionality is built as an HSP service rather than as a new standalone application.
- Solution submissions include a short options analysis covering reuse of the Event Backbone (APP-120), API Gateway (APP-121) and Tidewater (APP-080) before proposing new platforms.
- Custom build is justified where the capability differentiates Harbourline (e.g., HSP's multimodal planning), not where a commodity SaaS exists (e.g., warehouse management via Manhattan Active WM, APP-070).
- Bought products must meet integration standards; a package that can only integrate via shared databases fails AP-07 and AP-08 regardless of price.

### 8.4 Related standards
STD-TLC-014, STD-INT-001.

## 9. AP-04 — Business Continuity at the Quay

### 9.1 Statement
Terminal operations must continue safely for at least 72 hours after a complete loss of WAN connectivity or cloud services.

### 9.2 Rationale
A terminal that stops moving containers incurs vessel delay costs within hours and contractual penalties with shipping lines. WAN and cloud outages are outside Harbourline's direct control.

### 9.3 Implications
- Navis N4 (APP-030) runs on a two-node edge cluster at each terminal (ADR-0027); the cloud is used for replication and analytics only.
- Tier 0 services meet RTO 15 minutes and RPO 0-5 minutes and are DR-tested semi-annually (STD-RES-015).
- Gate automation (APP-031) and crane control interfaces must not have a runtime dependency on Entra ID, the Event Backbone or any cloud API; they use locally cached credentials and store-and-forward queues.
- Terminal sites maintain dual ISP plus LTE/5G backup (ADR-0036), but AP-04 is satisfied by local autonomy, not by connectivity redundancy.
- Designs for HSP must tolerate terminal events arriving up to 72 hours late and out of order.

### 9.4 Related standards
STD-RES-015, STD-NET-011.

## 10. AP-05 — Data Is an Asset with a Named Owner

### 10.1 Statement
Every data domain and every data product has a named business owner who is accountable for its quality, classification and access decisions.

### 10.2 Rationale
Unowned data decays: quality issues go unresolved and access requests stall. Named ownership is also a precondition for GDPR accountability.

### 10.3 Implications
- Each data product in Tidewater (APP-080) is registered in Unity Catalog with an owner and steward (RA-04).
- The `owner` tag is mandatory on all Azure resources (STD-CLD-007).
- Event topics on the Event Backbone have an owning domain encoded in the topic name (`<domain>.<entity>.<event>.v<major>`).
- Access to Restricted data is approved by the data owner, not by the platform team.

### 10.4 Related standards
STD-DAT-004, STD-EVT-003, STD-CLD-007.

## 11. AP-06 — Data Residency Follows Jurisdiction

### 11.1 Statement
Personal and regulated data is stored and processed in the jurisdiction required by law or contract, and moves across borders only through an approved transfer mechanism.

### 11.2 Rationale
GDPR, PIPEDA, UAE PDPL and customer contracts impose location and transfer constraints. Breaches carry fines and reputational damage, and Harbourline Europe's NIS2 status raises supervisory scrutiny.

### 11.3 Implications
- EU personal data resides in Azure West Europe with DR in North Europe; Harbourline Connect serves EU customers from its West Europe stamp (ADR-0041).
- UAE personal data for Harbourline Gulf resides in UAE North; CR-2026-014 proposes a UAE stamp for Harbourline Connect for this reason.
- Any cross-border transfer — including to SaaS sub-processors such as SMS providers — requires a Transfer Impact Assessment approved by the DPO before go-live (see EXC-2026-004).
- Pseudonymised data remains personal data; only aggregated or anonymised data may be centralised in the Tidewater East US 2 workspace.

### 11.4 Related standards
STD-DAT-005, STD-DAT-004, STD-CLD-007.

## 12. AP-07 — One System of Record per Data Domain

### 12.1 Statement
Each data domain has exactly one authoritative system of record; all other copies are derived, read-only and traceable to it.

### 12.2 Rationale
Three TMS platforms each claiming to be authoritative for shipments is the root cause of billing disputes and inconsistent customer status.

### 12.3 Implications
- HSP (APP-022) is the system of record for shipments; FreightMaster (APP-020) and Nordhaven TMS (APP-021) become read-only as lanes migrate (F-01).
- Salesforce (APP-040) is the system of record for customer accounts; SAP S/4HANA (APP-010) for financial postings; ServiceNow (APP-110) for configuration items.
- Local read models, such as the Harbourline Connect shipment view (ADR-0030), are permitted but never written back to by consumers.
- Azure Cache for Redis is never a system of record (STD-DB-006).

### 12.4 Related standards
STD-DB-006, STD-INT-001.

## 13. AP-08 — Event-First Integration Between Domains

### 13.1 Statement
Domains integrate asynchronously by publishing and subscribing to business events on the Harbourline Event Backbone; synchronous coupling between domains is the exception.

### 13.2 Rationale
Event-first integration decouples release cycles, supports near-real-time visibility (AP-01) and removes the polling load that degraded FreightMaster.

### 13.3 Implications
- Cross-domain asynchronous integration uses INT-P1 Domain Event Publication; HSP uses a transactional outbox with CDC (ADR-0038).
- Consumers that need a current view of another domain's state build a local read model via INT-P2.
- Polling another domain's API on a timer to detect change is non-conforming.
- New MuleSoft flows are prohibited after 2025-06-30 (ADR-0015); remaining flows migrate before sunset on 2026-12-31.
- New point-to-point database links and shared databases across domains are prohibited.

### 13.4 Related standards
STD-INT-001, STD-EVT-003.

## 14. AP-09 — API-First for Synchronous Access

### 14.1 Statement
Where a consumer genuinely needs an immediate answer, capabilities are exposed as managed, versioned APIs published through the Harbourline API Gateway.

### 14.2 Rationale
Consistent API contracts reduce integration effort, enable partner self-service and let security and rate limiting be enforced in one place (ADR-0019).

### 14.3 Implications
- APIs are REST with OpenAPI 3.1 contracts and `/v1/`-style major versioning.
- All APIs are published through Azure API Management (APP-121); direct calls to service endpoints from other domains are not allowed.
- Breaking changes require a new major version and at least six months' deprecation notice.
- Synchronous call chains deeper than three hops are prohibited.
- Partner integrations currently on EDI via IBM Sterling (APP-123) have a target state of partner APIs.

### 14.4 Related standards
STD-API-002, STD-INT-001, STD-IAM-008.

## 15. AP-10 — Cloud-Smart and Portable

### 15.1 Statement
Workloads are hosted in Azure by default, in AWS only where approved, and on-premises only where AP-04 or AP-13 requires; designs avoid lock-in that brings no proportionate benefit.

### 15.2 Rationale
Exiting the Baltimore data centre by 30 June 2027 (Horizon 2028 goal 3) requires a clear default. Portability protects negotiating position and eases integration of acquisitions such as Nordhaven.

### 15.3 Implications
- New workloads land in the Azure Landing Zone in an approved region (STD-CLD-007).
- AWS is permitted for Nordhaven legacy workloads under EXC-2025-003, DR-only workloads, or services without an Azure equivalent, each approved by the ARB.
- Open, portable technologies are preferred where functionally equivalent: PostgreSQL (ADR-0024), Kafka via Confluent (ADR-0007), Kubernetes, Terraform, OpenTelemetry.
- Proprietary PaaS features are acceptable when they materially reduce operational effort (AP-11); the trade-off is recorded in the ADR.

### 15.4 Related standards
STD-CLD-007, STD-DB-006, STD-CTR-012, STD-TLC-014.

## 16. AP-11 — Managed Services over Self-Managed Infrastructure

### 16.1 Statement
Teams use provider-managed platform services in preference to operating their own infrastructure, middleware or databases.

### 16.2 Rationale
Self-managed platforms consume scarce engineering capacity, increase patch backlogs and inflate run cost. Managed services support goal 5.

### 16.3 Implications
- Self-managed Kubernetes and self-managed MongoDB or Cassandra on VMs are prohibited.
- Databases use PostgreSQL Flexible Server, Azure SQL Database or Cosmos DB per STD-DB-006.
- Kafka is consumed as Confluent Cloud, not operated in-house.
- Terminal edge clusters (ADR-0027) are an accepted exception driven by AP-04.

### 16.4 Related standards
STD-CLD-007, STD-CTR-012, STD-DB-006.

## 17. AP-12 — Zero Trust Access

### 17.1 Statement
No user, device or workload is trusted because of its network location; every access is authenticated, authorised with least privilege and continuously evaluated.

### 17.2 Rationale
The flat, perimeter-based network of the MPLS era does not suit a cloud-first, multi-entity group, and NIS2 and the US Coast Guard rule both require strong access control.

### 17.3 Implications
- Entra ID is the single workforce IdP; MFA is mandatory and administrators use FIDO2 keys.
- Privileged access uses Entra PIM with just-in-time elevation of at most 8 hours.
- Workloads authenticate with managed identities; secrets in code and shared accounts are prohibited.
- Restricted systems undergo quarterly access recertification.
- Encryption in transit uses TLS 1.2 minimum, TLS 1.3 preferred.

### 17.4 Related standards
STD-IAM-008, STD-SEC-009, STD-NET-011.

## 18. AP-13 — Separate IT and OT

### 18.1 Statement
Terminal operational technology is segmented from corporate IT and from the internet, and crosses that boundary only through controlled, inspected conduits.

### 18.2 Rationale
A compromise of gate or crane systems threatens safety as well as operations. IEC 62443 and the US Coast Guard cybersecurity rule require demonstrable segmentation.

### 18.3 Implications
- OT zones at Purdue levels 0-2 have no direct internet access.
- All IT/OT data exchange passes through the level 3.5 IT/OT DMZ; data to the cloud flows one-way via the DMZ broker (RA-03).
- Remote vendor access to OT uses the OT jump host with session recording and time-bound approval.
- Legacy OT assets that cannot be patched, such as the gate servers under EXC-2026-002, receive compensating segmentation controls.

### 18.4 Related standards
STD-NET-011, STD-IAM-008.

## 19. AP-14 — Observable by Default

### 19.1 Statement
Every service emits traces, metrics and logs in a standard form from its first release, and defines health endpoints and, where tiered, SLOs.

### 19.2 Rationale
Diagnosing incidents across HSP microservices, the Event Backbone and partner integrations is impossible without end-to-end correlation.

### 19.3 Implications
- New services use OpenTelemetry SDKs with W3C trace context propagation.
- Telemetry lands in Azure Monitor / Log Analytics with Grafana dashboards.
- Personal data and secrets must not appear in logs.
- Tier 0 and Tier 1 services publish SLOs; the milestone latency SLO is traced from HSP to Harbourline Connect.

### 19.4 Related standards
STD-OBS-010, STD-RES-015.

## 20. AP-15 — Everything as Code

### 20.1 Statement
Infrastructure, configuration, policy and deployment pipelines are defined as version-controlled code and applied through automation.

### 20.2 Rationale
Manual changes cause drift, are not auditable and slow down regional stamp deployment such as the UAE stamp proposed in CR-2026-014.

### 20.3 Implications
- Terraform is the only approved IaC tool for cloud resources.
- AKS workloads are deployed via Helm and GitOps (Flux).
- Azure Policy assignments, including mandatory tags, are managed as code.
- Portal changes in production are permitted only for break-glass incidents and must be reconciled into code within five working days.

### 20.4 Related standards
STD-CLD-007, STD-CTR-012.

## 21. AP-16 — Accountable Use of AI

### 21.1 Statement
Every AI-assisted decision or output that affects customers, employees, customs or safety has a named human who is accountable for it.

### 21.2 Rationale
AI models can be wrong with confidence. Customs declarations and safety-related decisions carry legal consequences, and the EU AI Act imposes obligations on EU-facing use cases.

### 21.3 Implications
- Every AI use case is registered in the AI Use Case Register with an `AIU-NNN` ID, risk tier and accountable owner.
- High-impact decisions (customs, safety, HR) require human review before action; DocIntel (APP-130, AIU-004) requires a validator to confirm customs-relevant fields (ADR-0033).
- The approved LLM platform is Azure OpenAI in approved regions; public consumer AI tools must not receive Internal, Confidential or Restricted data.
- Retrieval-augmented answers must cite their sources, and prompts and responses are logged for 90 days.

### 21.4 Related standards
STD-AI-013, STD-DAT-004, STD-DAT-005.

## 22. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 3.0 | 2023-06-15 | David Okafor | Catalog consolidated to 15 principles |
| 3.2 | 2024-11-21 | David Okafor | Aligned with Horizon 2028 goals |
| 4.0 | 2026-02-12 | David Okafor, Samuel Adeyemi | Added AP-16; AP-04 72-hour autonomy; AP-10 renamed; related standards added (ARB-2026-006) |
