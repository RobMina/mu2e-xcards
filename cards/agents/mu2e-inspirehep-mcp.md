---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-inspirehep-mcp
name: INSPIRE-HEP Literature MCP Server (Mu2e deployment)
description: >-
  Read-only MCP server that lets AI agents search the INSPIRE-HEP high energy
  physics literature database through its public REST API: search papers by
  text, title, author, collaboration or category, sorted by most recent or most
  cited; get a paper's full record by INSPIRE record id, DOI or arXiv id; list an
  author's papers; follow the citation graph (papers citing a paper, and the
  references a paper cites); find a collaboration's publications (for example
  Mu2e, COMET, MEG II, CMS); and export BibTeX or LaTeX citations. Agents use it
  for bibliography, prior-art and citation work: finding the published
  measurements and methods behind an analysis, checking who cites a result, and
  writing reports with correct references. Deployed by the Mu2e Genesis phase 1
  project on the Mu2e AI node at Fermilab, next to the Mu2e documentation,
  data-quality and logbook MCP servers; complements the arXiv server. Reachable
  from the Fermilab network; INSPIRE-HEP itself is public.

science:
  - particle-physics
keywords:
  - inspire-hep
  - inspire
  - hep literature
  - citations
  - citation graph
  - references
  - bibtex
  - bibliography
  - collaboration papers
  - author papers
  - prior art
  - literature search
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
    - application/x-bibtex
  modalities:
    - text
  task_tags:
    - literature search
    - citation analysis
    - document retrieval

extension:
  kind: agent
  skills:
    - Search HEP papers by text, title, author, collaboration or category, most recent or most cited (search_papers)
    - Get a paper's full record by INSPIRE record id, DOI or arXiv id (get_paper_details)
    - List one author's papers (get_author_papers)
    - Find papers citing a paper, and the references it cites (get_citations, get_references)
    - Find a collaboration's publications (search_by_collaboration)
    - Export BibTeX or LaTeX citations (get_bibtex)
    - Retrieve a paper's figures where INSPIRE exposes them (get_paper_figures, best effort)
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# INSPIRE-HEP Literature MCP Server (Mu2e deployment)

A read-only Model Context Protocol (MCP) server over INSPIRE-HEP's public REST API (`inspirehep.net/api`), written
independently for Mu2e (it does not contain code from the third-party `inspirehep-mcp` package). It is a general HEP
literature tool, deployed for Mu2e agents alongside the experiment-specific servers. Software: `mcp/inspirehep` in
[Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0). This card describes the deployment on the Mu2e AI
node, version 0.4.0 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `search_papers` | Literature search with INSPIRE's field syntax plus named title, author, collaboration and category filters; sort most recent or most cited |
| `get_paper_details` | One record by INSPIRE recid, DOI or arXiv id |
| `get_author_papers` | Papers by an author name (a literature search, not an author-profile lookup) |
| `get_citations`, `get_references` | Incoming and outgoing citations of a paper |
| `search_by_collaboration` | A collaboration's papers, optionally with a query |
| `get_bibtex` | BibTeX or LaTeX citation text |
| `get_paper_figures` | Figures, best effort |
| `server_stats`, `get_server_info` | Cache and request counters; version, rate limit, cache settings |

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: reachable from the Fermilab network (on site, VPN or an SSH tunnel); no key. The data are public
  INSPIRE-HEP records, and anyone outside Fermilab can run the same server from the open-source package.
- Read-only. Responses are cached for an hour.

## Role in the Mu2e Genesis project

Bibliography and prior art for the agents of the Mu2e Genesis phase 1 project (Mu2e-doc-57514): placing Mu2e
results among published measurements, citing methods correctly in agent-written reports, and finding related work
for optimization and anomaly-detection studies. Pairs with the arXiv server (newest preprints) and the Mu2e
knowledge base (internal documents).

## Limitations

- `get_paper_figures` is best effort: INSPIRE's public API does not reliably expose figures.
- INSPIRE limits each source IP to 15 requests per 5 seconds; the server paces its own requests at 2 per second,
  but cannot account for other traffic from the same IP.
- Metadata and citations only; no paper full text.
