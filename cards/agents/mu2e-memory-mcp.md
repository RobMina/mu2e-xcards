---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-memory-mcp
name: Mu2e Persistent Agent Memory MCP Server (memory)
description: >-
  MCP server that gives AI agents persistent, versioned project memory that
  survives across sessions, machines and ephemeral sandboxes: agents store Markdown
  or text documents (notes, findings, plans, results of a study, what an
  optimization campaign learned) under a project and name, and read them back
  later. Every write adds a new version and nothing is ever overwritten or deleted,
  so an agent's history stays auditable; documents carry keywords, a description,
  a weight and an optional expiry so the right one can be found again; listings
  show sizes, never content, so an agent decides what to read before reading it.
  Each caller's documents are private to the owner named by their Mu2e key. It is
  the memory layer for agentic workflows in the Mu2e Genesis phase 1 project: an
  agent stores what a simulation or optimization campaign learned (configurations
  tried, results, dead ends) so that later agents and later campaigns build on it
  instead of starting over, and data-quality and analysis agents keep running notes
  and hand work over between sessions. Runs on the Mu2e
  AI node at Fermilab with storage in a Fermilab-managed PostgreSQL database;
  access needs the Fermilab network and a Mu2e key.

science:
  - particle-physics
keywords:
  - agent memory
  - persistent memory
  - long-term memory
  - project memory
  - versioned documents
  - append-only
  - knowledge persistence
  - session continuity
  - optimization memory
  - campaign results
  - lessons learned
  - handover between sessions
  - agentic workflows
  - provenance
  - mcp server
  - model context protocol
  - mu2e
  - fermilab
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '0.7.3'
last_updated: '2026-10-15'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/Mu2e/aitools/blob/main/LICENSE
relationships: []

io_contract:
  input_modes:
    - text/plain
    - text/markdown
    - application/json
  output_modes:
    - text/markdown
    - application/json
  modalities:
    - text
  task_tags:
    - agent memory
    - knowledge persistence

extension:
  kind: agent
  skills:
    - Store a document under a project and name, replacing or appending, as a new version (put_document)
    - Read the current or any earlier version of a document (get_document)
    - List projects, and documents with size, keywords, weight and dates but no content (list_projects, list_documents)
    - Show every stored version of a document (list_versions)
    - Update keywords, description, weight, expiry, or retire a document from listings (set_metadata)
    - Report the owner the caller's key resolves to (get_server_info)
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# Mu2e Persistent Agent Memory MCP Server (memory)

A Model Context Protocol (MCP) server that stores agents' documents in PostgreSQL and serves them back later, across
sessions and across per-session sandboxes that keep no disk of their own. Unlike the other Mu2e MCP servers it
writes, but only by appending. Software: `mcp/memory` in [Mu2e/aitools](https://github.com/Mu2e/aitools)
(Apache-2.0). This card describes the deployment that serves the Mu2e collaboration, version 0.7.3 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `put_document` | Create a document or add a version; `mode="replace"` stores the content given, `mode="append"` adds to the current content. Optional keywords, description, weight (0-100), expiry |
| `get_document` | The current or a given version. Refuses to return more than about 100 kB inline; can write a large document to a file instead |
| `list_projects` | The caller's project names |
| `list_documents` | Metadata and size, never content; filter by project, name, keywords, description, weight, dates; include expired or retired on request |
| `list_versions` | Every version of a document, newest first |
| `set_metadata` | Change metadata, or retire a document (hide it from listings) |
| `get_server_info` | Version, limits, and the owner the caller's key resolves to |

## Ownership, privacy and permanence

- **A document belongs to an owner, a project and a name.** The owner is the name of the caller's Mu2e key and is
  never a tool argument, so a caller cannot read or write another owner's documents.
- **Shared keys share memory.** Everyone holding a group or collaboration-wide key is the same owner and sees and
  versions the same documents. Use a personal key for private notes, and a group key only for memory meant to be
  shared.
- **Nothing is deleted.** Every write is a new row. Retiring a document only hides it from listings. Removing content
  (a pasted credential, personal data) needs a database administrator, so never store secrets.
- Documents are capped at 1 MiB; Markdown by convention.

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: collaboration members only. It needs the Fermilab network (on site, VPN or an SSH tunnel) and a Mu2e MCP
  key, issued by the Mu2e AI infrastructure maintainers and sent as an HTTP bearer token. The key decides whose
  memory you see.
- Good practice for agents: list before reading, give every document keywords and a description, and set a weight
  so the important ones come first.

## Role in the Mu2e Genesis project

The memory layer for the agentic workflows of the Mu2e Genesis phase 1 project, "Expedited Discovery by Leveraging
Agentic Workflows for the Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514). The project plans an
optimization memory that records what earlier simulation and optimization campaigns found, so later agents build on
it, and a reporting agent that writes results back for the collaboration; data-quality and analysis agents can keep
running notes the same way. Append-only versions keep a traceable record of what each agent knew and wrote.

## Limitations

- Isolation between owners is enforced by the server, not by the database; all owners share one database role.
- `get_document` with a file path writes on the server host, which only helps clients that can read that host's
  shared storage.
- Expiry is advisory: expired documents are hidden from listings, not removed.
