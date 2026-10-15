---
xCard:
  card_type: workflow
  version: '0.1'

id: mu2e-run1-optimization
name: Mu2e Agentic Run-1 Experiment Optimization Workflow
description: |-
  Closed-loop agentic simulation, analysis and optimization workflow for the Mu2e experiment at Fermilab, built by
  the Mu2e Genesis phase 1 project to maximize sensitivity to muon-to-electron conversion (R_mue) for Run-1. A
  physicist states an objective in natural language (for example, maximize sensitivity with 10 percent lower
  solenoid fields, or with half the beam intensity); the agent assembles a detector and beamline configuration (for
  example the stopping-target foil geometry), launches Geant4 and G4beamline simulation campaigns on the Fermilab
  grid and HPC (NERSC, Argonne LCRC), runs the analysis to compute figures of merit (signal over square root of
  background, radiation damage, muon stops per proton on target), uses Bayesian optimization with Gaussian-process
  surrogates for sample-efficient local search, diagnoses failed or unphysical jobs, and reports the best
  configurations with full traces. Goal: re-optimization in days instead of weeks, ten times more configurations
  evaluated, and a better Run-1a sensitivity than the manual baseline.

  Steps:
  1. A physicist gives an objective and constraints in natural language; the agent reads prior studies and Mu2e
     documentation, cards mu2e-memory-mcp and mu2e-kb-mcp.
  2. The agent (or the Bayesian-optimization surrogate, card mu2e-mu2ebo-surrogate) proposes configurations:
     geometry variants, beamline settings, pipeline stages; Mu2eBO (card mu2e-mu2ebo) checks the study.
  3. Simulation campaigns run: Geant4 fast simulation and full chain (dts, digi, reco, EventNtuple) on FermiGrid or
     HPC (cards mu2e-fermigrid, mu2e-nersc-perlmutter, mu2e-anl-lcrc), G4beamline for the beamline, after a
     one-event geometry pre-check, driven by Mu2eBO campaigns (card mu2e-mu2ebo).
  4. The analysis interface (card mu2e-analysis-mcp) computes figures of merit for each configuration and adds a
     leaderboard row; inputs and outputs can be located with card mu2e-metacat-mcp.
  5. The surrogate refits on the leaderboard and suggests the next points; the agent explores across qualitatively
     different configurations and handles failed jobs.
  6. Results, traces and lessons are written to memory and reported to the collaboration: the reporting agent (card
     mu2e-mu2ebo-reporter) writes a number-checked report at every loop exit and on request mid-campaign, with
     DocDB context, and can store it in memory (cards mu2e-memory-mcp, mu2e-kb-mcp); literature context from cards
     mu2e-inspirehep-mcp and mu2e-arxiv-mcp.

  Inputs: a study definition (parameters, geometry, simulation and analysis steps, objectives); Mu2e Offline and
  simulation software on CVMFS; grid or HPC allocations. Outputs: leaderboards of evaluated configurations with
  figures of merit, the recommended configuration, logged agent traces and token usage, and a written report.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - experiment optimization
  - detector optimization
  - bayesian optimization
  - gaussian process surrogate
  - closed-loop optimization
  - agentic workflow
  - geant4
  - g4beamline
  - simulation campaign
  - stopping target
  - sensitivity
  - figure of merit
  - campaign report
  - run-1
  - genesis mission
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.1.0'
last_updated: '2026-10-15'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-xcards/blob/main/LICENSE

