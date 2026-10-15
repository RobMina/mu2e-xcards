---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-ecl-mcp
name: Mu2e Electronic Logbook MCP Server (ecl)
description: >-
  Read-only MCP server that gives AI agents search and retrieval over the Mu2e
  experiment's Fermilab Electronic Collaboration Logbook (ECL): shift logs, run
  log entries, detector notes (Cosmic Ray Veto, calorimeter, tracker, extinction
  monitor, muon beamline), cryogenics and controls, safety and global run
  entries. Agents can search entries by category, tag, form, author, time window
  or text, fetch a full entry, and list the logbook's categories, tags and forms.
  It is part of the context assembly of the Mu2e Genesis phase 1 project: in
  agentic data quality monitoring (DQM) an agent searches shift and expert logbook
  entries made around a flagged run or metric, to find what operators saw or
  changed and to diagnose the root cause of a detector anomaly, for the Cosmic Ray
  Run and commissioning of the Mu2e muon-to-electron conversion search. Runs on the
  Mu2e AI node at Fermilab; access needs the Fermilab network and a per-user Mu2e
  key.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - electronic logbook
  - ecl
  - elog
  - shift log
  - shifter logbook
  - run log
  - operations log
  - detector operations
  - data quality monitoring
  - dqm
  - anomaly investigation
  - root cause diagnosis
  - commissioning
  - mcp server
  - model context protocol
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.0'
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
    - document retrieval
    - operations context

extension:
  kind: agent
  skills:
    - Search logbook entries by category, tag, form, author, time window or text (ecl_search_entries)
    - Count or page through matching entries cheaply by id (ecl_search_entry_ids)
    - Fetch the full text and fields of one logbook entry (ecl_get_entry)
    - List the logbook's categories, tags and forms (ecl_list_categories, ecl_list_tags, ecl_list_forms)
    - Find shift and expert logbook entries made around a flagged run or data quality anomaly
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# Mu2e Electronic Logbook MCP Server (ecl)

A read-only Model Context Protocol (MCP) server over the Mu2e instance of the Fermilab Electronic Collaboration
Logbook (ECL). Any MCP client (Claude Code, Codex, goose, or the Mu2e agentic DQM workflow) can use it to search and
read logbook entries. Software: `mcp/ecl` in [Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0), reusing
the ECL protocol code of [Mu2e/ecl-api](https://github.com/Mu2e/ecl-api) (MIT). This card describes the deployment
that serves the Mu2e collaboration.

## What it does

| Tool | Purpose |
|---|---|
| `ecl_search_entries` | Entries matching category, tag, form, author, time window (`after`/`before`, relative or absolute), indexed words or a substring; returns author, subject, category, timestamp, tags, text and form fields |
| `ecl_search_entry_ids` | Same filters, ids only, for counting and paging |
| `ecl_get_entry` | One entry in full |
| `ecl_list_categories`, `ecl_list_tags`, `ecl_list_forms` | The logbook's vocabulary, for building filters |
| `get_server_info` | Version, read-only state and auth mode |

## Content

The Mu2e logbook categories, for example Shift, Runlog, Global Run, CRV, Calorimeter, Extinction Monitor, Muon
beamline, Cryogenics and controls, Facilities, Planning and Safety; `ecl_list_categories` gives the current list.

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: collaboration members only. It needs the Fermilab network (on site, VPN or an SSH tunnel) and a personal
  Mu2e MCP key, issued by the Mu2e AI infrastructure maintainers and sent as an HTTP bearer token.
- Read-only: this deployment does not register the optional posting tool, so agents cannot write to the logbook.

## Role in the Mu2e Genesis project

Context assembly for the AI-driven DQM workflow of the Mu2e Genesis phase 1 project, "Expedited Discovery by
Leveraging Agentic Workflows for the Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514). For each flagged
anomaly the agent queries the electronic logbook and shifter logs for entries close in time to the anomaly and for
earlier precedents; this server is that interface, next to the DQM metrics, run database and documentation servers.

## Limitations

- Substring search is unindexed and slow; prefer `words` for full-text search.
- Category, tag and form lists are sampled from recent entries, so a rarely used value can be missing.
- Logbook text is free-form and written in the moment; it can be incomplete or wrong. Use it as context, not as a
  record of decisions.
