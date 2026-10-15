---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-dqm-mcp
name: Mu2e Data Quality Monitoring MCP Server (dqm)
description: >-
  Read-only MCP server that gives AI agents access to the Mu2e experiment's data
  quality monitoring (DQM) database at Fermilab: per-run, per-file and per-day
  detector and production metrics, their acceptable limits and alarm codes. Agents
  can browse monitored sources (process, stream, aggregation, version), the catalog
  of tracked metrics (for example Cosmic Ray Veto, tracker, calorimeter and
  operations quantities), and run, subrun or time intervals. They can pull a metric
  as a time series or trend across runs, with values, uncertainties and status
  codes, and compare it against its DQM limits to flag outliers and out-of-range
  values. It is the DQM interface of the Mu2e Genesis phase 1 project: the data
  source for ML anomaly detection (for example transformer and autoencoder models
  on metric timelines) and for agentic DQM, where an agent checks each new run,
  finds anomalous metrics and reports them to shifters, in the Cosmic Ray Run and
  nightly validation of the Mu2e muon-to-electron conversion search. Runs on the
  Mu2e AI node at Fermilab; reachable only from the Fermilab network.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - data quality monitoring
  - dqm
  - detector monitoring
  - anomaly detection
  - time series
  - metric timeline
  - alarm limits
  - run quality
  - cosmic ray veto
  - crv
  - nightly validation
  - mcp server
  - model context protocol
  - query engine
  - charged lepton flavor violation
  - high energy physics
sensitivity: reviewed
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
    - application/vnd.mu2e.dqm-metrics+json
  modalities:
    - tabular
    - time-series
  task_tags:
    - data retrieval
    - anomaly detection
    - time-series monitoring

extension:
  kind: agent
  skills:
    - List monitored DQM sources by process, stream, aggregation and version (list_sources, list_versions)
    - Browse the catalog of tracked metrics by detector group, subgroup and name (list_values)
    - List run, subrun or time intervals for a source (list_intervals)
    - Retrieve a metric as a time series across runs with value, uncertainty and status (query_metrics)
    - Retrieve DQM limits and alarm codes to compare measurements against thresholds (query_metrics, limits table)
    - Report the server's database, endpoint and query defaults (get_server_info)
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# Mu2e Data Quality Monitoring MCP Server (dqm)

A read-only Model Context Protocol (MCP) server over the Mu2e DQM database (`mu2e_dqm_prd`), reached through
Fermilab's Query Engine over HTTPS. Any MCP client (Claude Code, Codex, goose, or the Mu2e agentic DQM workflow) can
use it to read detector and production quality metrics. Software: `mcp/dqm` in
[Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0). This card describes the deployment that serves the
Mu2e collaboration, version 0.4.0 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `list_sources` | Monitored sources, keyed by (process, stream, aggregation, version); returns the source id |
| `list_versions` | Code versions that have reported for a process and stream |
| `list_values` | Catalog of tracked metrics, keyed by (group, subgroup, name); returns the value id |
| `list_intervals` | Run/subrun or time intervals per source |
| `query_metrics` | Measured values (`numbers`) or limits and alarm codes (`limits`) for a source and metric over intervals: a plot-ready timeline |
| `get_server_info` | Database, endpoint and query defaults |

Results are JSON tables intended for the client model to interpret, tabulate or plot. Defaults are conservative
(last 10 days, 100 rows); `query_metrics` reports whether its scan was complete, so an empty result can be told apart
from a truncated one.

## Content (2026-10-15)

- 112 sources: Cosmic Ray Veto test-stand ageing and LED runs, Cosmic Ray Veto reconstruction of the cosmic-ray
  data in the hall, nightly validation streams (simulation, reconstruction, mixing, trigger, build) and test sources.
- 118 tracked metrics across Cosmic Ray Veto, tracker, calorimeter, straw and operations groups.

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: collaboration-internal. It is reachable only from the Fermilab network (on site, VPN or an SSH tunnel);
  outside traffic is blocked by the lab firewall. No per-user key is needed today.
- Read-only: it cannot write metrics or limits; filling the database stays with the production DQM jobs.

## Role in the Mu2e Genesis project

This is the DQM interface of the Mu2e Genesis phase 1 project, "Expedited Discovery by Leveraging Agentic Workflows
for the Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514). It serves both halves of the AI-driven DQM
workflow for the Cosmic Ray Run:
- **ML anomaly detection**: metric timelines are the input for transformer (TranAD) and autoencoder models, and
  for the traditional limit-based checks they are benchmarked against;
- **agentic DQM**: an agent queries the newest intervals, compares values with their limits and with the ML anomaly
  scores, then takes each flagged metric to the documentation and logbook servers for context.

## Limitations

- Coverage is what the production DQM jobs have filled. Many detector metrics, including several Cosmic Ray Veto
  series, are still being added, and limits are missing for many metrics.
- Unscoped queries scan only the most recent rows and filter client-side; check the scan-complete flag before
  treating "no rows" as "no data".
- No authentication beyond the Fermilab network boundary.
