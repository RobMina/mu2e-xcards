---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-runs-mcp
name: Mu2e Run Database MCP Server (runs)
description: >-
  Read-only MCP server that gives AI agents access to the Mu2e experiment's run
  database at Fermilab: which runs were taken, when, of what run type (for
  example cosmic-ray runs for the Cosmic Ray Veto, tracker, calorimeter or
  stopping target monitor, source runs and studies), their state transitions
  (start, stop, pause, error), subruns, the run configuration and the conditions
  database tables attached to each run. Agents can look up one run, list recent
  runs filtered by run range, run type or time window, and search a subsystem's
  run configuration for a key or value without loading it whole. It is part of
  the context assembly of the Mu2e Genesis phase 1 project: in agentic data
  quality monitoring (DQM) an agent uses it to find what changed around a flagged
  run (run type, configuration, transitions, errors) when diagnosing an anomaly,
  for the Cosmic Ray Run and commissioning of the Mu2e muon-to-electron conversion
  search. Runs on the Mu2e AI node at Fermilab; access needs the Fermilab network
  and a per-user Mu2e key.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - run database
  - run log
  - run conditions
  - run configuration
  - run type
  - state transitions
  - subruns
  - conditions database
  - detector operations
  - data quality monitoring
  - dqm
  - anomaly investigation
  - cosmic ray run
  - mcp server
  - model context protocol
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '0.7.2'
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
    - tabular
  task_tags:
    - data retrieval
    - operations context

extension:
  kind: agent
  skills:
    - Look up one run with its type, start time, configuration, transitions and subruns (get_run)
    - List recent runs filtered by run range, run type or time window (list_runs)
    - Map run-type and transition-type ids to names (get_flags)
    - Summarise or search a subsystem's run configuration for a key or value (get_config_blob)
    - Show the conditions database tables attached to a run (get_dbtables, get_cidtables)
    - Find what changed around a flagged run when investigating a data quality anomaly
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# Mu2e Run Database MCP Server (runs)

A read-only Model Context Protocol (MCP) server over the Mu2e run database, built on Mu2e Offline's `runTool`.
Any MCP client (Claude Code, Codex, goose, or the Mu2e agentic DQM workflow) can use it to answer questions about
runs. Software: `mcp/runs` in [Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0). This card describes the
deployment that serves the Mu2e collaboration, version 0.7.2 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `get_run` | One run by number, optionally with configurations, transitions and subruns |
| `list_runs` | Recent runs, filtered by run range, run-type ids, time range or the last N days; most recent first, capped at 200 rows |
| `get_flags` | Run-type and transition-type id-to-name maps |
| `get_config_blob` | A subsystem's run configuration: by default only its size and top-level keys; with a query, only the matching key paths and values (at most 100) |
| `get_dbtables`, `get_cidtables` | The conditions-database tables attached to one run, mainly for debugging |
| `get_server_info` | Version and configuration |

Configuration blobs can be hundreds of kilobytes, so the server never returns one whole; it summarises or searches
instead.

## Content (2026-10-15)

Run types defined: mu2e, cosmics, cosmics_crv, cosmics_trk, cosmics_calo, cosmics_stm, cosmics_debug, lowth_crv,
study_crv and source_stm. The 200 most recent runs (125068-125267) are cosmic-ray, Cosmic Ray Veto, calorimeter and
stopping target monitor runs and studies from detector commissioning.

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: collaboration members only. It needs the Fermilab network (on site, VPN or an SSH tunnel) and a personal
  Mu2e MCP key, issued by the Mu2e AI infrastructure maintainers and sent as an HTTP bearer token.
- Read-only: `runTool` has no write mode, so the server cannot change the run database.

## Role in the Mu2e Genesis project

Context assembly for the AI-driven DQM workflow of the Mu2e Genesis phase 1 project, "Expedited Discovery by
Leveraging Agentic Workflows for the Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514). The agentic DQM
plan has the agent query the run-log and configuration databases for entries temporally correlated with a flagged
anomaly; this server is that interface, next to the DQM metrics, logbook and documentation servers.

## Limitations

- Listings are capped at 200 runs per call; narrow with a run range, type or time window.
- `get_config_blob` is slow (about 1-2 s per call, uncached) and never returns a whole blob.
- The deployment follows the current Offline development build of `runTool`, so output details can change.
