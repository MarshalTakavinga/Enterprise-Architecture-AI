# ADR-P002 — PostgreSQL + pgvector as the vector store

**Status:** Accepted · **Date:** 2026-09-28 · **Decider:** Marshal Takavinga

## Context
The index holds about 550 chunks today. A large real enterprise repository might reach 50–100k
chunks. The service also needs to store document metadata and, in the future, the audit log.

## Options
| Option | Pros | Cons |
|---|---|---|
| **PostgreSQL + pgvector** | One managed database for metadata, vectors and logs; SQL joins between chunks and documents; available as a managed service on Azure and AWS; HNSW indexing when needed | Not the fastest at hundreds of millions of vectors |
| Dedicated vector DB (Pinecone, Weaviate, Qdrant) | Built for very large scale; filtering features | Another platform to operate, secure and pay for; metadata split across systems |
| Azure AI Search | Hybrid search built in | Ties the design to Azure, against a vendor-neutral positioning; higher fixed cost |

## Decision
**pgvector.** Exact search is used at the current size, and an HNSW index is created automatically
above 50k chunks. An in-memory store with the same interface is used for development and CI.

## Consequences
- ✅ Simpler operations, and the same design on Azure Database for PostgreSQL or Amazon RDS.
- ✅ BM25 runs in the application over chunks loaded from the database. This is fine at repository
  scale.
- ⚠ Reconsider when the index reaches millions of vectors or needs multi-tenant filtering. At that
  point, move BM25 to Postgres full-text search or adopt a search service.
