---
doc_id: STD-IAM-008
title: Identity & Access Management Standard
doc_type: standard
togaf_phase: Preliminary
version: "2.0"
status: Approved
owner: Priya Raman, Principal Security Architect
approved_by: Architecture Review Board (ARB-2024-048)
effective_date: 2024-11-01
next_review: 2026-11-01
classification: Internal
related: [AP-12, AP-13, AP-15, STD-API-002, STD-DAT-004, STD-SEC-009, STD-CLD-007, STD-OBS-010, STD-NET-011, RA-02, RA-03, GOV-01, GOV-02]
---

# STD-IAM-008 — Identity & Access Management Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines how people, customers and workloads are identified, authenticated and authorised across Harbourline Logistics Group systems. It implements principle AP-12 (Zero Trust Access): no user or workload is trusted because of its network location, every access is explicitly verified, and privileges are the minimum needed for the shortest practical time. It supports Harbourline's obligations under NIS2 and the US Coast Guard maritime cybersecurity rule, both of which require strong access control for systems supporting port operations.

## 2. Scope

- All workforce identities: employees, contractors and partner staff (including Nordhaven Freight GmbH and Harbourline Gulf FZE).
- All customer identities used for Harbourline Digital products, including Harbourline Connect (APP-050).
- All workload identities: applications, pipelines, automation and integration services.
- All applications, cloud platforms (Azure, AWS), SaaS and on-premises systems.

OT identities inside terminal control zones (Purdue levels 0–2) are governed by STD-NET-011 and RA-03; access *into* those zones from IT is in scope of §7.4.

## 3. Related Principles and Normative References

- **AP-12 Zero Trust Access**; **AP-13 Separate IT and OT**; **AP-15 Everything as Code**.
- **STD-API-002** §6 (OAuth 2.0 for APIs); **STD-DAT-004** (Restricted data access); **STD-SEC-009** (secrets and certificates); **STD-OBS-010** (security logging); **STD-NET-011** (OT access).
- NIST SP 800-63B authenticator assurance levels (informative).

Normative terms follow RFC 2119.

## 4. Identity Providers

### 4.1 Workforce

1. **Microsoft Entra ID** (APP-100) is the **single workforce identity provider** for Harbourline. All workforce access to applications MUST authenticate against Entra ID via SAML 2.0 or OpenID Connect.
2. Separate directories, local application accounts and other workforce IdPs MUST NOT be introduced. Nordhaven's legacy directory MUST be consolidated into the Harbourline Entra ID tenant; until then access is federated.
3. Joiner/mover/leaver processes MUST be driven from the HR system of record through automated provisioning (SCIM where the target supports it). Leaver accounts MUST be disabled within 4 hours of termination and within 1 hour for involuntary terminations.

### 4.2 Customers

1. Customer identities MUST use **Microsoft Entra External ID**, branded **"Harbourline Connect ID"**.
2. Customer applications MUST NOT store customer passwords or implement their own credential stores.
3. Customer organisations MAY federate their own IdP to Harbourline Connect ID via OpenID Connect or SAML; such federation requires Harbourline Digital product owner approval.
4. Customer identity data is personal data and MUST be held in line with STD-DAT-005.

### 4.3 Workloads

1. Azure workloads MUST authenticate using **managed identities** (system- or user-assigned). AKS workloads MUST use workload identity federation.
2. CI/CD pipelines MUST use workload identity federation (OIDC) to Azure and AWS; long-lived service principal secrets for pipelines are prohibited.
3. Secrets MUST NOT be stored in source code, container images, configuration files or pipeline variables in clear text. Where a secret is unavoidable (e.g. a third-party API key), it MUST be stored in Azure Key Vault and retrieved at runtime by managed identity (STD-SEC-009).
4. AWS workloads (Nordhaven eu-central-1 estate) MUST use IAM roles; IAM user access keys are prohibited for workloads.

## 5. Authentication

### 5.1 Multi-factor authentication

| Population | Requirement |
|---|---|
| All workforce users | **MFA mandatory** for every sign-in, enforced by Conditional Access |
| Administrators and privileged role holders | **Phishing-resistant MFA (FIDO2 security keys or passkeys)** mandatory |
| Customer users (Harbourline Connect ID) | MFA mandatory; SMS one-time codes permitted only as fallback |
| Break-glass accounts | FIDO2 keys held in the Baltimore and Rotterdam safes; see §8.3 |

