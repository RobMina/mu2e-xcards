---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-analysis-mcp
name: Mu2e Analysis MCP Server (figures of merit for optimization, anakit)
description: >-
  MCP server that exposes Mu2e physics analyses as agent tools: an agent lists the
  available analyses, then runs one over Mu2e art files (a mu2e job with the
  analysis' FHiCL configuration) or over a ROOT file or EventNtuple, and gets its
  metrics back. Analyses include energy deposition in the tracker and
  calorimeter, event counts, muon stopping rate per proton on target, muon stops
  per material, approximate conversion-electron sensitivity (signal over square
  root of background), trigger efficiency, rate and timing, trigger efficiency
  from EventNtuples, and full-simulation sensitivity analyses. Inputs can be
  files, SAM definitions or MetaCat datasets. It is the Analysis interface of the
  Mu2e Genesis phase 1 project: Mu2eBO calls it to score every simulated
  configuration in the Run-1 optimization workflow (fast-simulation figures of
  merit), and its full-simulation analyses validate selected designs. Runs on
  Fermilab Mu2e machines with Mu2e Offline.

science:
  - particle-physics
keywords:
  - mu2e
  - physics analysis
  - figure of merit
  - sensitivity
  - signal over background
  - muon stopping rate
  - energy deposition
  - radiation damage
  - trigger efficiency
  - fast simulation
  - full simulation
  - eventntuple
  - fhicl
  - art
  - mcp server
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '0.1.0'
last_updated: '2026-10-15'
license:
  spdx_id: NOASSERTION
  name: 'No license declared in the repository'
  url: https://github.com/michaelmackenzie/analysis-mcp-server
relationships:
  - type: part_of
    target: mu2e-run1-optimization
    target_label: Mu2e Agentic Run-1 Experiment Optimization Workflow

io_contract:
  input_modes:
    - application/json
    - application/vnd.mu2e.art+root
    - application/vnd.mu2e.eventntuple+root
    - application/x-root
  output_modes:
    - application/json
  modalities:
    - tabular
  task_tags:
    - physics analysis
    - scoring

extension:
  kind: agent
  skills:
    - List the available Mu2e analyses with their inputs, parameters and metrics (list_analyses)
    - Run an analysis over art files, a file list, a SAM definition or a MetaCat dataset and return metrics (run_analysis)
    - Compute muon stopping rate per proton on target and muon stops per material
    - Compute energy deposition in tracker and calorimeter, including beam-flash radiation damage
    - Estimate approximate conversion-electron sensitivity (signal over square root of background)
    - Measure trigger efficiency, rate and processing time, also from EventNtuples
  capabilities:
    streaming: false
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP stdio'
---

# Mu2e Analysis MCP Server (figures of merit for optimization, anakit)

[michaelmackenzie/analysis-mcp-server](https://github.com/michaelmackenzie/analysis-mcp-server) (M. MacKenzie;
version 0.1.0, main at `232239f`, 2026-10-14), called `anakit` inside Mu2eBO. Its design: the science code is an
ordinary Python package, and a generic wrapper publishes the functions it lists as MCP tools, following the HEP-KE
`spectra-mcp-server` pattern. This card is a draft written from the repository for review by its author.

## What it does

| Tool | Purpose |
|---|---|
| `list_analyses` | The catalogue: each analysis with its input kind (art files or ROOT file), parameters and metrics |
| `run_analysis` | Run one analysis over a file, a file list, a SAM definition or a MetaCat dataset (optionally capped in files and events) and return its metrics |

Analyses: `edep`, `count`, `muon_stop_rate`, `stop_materials`, `approx_ce_sensitivity`, `trigger_efficiency`,
`trigger_rate`, `trigger_timing`, `trigger_efficiency_ntuple`, plus full-simulation sensitivity analyses
(S. Middleton). Mu2e Offline comes from a work area, a Musing or a tarball.

## Role in the Mu2e Genesis project

The Analysis interface of phase 1 (Mu2e-doc-57514): in the Run-1 optimization workflow (`mu2e-run1-optimization`)
Mu2eBO (`mu2e-mu2ebo`) calls it for every evaluated configuration. In the stopping-target study four analyses
score each design: muon stop rate, conversion-electron energy deposition, approximate sensitivity (using the stop
rate) and beam-flash energy deposition (the radiation-damage objective).

## Access and limitations

- Runs as a stdio MCP server on Fermilab Mu2e machines with Mu2e Offline available; one analysis runs at a time
  per server, synchronously.
- The approximate sensitivity is a fast figure of merit for ranking designs, not the collaboration's sensitivity
  analysis.
- The repository declares no license; ask the author before reuse.
