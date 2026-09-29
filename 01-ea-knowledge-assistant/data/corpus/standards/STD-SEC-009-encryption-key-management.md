---
doc_id: STD-SEC-009
title: Encryption & Key Management Standard
doc_type: standard
version: "1.5"
status: Approved
owner: Priya Raman, Principal Security Architect
approved_by: Architecture Review Board (ARB-2024-061)
effective_date: 2025-01-01
next_review: 2027-01-01
classification: Internal
related: [AP-02, AP-05, AP-12, AP-15, STD-DAT-004, STD-DAT-005, STD-IAM-008, STD-EVT-003, STD-CLD-007, STD-NET-011, STD-OBS-010, GOV-01, GOV-02]
---

# STD-SEC-009 — Encryption & Key Management Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard defines the minimum cryptographic controls that protect Harbourline data in transit and at rest, and the way cryptographic keys, secrets and certificates are created, stored, rotated and retired. It turns the security and compliance principles into testable rules that solution architects, platform engineers and suppliers can design against and that the Architecture Review Board (ARB) can assess.

## 2. Scope

### 2.1 In scope

- All workloads hosted in Harbourline Azure subscriptions, including the Harbourline Shipment Platform (APP-022), Harbourline Connect (APP-050), the Tidewater Data Platform (APP-080) and the Customs Filing Gateway (APP-060).
- Workloads hosted on AWS under the conditions of STD-CLD-007, including Nordhaven TMS (APP-021) under EXC-2025-003.
- SaaS services that store Harbourline data classified Confidential or Restricted under STD-DAT-004.
- On-premises servers in the Baltimore data centre and at terminal edge sites, to the extent that the technology supports the controls.

### 2.2 Out of scope

- Cryptographic protection inside OT field devices at Purdue levels 0-1 that cannot support modern cryptography. Compensating network controls for those devices are defined in STD-NET-011.
- Consumer-facing password policies, which are governed by STD-IAM-008.

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-02 Compliance by Design | Encryption controls are designed in, not retrofitted after audit |
| AP-05 Data Is an Asset with a Named Owner | The data owner approves the key-management model for Restricted data |
| AP-12 Zero Trust Access | Every connection is encrypted and authenticated regardless of network location |
| AP-15 Everything as Code | Key Vaults, key policies and certificate automation are provisioned with Terraform |
| STD-DAT-004 | Defines the Restricted classification that triggers the stricter rules below |
| STD-DAT-005 | Keys for jurisdiction-bound data are held in the same region as the data |
| STD-IAM-008 | Access to keys and secrets uses managed identities and PIM |
| STD-EVT-003 | Field-level encryption of Restricted fields in event payloads |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Encryption in Transit

### 4.1 Protocol versions

1. All network traffic carrying Harbourline data MUST use TLS 1.2 or higher. TLS 1.3 is the preferred protocol and MUST be enabled wherever the platform supports it.
2. TLS 1.0, TLS 1.1, SSL 3.0 and earlier MUST be disabled on every endpoint, including load balancers, Azure Front Door, Application Gateway, API Management and FortiGate VIPs.
3. Cipher suites for TLS 1.2 MUST be restricted to AEAD suites with forward secrecy (ECDHE with AES-GCM or ChaCha20-Poly1305). CBC-mode and RSA key-exchange suites MUST NOT be offered.

### 4.2 Internal traffic

1. Service-to-service traffic inside AKS clusters and between Azure services MUST be encrypted, including traffic that never leaves a private virtual network. "Trusted network" is not an exemption (AP-12).
2. Connections to PostgreSQL Flexible Server, Azure SQL Database and Azure Cache for Redis MUST enforce TLS on the server side (`require_secure_transport` or equivalent).
3. Site-to-cloud and site-to-site traffic MUST traverse the Fortinet SD-WAN IPsec overlay defined in STD-NET-011 §6; the IPsec proposals MUST use AES-256-GCM with Diffie-Hellman group 20 or higher.

### 4.3 TLS inspection

TLS interception is permitted only at the controlled inspection points defined in STD-NET-011 §8. Inspection certificates MUST be issued from the Harbourline internal CA and MUST NOT be exported from the FortiGate or proxy appliance.

## 5. Encryption at Rest

1. All persistent storage (managed disks, Blob Storage, ADLS Gen2, databases, backups, snapshots and message logs) MUST be encrypted with AES-256.
2. Platform-managed keys are acceptable for Public, Internal and Confidential data.
3. Restricted data MUST be encrypted with customer-managed keys (CMK) held in Azure Key Vault Premium or Azure Key Vault Managed HSM (see §6). This applies to primary stores, replicas, backups and DR copies.
4. Restricted fields carried in Harbourline Event Backbone payloads MUST be field-level encrypted before publication, in line with STD-EVT-003. The encryption key MUST be scoped to the producing domain.
5. Backups exported to AWS or any secondary location MUST retain encryption end to end; decrypted backups MUST NOT be staged in intermediate storage.

