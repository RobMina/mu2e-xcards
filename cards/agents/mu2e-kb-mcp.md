---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-kb-mcp
name: Mu2e Knowledge Base MCP Server (kb)
description: >-
  MCP server that gives AI agents and chat clients search and retrieval over the
  Mu2e experiment's internal documentation, starting with Mu2e DocDB: technical
  notes, talks, design reviews, run plans and meeting slides, parsed into text,
  tables and image descriptions. Provides hybrid (BM25 full-text plus semantic
  embedding) search with metadata filters, full-document retrieval, figure
  retrieval, and a multi-step research agent that answers open questions with
  citations to DocDB documents. It is the Documentation interface of the Mu2e
  Genesis phase 1 project. In agentic data quality monitoring (DQM) it supplies
  context for anomaly investigation: when a detector metric or DQM histogram is
  flagged, an agent searches it for prior occurrences, known detector issues,
  commissioning notes, run plans and expert reports to help diagnose the root cause.
  It also grounds simulation and analysis agents for the Mu2e charged lepton
  flavor violation (muon-to-electron conversion) search at Fermilab. Runs on the
  Mu2e AI node at Fermilab for collaboration members; access needs the Fermilab
  network and a per-user Mu2e key.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - docdb
  - knowledge base
  - retrieval augmented generation
  - rag
  - document search
  - hybrid search
  - semantic search
  - mcp server
  - model context protocol
  - collaboration documentation
  - context assembly
  - data quality monitoring
  - dqm
  - anomaly investigation
  - root cause diagnosis
  - detector operations
  - charged lepton flavor violation
  - muon to electron conversion
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '0.2.6'
last_updated: '2026-10-15'
license:
  spdx_id: MIT
  name: MIT License
  url: https://github.com/Mu2e/kb-mcp/blob/main/LICENSE
relationships: []

io_contract:
  input_modes:
    - text/plain
    - application/json
  output_modes:
    - text/markdown
    - application/json
    - image/png
  modalities:
    - text
    - image
  task_tags:
    - document retrieval
    - question answering

extension:
  kind: agent
  skills:
    - Search Mu2e DocDB with hybrid full-text and semantic search (kb_search)
    - Filter searches by source, document type, DocDB number, title or date
    - Retrieve the full text of a DocDB document with its metadata (kb_get)
    - Retrieve a figure or slide image from a DocDB document (kb_get_image)
    - Answer open research questions about Mu2e with a multi-step agent that cites DocDB (kb_research)
    - Assemble documentation context for a flagged DQM anomaly (prior occurrences, known detector issues, expert notes)
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# Mu2e Knowledge Base MCP Server (kb)

A Model Context Protocol (MCP) server over the Mu2e knowledge base, so that any MCP client (Claude Code, Codex,
Cursor, goose, or the Mu2e agentic workflows) can search and read the collaboration's documentation. Software:
[Mu2e/kb-mcp](https://github.com/Mu2e/kb-mcp) (MIT). This card describes the deployment that serves the Mu2e
collaboration, version 0.2.6 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `kb_search` | Hybrid search (BM25 full-text and embeddings, fused) with optional reranking; Elasticsearch-style metadata filters (`term`, `terms`, `range`, `match`, `wildcard`, `bool`) on source, document type, DocDB id, title and timestamps |
| `kb_get` | Full text of one document, with metadata and the knowledge-graph concepts it mentions |
| `kb_get_image` | A figure or slide image referenced in a document, as an MCP image |
| `kb_research` | A multi-step research agent that runs several searches and returns a synthesised answer |

Documents are parsed into text, table and image chunks, and images are given generated descriptions, so slides and
plots are searchable. All data stays on site in a Fermilab-managed PostgreSQL database.

## Content

- **Mu2e DocDB**: about 24,000 documents (89,445 indexed text, table and image chunks on 2026-10-15).
- The tool interface also names Mu2e wiki pages, INSPIRE-HEP papers, meeting transcripts and uploads as sources.
  On 2026-10-15 only DocDB is populated in this deployment.

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: collaboration members only. It needs the Fermilab network (on site, VPN or an SSH tunnel) and a personal
  Mu2e MCP key, issued by the Mu2e AI infrastructure maintainers and sent as an HTTP bearer token.
- Read-only: no tool modifies the knowledge base.

## Role in the Mu2e Genesis project

This is the Documentation interface of the Mu2e Genesis phase 1 project, "Expedited Discovery by Leveraging Agentic
Workflows for the Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514). In the agentic DQM workflow it
supplies the historical context for each flagged anomaly. In the optimization workflow it grounds agents in Mu2e
documentation. It builds on the AmSC IDA Pilot Knowledge Extraction (HEP-KE) work.

## Limitations

- Coverage is DocDB only today; wiki, papers and meeting transcripts are not yet ingested.
- `kb_research` failed server-side on 2026-10-15; `kb_search` and `kb_get` cover most needs.
- Content is collaboration-internal. Answers inherit any errors in the source documents and in the automatically
  generated summaries and image descriptions.
- Not reachable from outside the Fermilab network.