1. Legacy authentication protocols (basic authentication, NTLM for cloud apps) MUST be blocked.
2. Conditional Access policies MUST evaluate sign-in risk and user risk and block high-risk sign-ins pending remediation.
3. Conditional Access policies MUST be managed as code (AP-15) and changes reviewed by the security architecture team.

### 5.2 Session controls

1. Workforce sessions for Confidential and Restricted applications SHOULD re-authenticate at least every 12 hours.
2. Administrative portal sessions (Azure, AWS, Entra admin centre) MUST re-authenticate at least every 4 hours.

## 6. Authorisation

1. Access MUST be granted on least-privilege principles through roles assigned to Entra ID groups, not to individuals.
2. Application roles MUST be defined in the application registration and consumed from token claims; applications MUST NOT maintain parallel role stores for workforce users.
3. Azure RBAC assignments MUST be at the narrowest practical scope (resource group or resource); `Owner` at subscription scope is restricted to the platform team via PIM.
4. Segregation of duties MUST be enforced for finance and customs functions (for example, the same user cannot both create and approve a customs declaration submission).

## 7. Privileged Access

### 7.1 Just-in-time access

1. All privileged roles — Entra ID directory roles, Azure subscription Owner/Contributor, AWS administrator roles, database administrator roles for Restricted systems — MUST be granted through **Entra Privileged Identity Management (PIM)** as eligible, not permanent, assignments.
2. Activation is **just-in-time** with a **maximum duration of 8 hours**, requires justification and a ticket reference (ServiceNow, APP-110), and requires approval for Global Administrator and roles over Restricted data.
3. Standing (permanent) privileged assignments are prohibited except for break-glass accounts.

### 7.2 Accounts

1. **Shared accounts are prohibited.** Every human access MUST be attributable to a named individual.
2. Administrators MUST use a separate privileged account (e.g. `adm-` prefix) that is not mail-enabled and is not used for browsing or email.

### 7.3 Recertification

| System type | Recertification frequency | Reviewer |
|---|---|---|
| Systems holding **Restricted** data | **Quarterly** | Data Owner |
| Confidential systems | Semi-annually | Application Owner |
| Privileged role eligibility | Quarterly | CISO's team |
| Other systems | Annually | Application Owner |

Access not confirmed by the reviewer within 14 days of the review deadline MUST be removed automatically via Entra ID access reviews.

### 7.4 Access to OT environments

Remote access from IT to terminal OT zones MUST use the OT jump host with session recording and time-bound approval, as specified in STD-NET-011. Entra ID authentication with phishing-resistant MFA MUST be enforced at the jump host.

## 8. Logging and Break-Glass

1. Sign-in logs, audit logs and PIM activation logs MUST be forwarded to Microsoft Sentinel and retained for 24 months (STD-OBS-010).
2. Alerts MUST fire for PIM activation of Global Administrator, disabled MFA, and new federation trusts.
3. Two break-glass accounts MUST exist, excluded from Conditional Access only as documented, monitored for any sign-in, and tested every 6 months.

## 9. Compliance and Exceptions

1. Identity design is reviewed by the security architect (or delegate) in every Tier 1 ARB review; quorum rules in GOV-01 require the security architect's presence.
2. Entra ID Secure Score, PIM coverage and recertification completion are reported monthly to the CISO.
3. Deviations MUST be requested through the GOV-01 exception process and recorded in GOV-02 with an `EXC-YYYY-NNN` identifier, a maximum 12-month term (renewable once) and a remediation plan. Exceptions to the MFA or shared-account rules require CISO approval in addition to the ARB.

## 10. Document History

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 1.0 | 2023-05-01 | Priya Raman | Initial standard; Entra ID as workforce IdP; MFA for all users |
| 1.1 | 2024-03-01 | Priya Raman | Customer identity via Entra External ID ("Harbourline Connect ID"); managed identities mandatory |
| 1.2 | 2024-06-15 | Priya Raman | Nordhaven federation; AWS IAM role rules |
| 2.0 | 2024-11-01 | Priya Raman | Phishing-resistant MFA for admins; PIM just-in-time max 8 hours; quarterly recertification for Restricted systems; shared accounts prohibited; ARB-2024-048 |