datasets: []
relationships:
  - type: has_part
    target: mu2e-metacat-mcp
    target_label: Mu2e File Catalog MCP Server
  - type: has_part
    target: mu2e-memory-mcp
    target_label: Mu2e Persistent Agent Memory MCP Server
  - type: has_part
    target: mu2e-kb-mcp
    target_label: Mu2e Knowledge Base MCP Server
  - type: has_part
    target: mu2e-inspirehep-mcp
    target_label: INSPIRE-HEP Literature MCP Server
  - type: has_part
    target: mu2e-arxiv-mcp
    target_label: arXiv Paper Search MCP Server
  - type: runs_on
    target: mu2e-ai-node
    target_label: Mu2e AI Node and MCP Server Registry
  - type: runs_on
    target: mu2e-fermigrid
    target_label: FermiGrid for Mu2e
  - type: runs_on
    target: mu2e-nersc-perlmutter
    target_label: NERSC Perlmutter for Mu2e simulation
  - type: runs_on
    target: mu2e-anl-lcrc
    target_label: Argonne LCRC clusters for Mu2e simulation
  - type: has_part
    target: mu2e-mu2ebo
    target_label: Mu2eBO (autoresearch) closed-loop Bayesian optimization
  - type: has_part
    target: mu2e-mu2ebo-surrogate
    target_label: Mu2eBO Gaussian-process surrogate MCP server
  - type: has_part
    target: mu2e-analysis-mcp
    target_label: Mu2e Analysis MCP Server
  - type: has_part
    target: mu2e-mu2ebo-reporter
    target_label: Mu2eBO campaign reporting agent
  - type: based_on
    target: HEP-KE-Agent-xcard
    target_label: HEP-KE-Agent (AmSC IDA Pilot Knowledge Extraction)
---

# Mu2e Agentic Run-1 Experiment Optimization Workflow

Workflow (i) of the Mu2e Genesis phase 1 project, "Expedited Discovery by Leveraging Agentic Workflows for the
Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514, section 3.2). It replaces the manual, months-long
loop of configuring simulation and analysis chains per scenario with an agent-orchestrated closed loop. The
optimization engine is Mu2eBO ([Mu2e/Mu2eBO](https://github.com/Mu2e/Mu2eBO)), whose study definitions, contract
engine, leaderboards and two MCP servers (campaign control and surrogate) implement steps 2-5. Orchestration
follows the AmSC IDA Pilot Knowledge Extraction (HEP-KE) framework.

## Steps

| # | Step | Component | Card |
|---|---|---|---|
| 1 | State objective and constraints; read prior studies | agent; memory and knowledge-base MCP servers | `mu2e-memory-mcp`, `mu2e-kb-mcp` |
| 2 | Propose configurations | agent; Mu2eBO GP surrogate (botorch) | `mu2e-mu2ebo-surrogate`, `mu2e-mu2ebo` |
| 3 | Simulate | Mu2eBO campaign MCP and kits: Geant4 jobs via Mu2e production tools (grid or local), one-event geometry pre-check, G4beamline | `mu2e-mu2ebo` |
| 4 | Analyse and score | analysis interface (S/sqrt(B), radiation damage, stops/POT, energy deposition); file catalog | `mu2e-analysis-mcp`, `mu2e-metacat-mcp` |
| 5 | Refit and choose next points; handle failures | Mu2eBO surrogate MCP; agent | `mu2e-mu2ebo-surrogate` |
| 6 | Record, report, cite | memory and knowledge-base MCP servers; literature servers; reporting agent | `mu2e-memory-mcp`, `mu2e-kb-mcp`, `mu2e-inspirehep-mcp`, `mu2e-arxiv-mcp` |

Results of the optimization studies are reported in Mu2e documents (for example Mu2e-doc-58092), not in this card.

## Inputs

- A study definition: parameters, geometry, simulation kits and analysis steps, objectives.
- Mu2e Offline, simulation and analysis software from CVMFS; grid (FermiGrid) and HPC (NERSC, Argonne LCRC)
  allocations.

## Outputs

- A leaderboard per study: each evaluated configuration with its figures of merit.
- The recommended configuration, documented for collaboration review.
- Logged agent reasoning traces, tool calls and token usage.
- A written report and the lessons stored for later campaigns.

## How success is measured (6-month decision gate)

- The closed loop (agent-orchestrated search with local Bayesian optimization) demonstrated on at least two
  distinct external-constraint scenarios (for example half beam intensity, 10 % lower fields), each started from a
  natural-language prompt and finished within one week, with full traces logged.
- For a Run-1a scenario, an agent-produced configuration improves R_mue sensitivity over the collaboration's
  manually optimized baseline, documented for review.

## Caveats

- The Mu2eBO and analysis-server cards are drafts pending review by their authors (Y. Oksuzian, M. MacKenzie).
- A global surrogate over Mu2e's whole configuration space is out of scope for phase 1.
- Fast-simulation figures of merit must be confirmed with full simulation before a configuration is recommended.
