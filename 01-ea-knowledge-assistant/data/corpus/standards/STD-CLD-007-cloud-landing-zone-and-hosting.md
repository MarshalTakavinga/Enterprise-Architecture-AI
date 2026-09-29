---
doc_id: STD-CLD-007
title: Cloud Landing Zone & Hosting Standard
doc_type: standard
togaf_phase: Preliminary
version: "2.2"
status: Approved
owner: Kenji Watanabe, Principal Cloud Architect
approved_by: Architecture Review Board (ARB-2025-014)
effective_date: 2025-04-01
next_review: 2026-10-01
classification: Internal
related: [AP-10, AP-11, AP-12, AP-15, AP-06, STD-DAT-004, STD-DAT-005, STD-IAM-008, STD-SEC-009, STD-CTR-012, STD-RES-015, STD-OBS-010, ADR-0021, ADR-0027, RA-02, GOV-01, GOV-02]
---

# STD-CLD-007 — Cloud Landing Zone & Hosting Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines where and how Harbourline Logistics Group workloads are hosted in public cloud: the primary and secondary cloud providers, approved regions, the landing zone structure, mandatory tagging, infrastructure-as-code, and network ingress rules. It underpins the Horizon 2028 goal of exiting the Baltimore on-premises data centre by **30 June 2027** without creating an uncontrolled cloud estate.

## 2. Scope

- All workloads deployed to Microsoft Azure or Amazon Web Services by Harbourline, its legal entities (including Nordhaven Freight GmbH) and delivery partners.
- All environments: production, pre-production, test, development and sandbox.
- Migration of workloads from the Baltimore data centre.

Terminal edge hosting for Tier 0 systems (Navis N4 on-premises edge clusters, ADR-0027) is out of scope and governed by RA-03 and STD-NET-011. SaaS applications are out of scope except for identity integration (STD-IAM-008).

## 3. Related Principles and Normative References

- **AP-10 Cloud-Smart and Portable** — Azure primary, AWS secondary, avoid unnecessary lock-in.
- **AP-11 Managed Services over Self-Managed Infrastructure**; **AP-12 Zero Trust Access**; **AP-15 Everything as Code**; **AP-06 Data Residency Follows Jurisdiction**.
- **STD-DAT-005** (residency), **STD-CTR-012** (containers), **STD-RES-015** (resilience), **STD-SEC-009** (encryption), **STD-IAM-008** (identity), **STD-OBS-010** (monitoring).
- **ADR-0021** Temporarily Retain Nordhaven TMS on AWS.
- **RA-02** Cloud-Native Application on the Azure Landing Zone.

Normative terms follow RFC 2119.

## 4. Cloud Providers

### 4.1 Azure — primary cloud

Microsoft Azure is Harbourline's **primary cloud**. All new workloads MUST be hosted on Azure unless a condition in §4.2 applies.

### 4.2 AWS — secondary cloud

AWS is the **secondary cloud** and MAY be used only in the following cases:

| Case | Condition | Current example |
|---|---|---|
| (a) Nordhaven legacy workloads | In **eu-central-1** only, under exception **EXC-2025-003**, until migrated into HSP | Nordhaven TMS (APP-021), ADR-0021 |
| (b) DR-only workloads | Approved by the ARB where cross-provider recovery is justified | None approved at time of issue |
| (c) Services with no Azure equivalent | Approved by the ARB (Tier 1) with documented comparison of Azure options | — |

New AWS accounts MUST be created under the Harbourline AWS Organization with centrally managed guardrails; standalone accounts on corporate cards are prohibited.

### 4.3 Other clouds

Other public cloud providers MUST NOT host Harbourline workloads. SaaS products are assessed separately through ARB review.

## 5. Approved Regions

| Azure region | Typical use |
|---|---|
| East US 2 | US primary; Tidewater Data Platform; SAP S/4HANA (APP-010) |
| Central US | US DR |
| Canada Central | Canadian primary (where residency required) |
| Canada East | Canadian DR |
| West Europe | EU primary |
| North Europe | EU DR |
| UAE North | Harbourline Gulf workloads |

1. Resources MUST be deployed only in the regions above. Azure Policy denies resource creation elsewhere; global services (Front Door, Entra ID) are exempt.
2. Region selection for personal data MUST follow STD-DAT-005.
3. Adding a region requires Tier 1 ARB approval.

## 6. Landing Zone Structure

### 6.1 Management groups

Harbourline uses **Azure Landing Zones** aligned to the Microsoft Cloud Adoption Framework (CAF). The management group hierarchy is:

