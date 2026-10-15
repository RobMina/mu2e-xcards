---
xCard:
  card_type: workflow
  version: '0.1'

id: mu2e-agentic-dqm
name: Mu2e AI-Driven Data Quality Monitoring Workflow (Cosmic Ray Run)
description: |-
  End-to-end AI-driven data quality monitoring (DQM) workflow for the Mu2e experiment at Fermilab, planned for the
  Cosmic Ray Run by the Mu2e Genesis phase 1 project. After the offline DQM pipeline processes each run, machine
  learning anomaly detection scores the detector metrics, and an AI agent investigates every flagged anomaly: it
  pulls the metric history and limits, assembles context from the electronic logbook, shift logs, run database,
  run configuration and collaboration documentation, and writes a structured summary with links to the sources for
  the DQM shifter, escalating anomalies it cannot explain and suggesting diagnostic actions. Goal: every Cosmic Ray
  Run dataset investigated, and anomaly context assembled in minutes instead of hours, compared against traditional
  limit-based DQM on the same data.

  Steps:
  1. Offline DQM production fills the DQM database with per-run detector metrics (Cosmic Ray Veto first), card
     mu2e-dqm-mcp to read them.
  2. ML anomaly detection (transformer TranAD and autoencoder models from the Hardware-Aware AI toolkit) scores
     metric timelines and histograms, trained on GPUs at the Elastic Analysis Facility (card mu2e-fnal-eaf);
     traditional limit checks and chi-square tests run as the baseline. No model card yet.
  3. The agent compares each new run's metrics with their limits and anomaly scores and flags anomalies, card
     mu2e-dqm-mcp.
  4. For each flagged anomaly the agent gathers temporally correlated context: logbook and shift entries (card
     mu2e-ecl-mcp), run type, configuration and transitions (card mu2e-runs-mcp), and prior occurrences and expert
     notes in DocDB (card mu2e-kb-mcp); input data can be located with card mu2e-metacat-mcp.
  5. The agent writes a structured summary with source links for the shifter, keeps running notes across shifts
     (card mu2e-memory-mcp), and escalates unresolved anomalies with suggested diagnostic actions.
  6. Shifters rate the summaries; the feedback and the injected-anomaly benchmark measure the AI advantage.

  Inputs: Cosmic Ray Run data processed by the offline DQM pipeline; DQM database metrics and limits; access to the
  Mu2e MCP servers on the Fermilab network (Mu2e collaboration key for logbook, run database and documentation).
  Outputs: anomaly scores per run and metric; one structured, source-linked summary per flagged anomaly; escalations;
  shifter ratings.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - data quality monitoring
  - dqm
  - agentic workflow
  - anomaly detection
  - anomaly investigation
  - root cause diagnosis
  - shift assistant
  - context assembly
  - detector operations
  - cosmic ray run
  - cosmic ray veto
  - tranad
  - autoencoder
  - genesis mission
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '0.1.0'
last_updated: '2026-10-15'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-xcards/blob/main/LICENSE

datasets: []
relationships:
  - type: has_part
    target: mu2e-dqm-mcp
    target_label: Mu2e Data Quality Monitoring MCP Server
  - type: has_part
    target: mu2e-ecl-mcp
    target_label: Mu2e Electronic Logbook MCP Server
  - type: has_part
    target: mu2e-runs-mcp
    target_label: Mu2e Run Database MCP Server
  - type: has_part
    target: mu2e-kb-mcp
    target_label: Mu2e Knowledge Base MCP Server
  - type: has_part
    target: mu2e-memory-mcp
    target_label: Mu2e Persistent Agent Memory MCP Server
  - type: has_part
    target: mu2e-metacat-mcp
    target_label: Mu2e File Catalog MCP Server
  - type: runs_on
    target: mu2e-ai-node
    target_label: Mu2e AI Node and MCP Server Registry
  - type: runs_on
    target: mu2e-fermigrid
    target_label: FermiGrid for Mu2e
  - type: runs_on
    target: mu2e-fnal-eaf
    target_label: Fermilab Elastic Analysis Facility for Mu2e
  - type: based_on
    target: HEP-KE-Agent-xcard
    target_label: HEP-KE-Agent (AmSC IDA Pilot Knowledge Extraction)
---

# Mu2e AI-Driven Data Quality Monitoring Workflow (Cosmic Ray Run)

Workflow (ii) of the Mu2e Genesis phase 1 project, "Expedited Discovery by Leveraging Agentic Workflows for the
Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514, section 3.3). It combines machine-learning anomaly
detection with agentic context assembly into one DQM pipeline for the Cosmic Ray Run. Orchestration follows the
AmSC IDA Pilot Knowledge Extraction (HEP-KE) framework; anomaly detection builds on the Hardware-Aware AI (HAAI)
data-quality toolkit.

## Steps

| # | Step | Component | Card | Status (2026-10-15) |
|---|---|---|---|---|
| 1 | Fill the DQM database with per-run metrics | Offline DQM production; DQM MCP server for reads | `mu2e-dqm-mcp` | running; CRV metrics being extended |
| 2 | Score metrics for anomalies; run the traditional baseline | TranAD / autoencoder (HAAI toolkit); limits, chi-square and pulls vs references | none yet | prototype on CRV timelines |
| 3 | Flag anomalies per run | agent + DQM MCP server | `mu2e-dqm-mcp` | MCP server in production; agent planned |
| 4 | Assemble context for each anomaly | ECL logbook, run database, DocDB knowledge base, file catalog MCP servers | `mu2e-ecl-mcp`, `mu2e-runs-mcp`, `mu2e-kb-mcp`, `mu2e-metacat-mcp` | MCP servers in production |
| 5 | Summarise for the shifter, keep notes, escalate | agent; memory MCP server | `mu2e-memory-mcp` | planned |
| 6 | Collect shifter feedback; benchmark on injected anomalies | feedback mechanism; validation set | none yet | planned |

## Inputs

- Cosmic Ray Run data, processed by the offline DQM pipeline into DQM histograms and per-run metrics.
- The DQM database (`mu2e_dqm_prd`) with metric values and limits.
- Network access to the Mu2e MCP servers at Fermilab; a Mu2e collaboration key for the logbook, run database,
  documentation and memory servers.

## Outputs

- Anomaly scores per run and metric.
- For each flagged anomaly, a structured summary with links to the logbook entries, runs and documents used.
- Escalations with suggested diagnostic actions.
- Shifter ratings and comments, collected over the evaluation window.

## How success is measured (6-month decision gate)

- ML scoring and agentic context assembly applied to all valid Cosmic Ray Run datasets in the evaluation window,
  with a summary for every flagged anomaly.
- The ML detector characterised on an injected-anomaly validation set: signal efficiency at representative false
  positive rates, compared with non-ML baselines.
- Shifter feedback collected over at least two weeks of Cosmic Ray Run shifts, with ratings and comments.

## Caveats

- This card describes the planned workflow; steps 2, 5 and 6 are not deployed yet and have no cards.
- It depends on the Cosmic Ray Run schedule and on the DQM database coverage of the detector metrics.
- The agent assists shifters; decisions on data quality stay with people.