## 6. Key Management

### 6.1 Key stores

| Data classification | Approved key store | Key protection |
|---|---|---|
| Public / Internal | Azure Key Vault Standard or platform-managed | Software |
| Confidential | Azure Key Vault Standard or Premium | Software or HSM |
| Restricted | Azure Key Vault Premium or Managed HSM | HSM-backed (FIPS 140-2 Level 2 minimum; Level 3 for Managed HSM) |
| Nordhaven on AWS (EXC-2025-003) | AWS KMS customer-managed keys in eu-central-1 | HSM-backed |

### 6.2 Key vault topology

1. Each application (by `app-id` tag) MUST have its own Key Vault per environment; Key Vaults MUST NOT be shared across applications.
2. A Key Vault holding keys for jurisdiction-bound data MUST be deployed in the same Azure region as the data it protects (for example, West Europe for EU personal data), consistent with STD-DAT-005.
3. Key Vaults MUST have soft-delete and purge protection enabled, public network access disabled, and access only through private endpoints.
4. Key Vaults MUST use Azure RBAC authorisation; legacy access policies MUST NOT be used for new vaults.

### 6.3 Rotation and lifecycle

1. Customer-managed keys MUST be rotated at least every 12 months. Automatic rotation policies SHOULD be configured in Key Vault rather than manual procedures.
2. A key MUST be rotated immediately when compromise is suspected; the incident is handled under the security incident process owned by the CISO, Hannah Brennan.
3. Retired key versions MUST remain available (disabled for encryption, enabled for decryption) until all data encrypted under them has been re-encrypted or has reached end of retention.
4. Key deletion for Restricted data requires approval of the data owner and the Principal Security Architect, and MUST be logged.

### 6.4 Separation of duties

1. Administrators of a data store MUST NOT hold key-management rights on the CMK protecting that store.
2. Key Vault administrative roles MUST be activated through Entra PIM, just-in-time, in accordance with STD-IAM-008.
3. Workloads MUST access keys and secrets with managed identities. Secrets, keys, connection strings and certificates MUST NOT appear in source code, container images, pipeline variables in plain text, or logs (see STD-OBS-010).

## 7. Certificates

1. Public-facing TLS certificates MUST have a maximum lifetime of 397 days.
2. Certificate issuance and renewal MUST be automated through Key Vault certificate integration with an approved public CA, or through the internal CA for private endpoints. Manual renewal is not permitted for new services.
3. Renewal MUST begin no later than 30 days before expiry; expiry alerts at 30, 14 and 7 days MUST be routed to the owning team through Azure Monitor.
4. Wildcard certificates SHOULD NOT be used; where used, they MUST be limited to a single subdomain and a single application.
5. Private keys for certificates MUST be non-exportable where the platform supports it.

## 8. Cryptographic Algorithms

| Purpose | Approved | Not permitted |
|---|---|---|
| Symmetric encryption | AES-256-GCM, AES-256-XTS (disk) | DES, 3DES, RC4, AES-ECB |
| Asymmetric | RSA ≥ 3072 bits, ECDSA P-256/P-384 | RSA < 2048 bits |
| Hashing | SHA-256, SHA-384, SHA-512 | MD5, SHA-1 |
| Password storage (where unavoidable) | Argon2id, bcrypt | Unsalted or fast hashes |

Existing RSA 2048-bit keys MAY remain until their next scheduled rotation, after which RSA 3072 or ECDSA MUST be used.

## 9. Compliance & Exceptions

1. Conformance is assessed at ARB Tier 1 and Tier 2 reviews using the security checklist maintained under GOV-01. Azure Policy assignments at the `hlg-platform` management group enforce TLS minimums, CMK for tagged Restricted resources and Key Vault purge protection; non-compliant resources are reported weekly to the owner.
2. Deviations MUST be requested through the exception process in GOV-01 and, if granted, are recorded in the Architecture Exceptions Register (GOV-02) with an `EXC-YYYY-NNN` identifier, a remediation plan and a maximum duration of 12 months, renewable once.
3. Legacy platforms that cannot meet §4.1 (for example, Windows Server 2012 R2 gate servers under EXC-2026-002) MUST be isolated by the network controls in STD-NET-011 until retired.

## 10. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2023-06-12 | Priya Raman | First issue; TLS 1.2 minimum and AES-256 at rest |
| 1.2 | 2024-02-05 | Priya Raman | Added Key Vault topology rules and certificate automation |
| 1.4 | 2024-09-01 | Priya Raman | Aligned with STD-DAT-004 v3.0; CMK mandatory for Restricted data |
| 1.5 | 2025-01-01 | Priya Raman | Certificate lifetime ≤ 397 days; AWS KMS rules for Nordhaven; field-level encryption for events (ARB-2024-061) |
| 1.5 | 2026-01-08 | Priya Raman | Annual review; no substantive change; next review set to 2027-01-01 |