| Management group | Purpose |
|---|---|
| `hlg-platform` | Shared platform subscriptions: connectivity (hub networks, firewalls), identity, management (Log Analytics, Sentinel) |
| `hlg-corp` | Internal-facing workloads with private connectivity only (e.g. HSP back-end services, integration runtime) |
| `hlg-online` | Internet-facing workloads (e.g. Harbourline Connect, partner APIs) with ingress through approved edge services |
| `hlg-sandbox` | Experimentation; no production data, no connectivity to corporate networks, budgets capped at USD 2,000 per subscription per month |

1. Each application SHOULD have a separate subscription per environment (e.g. `sub-app022-prod`, `sub-app022-nonprod`).
2. Subscriptions MUST be vended through the platform team's subscription-vending Terraform module, which applies policies, budgets, diagnostic settings and role assignments.
3. Policy assignments at management group level MUST NOT be overridden at subscription level without an exception.

### 6.2 Mandatory tags

Every resource group and resource MUST carry the following tags; Azure Policy denies creation without them:

| Tag | Example | Notes |
|---|---|---|
| `owner` | `amara.osei@harbourline.example` | Named accountable person, not a distribution list |
| `cost-centre` | `CC-4410` | Finance cost centre |
| `app-id` | `APP-022` | CMDB application ID from ServiceNow |
| `data-classification` | `restricted` | Per STD-DAT-004 |
| `environment` | `prod` | One of `prod`, `preprod`, `test`, `dev`, `sandbox` |

Resources without valid tags discovered by the monthly compliance scan are reported to the owner and, after 30 days, to the ARB.

## 7. Infrastructure as Code

1. **Terraform** MUST be used for all infrastructure provisioning in Azure and AWS (AP-15). Bicep, ARM templates and CloudFormation MUST NOT be used for new infrastructure.
2. Terraform state MUST be stored in the platform-managed remote backend with state locking and encryption.
3. All changes to production infrastructure MUST be applied through a CI/CD pipeline with plan review; manual changes via the portal or CLI in production are prohibited except during declared incidents, and MUST be reconciled into code within 5 working days.
4. Approved shared modules from the platform module registry SHOULD be used for common resources (networking, PostgreSQL, Key Vault, AKS).

## 8. Network and Ingress

1. Virtual machines MUST NOT have **public IP addresses**.
2. Internet ingress MUST be through **Azure Front Door with WAF** (global, internet-facing web and APIs) or **Azure Application Gateway with WAF** (regional). APIs are additionally fronted by the Harbourline API Gateway (STD-API-002).
3. PaaS services MUST use private endpoints; public network access MUST be disabled unless the service is an approved ingress component.
4. Egress to the internet MUST pass through the hub firewall in the `hlg-platform` connectivity subscription.
5. Administrative access to VMs MUST use Azure Bastion with Entra ID authentication; RDP/SSH exposed to the internet is prohibited.

## 9. Hosting Model Preference

Consistent with AP-11, teams MUST choose the highest-level managed service that meets the requirement:

1. SaaS (if the capability is not differentiating).
2. PaaS (e.g. App Service, Azure Functions, PostgreSQL Flexible Server).
3. Containers on AKS or Azure Container Apps (STD-CTR-012).
4. Virtual machines — only for vendor software that cannot run otherwise, with justification in the design.

## 10. Compliance and Exceptions

1. Landing zone policies enforce §5, §6.2 and §8 automatically; policy compliance is reported weekly to the Principal Cloud Architect.
2. ARB reviews verify provider choice, region, subscription placement and ingress design.
3. Deviations MUST be requested through the GOV-01 exception process and recorded in GOV-02. EXC-2025-003 (Nordhaven TMS on AWS eu-central-1) is the reference example of a case (a) exception: time-bound, renewable once, with the HSP migration as its remediation plan.

## 11. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2023-04-01 | Kenji Watanabe | Initial Azure landing zone standard; management groups and tagging |
| 2.0 | 2024-08-01 | Kenji Watanabe | Added AWS secondary-cloud conditions after Nordhaven acquisition (ADR-0021); UAE North added |
| 2.1 | 2024-12-01 | Kenji Watanabe | Terraform mandated for all IaC; `data-classification` tag mandatory |
| 2.2 | 2025-04-01 | Kenji Watanabe | Hosting model preference; ingress rules (Front Door/App Gateway + WAF); sandbox budgets; ARB-2025-014 |
