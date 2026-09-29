# Synthetic architecture repository — Harbourline Logistics Group

`corpus/` contains **48 original documents** (~66,000 words) forming the architecture repository of
*Harbourline Logistics Group*, a **fictional** global freight, port-terminal and contract-logistics company
(US, Canada, EU, UAE; Azure primary / AWS secondary; acquired a German forwarder in 2024; running a
USD 118M "Horizon 2028" programme to consolidate three transport management systems).

The documents are written to behave like a real repository: they cross-reference each other by ID,
carry owners, versions, approval decisions and review dates, contain normative MUST/SHOULD clauses,
and include the inconsistencies and open issues real repositories have (for example an exception that
expires before the migration it covers is due — see GOV-02 and ADR-0021).

| Folder | Documents | Examples |
|---|---|---|
| `principles/` | 1 catalog, 16 principles (Name / Statement / Rationale / Implications) | AP-04 Business Continuity at the Quay, AP-08 Event-First Integration |
| `standards/` | 15 technology standards with numbered, citable clauses | STD-INT-001 Integration Patterns, STD-DB-006 Database Selection, STD-NET-011 SD-WAN & OT Segmentation |
| `adrs/` | 12 Architecture Decision Records | ADR-0007 Confluent Cloud, ADR-0012 Cosmos DB for telemetry, ADR-0036 MPLS → SD-WAN |
| `reference-architectures/` | 4 | RA-01 Event-Driven Integration, RA-03 Terminal Edge & OT |
| `togaf-deliverables/` | 13 deliverables following the TOGAF ADM deliverable structure | Request for Architecture Work, Architecture Vision, Statement of Architecture Work, Architecture Definition Document, Architecture Requirements Specification, Roadmap & Migration Plan, Architecture Contract, Compliance Assessment, Change Request, Requirements Impact Assessment |
| `governance/` | 3 | ARB charter & governance framework, Exceptions register, Glossary |

Every file starts with YAML front matter (`doc_id`, `doc_type`, `togaf_phase`, `version`, `status`,
`owner`, `approved_by`, `effective_date`, `related`) that the ingestion pipeline turns into document metadata.

`WORLD_BIBLE.md` is the authoring reference used to keep facts consistent across documents. It is
**not** indexed.

## Provenance and licensing

All content is original, written for this portfolio. **No text from The Open Group's TOGAF® Standard
or its template deliverables is used.** The Open Group licence for those materials prohibits their use
with generative AI systems, and redistribution. Only the publicly known deliverable *names* and generic
structure (e.g. principles as Name / Statement / Rationale / Implications) are followed. TOGAF is a
registered trademark of The Open Group.

Real vendor products (Azure, Confluent, Fortinet, Navis N4, SAP, Salesforce…) are named because real
enterprises use them; nothing here describes any real company's architecture.
