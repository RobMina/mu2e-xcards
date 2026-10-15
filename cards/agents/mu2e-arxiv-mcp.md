---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-arxiv-mcp
name: arXiv Paper Search MCP Server (Mu2e deployment)
description: >-
  Read-only MCP server that lets AI agents search arXiv preprints and fetch paper
  metadata through arXiv's public API: search by free text, title, author,
  abstract or arXiv category (for example hep-ex, hep-ph, physics.ins-det), with
  arXiv's own query syntax for compound searches, sorted by relevance or date;
  and look up one paper by arXiv id for its title, authors, abstract, categories,
  dates, DOI and PDF link. Agents use it for literature context: recent
  results and methods in particle physics, detector technology, machine learning
  for physics and anomaly detection, when planning analyses, writing reports or
  explaining findings. Deployed by the Mu2e Genesis phase 1 project on the Mu2e AI
  node at Fermilab next to the Mu2e documentation, data-quality and logbook MCP
  servers; complements the INSPIRE-HEP server, which adds citations, BibTeX and
  collaboration searches. Reachable from the Fermilab network; arXiv itself is
  public.

science:
  - particle-physics
keywords:
  - arxiv
  - preprints
  - literature search
  - paper search
  - scientific papers
  - abstracts
  - hep-ex
  - hep-ph
  - physics.ins-det
  - machine learning for physics
  - research assistant
  - mcp server
  - model context protocol
  - mu2e
  - high energy physics
sensitivity: general
developed_by:
  - Mu2e Genesis team
version: '0.4.0'
last_updated: '2026-10-15'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/Mu2e/aitools/blob/main/LICENSE
relationships: []

io_contract:
  input_modes:
    - text/plain
    - application/json
  output_modes:
    - application/json
  modalities:
    - text
  task_tags:
    - literature search
    - document retrieval

extension:
  kind: agent
  skills:
    - Search arXiv by text, title, author, abstract or category, sorted by relevance or date (search_papers)
    - Use arXiv query syntax (ti, au, abs, cat with AND, OR, ANDNOT) for compound searches
    - Fetch one paper's metadata and PDF link by arXiv id (get_paper)
    - Report rate-limit settings and capability notes (get_server_info)
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# arXiv Paper Search MCP Server (Mu2e deployment)

A read-only Model Context Protocol (MCP) server over arXiv's public Atom API, using the `arxiv` Python package. It
is a general literature tool, deployed for Mu2e agents alongside the experiment-specific servers. Software:
`mcp/arxiv` in [Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0). This card describes the deployment on
the Mu2e AI node, version 0.4.0 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `search_papers` | Search by `query` (raw arXiv syntax) and/or named `title`, `author`, `abstract`, `category` filters, combined with AND; sort by relevance, last update or submission date; default 20 results |
| `get_paper` | Full metadata for one arXiv id: title, authors, abstract, categories, dates, DOI, journal reference, PDF link (nothing is downloaded server-side) |
| `get_server_info` | Version, rate-limit settings and notes |

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: reachable from the Fermilab network (on site, VPN or an SSH tunnel); no key. The data are public arXiv
  metadata, and anyone outside Fermilab can run the same server from the open-source package.
- Read-only.

## Role in the Mu2e Genesis project

Literature context for the agents of the Mu2e Genesis phase 1 project (Mu2e-doc-57514): grounding reports,
optimization studies and anomaly explanations in published work, alongside the Mu2e knowledge base (internal
documents) and INSPIRE-HEP (citations and bibliography).

## Limitations

- arXiv has no citation graph, author profiles, collaboration filter or BibTeX; use the INSPIRE-HEP server for those.
- arXiv rate-limits per source IP, and the server paces itself (3 s between pages, 3 retries), so it is not meant
  for high-volume or concurrent use. A slow search usually means arXiv is throttling.
- Metadata only; it does not read paper full text.
