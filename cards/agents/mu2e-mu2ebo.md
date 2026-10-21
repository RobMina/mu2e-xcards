---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-mu2ebo
name: Mu2eBO (autoresearch) closed-loop Bayesian optimization of Mu2e geometry
description: >-
  Closed-loop Bayesian optimization system for Mu2e experiment design, with an MCP
  server through which AI agents check studies and run optimization campaigns. A
  study file defines the knobs (for example stopping-target foil radii,
  thicknesses, hole fractions and spacing), the geometry, the simulation and
  analysis steps and the objectives (signal over square root of background for
  muon-to-electron conversion, radiation damage from beam flash). For each
  candidate geometry it renders the geometry, runs a one-event Geant4 overlap
  check, submits a fast Geant4 simulation chain on the Fermilab grid (or
  locally, or G4beamline for the production target), scores it with the Mu2e
  analysis server and adds a row to the study's leaderboard; a Gaussian-process
  surrogate (BoTorch) then proposes the next batch. Agents can list, show and
  check studies, dry-run and launch campaigns with operator approval, follow
  them and read leaderboards. It is the optimization engine of the Mu2e Genesis
  phase 1 Run-1 optimization workflow, used for stopping-target and
  production-target studies. Runs on Fermilab Mu2e machines with the user's grid
  credentials.

science:
  - particle-physics
keywords:
  - mu2e
  - bayesian optimization
  - closed-loop optimization
  - detector optimization
  - experiment design
  - gaussian process
  - botorch
  - geant4
  - g4beamline
  - fast simulation
  - stopping target
  - production target
  - leaderboard
  - campaign
  - autoresearch
  - mcp server
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.2.0'
last_updated: '2026-10-21'
license:
  spdx_id: NOASSERTION
  name: 'No license declared in the repository'
  url: https://github.com/Mu2e/Mu2eBO
relationships:
  - type: has_part
    target: mu2e-mu2ebo-surrogate
    target_label: Mu2eBO GP surrogate MCP server
  - type: invokes
    target: mu2e-analysis-mcp
    target_label: Mu2e analysis MCP server (figures of merit)
  - type: runs_on
    target: mu2e-fermigrid
    target_label: FermiGrid for Mu2e
  - type: runs_on
    target: mu2e-uva-hpc
    target_label: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction
  - type: invokes
    target: mu2e-crv-fastreco
    target_label: Mu2e CRV fast reconstruction (through the fastsimkit kit)
  - type: invokes
    target: mu2e-mu2ebo-reporter
    target_label: Mu2eBO campaign reporting agent (report at loop exit and on request)
  - type: part_of
    target: mu2e-run1-optimization
    target_label: Mu2e Agentic Run-1 Experiment Optimization Workflow

io_contract:
  input_modes:
    - application/json
    - text/plain
  output_modes:
    - application/json
    - text/tab-separated-values
  modalities:
    - tabular
  task_tags:
    - optimization
    - experiment design
    - simulation orchestration

extension:
  kind: agent
  skills:
    - List, show and explain optimization studies (list_studies, show_study, study_guide)
    - Check a draft study end to end, including a one-event Geant4 geometry pre-check (start_check, check_result)
    - Dry-run, then with operator approval launch, a closed-loop Bayesian-optimization campaign (start_campaign)
    - Follow and stop campaigns (campaign_status, stop_campaign)
    - Read a study's leaderboard, best configurations first (leaderboard)
    - Report on a campaign automatically at loop exit, and on request mid-campaign (start_report, report)
    - Run fast Geant4 simulation chains on the Fermilab grid or locally, and G4beamline beamline jobs
    - Run the JAX CRV fast chain on an HPC GPU endpoint, one Slurm job per point (fastsimkit)
    - Optimize stopping-target and production-target geometry for muon-to-electron conversion sensitivity
  capabilities:
    streaming: false
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP stdio'
---

# Mu2eBO (autoresearch) closed-loop Bayesian optimization of Mu2e geometry

[Mu2e/Mu2eBO](https://github.com/Mu2e/Mu2eBO) ("autoresearch", Y. Oksuzian) closes the loop between a
Gaussian-process optimizer and the Mu2e simulation and analysis chain. This card is a draft written from the
repository for review by its authors.

## How it works

- **Study**: one JSON file (`mode_specs/<name>.json`) with knobs, derived parameters, geometry, kits, evaluation
  steps, objectives, constraints and a leaderboard. Every key is required and unknown keys are rejected, so a typo
  fails at load, not hours into a campaign.
- **Kits**: each step runs on a kit that speaks one contract (submit, status, results): `prodtools` (Geant4 jobs
  through Mu2e production tools, grid or local), `offline_preflight` (one-event Geant4 overlap check of the
  rendered geometry), `anakit` (the Mu2e analysis MCP server, card `mu2e-analysis-mcp`) and `beamkit`
  (G4beamline for the production target), plus `fastsimkit`, a native kit that runs the JAX fast chain (cards
  `mu2e-crv-fastsim`, `mu2e-crv-fastreco`) as one Slurm job per point on an HPC endpoint (card `mu2e-uva-hpc`);
  its first task is a throughput smoke test.
- **Fast simulation**: a study defines a short chain of Geant4 grid steps per candidate (for the stopping target:
  muon beam, conversion-electron stops and beam flash), scored by analyses on the analysis server (muon stop rate,
  energy deposition, approximate sensitivity, beam-flash radiation damage). A full dts -> digi -> reco -> ntuple
  chain (`ce_chain`) is the validation path for selected designs.
- **Leaderboard**: one TSV per study; each row is one evaluated configuration with its objectives.
- **Optimizer**: BoTorch GP with batch pickers (qNEHVI, qLogNEI, a budget-constrained sensitivity picker, hybrid);
  card `mu2e-mu2ebo-surrogate`.

## MCP tools (`autoresearch` server, `service/server.py`)

| Tool | Purpose |
|---|---|
| `list_studies`, `show_study`, `study_guide` | Browse studies and the study-writing guide |
| `start_check`, `check_result` | Check a draft exactly as the command-line checker does (loads, paths exist, launch check, geometry pre-check at the centre of the knob box) |
| `start_campaign` | Dry run by default (launch checks, exact command, job budget); launches only with `confirm=true` after the operator's OK |
| `campaign_status`, `stop_campaign` | Follow a campaign; stop launching new evaluations (running ones finish) |
| `leaderboard` | A study's evaluated configurations, best first |
| `start_report`, `report` | Ask the reporting agent (card `mu2e-mu2ebo-reporter`) for an interim campaign report and read it; a final report is started automatically at every loop exit |

The study tools submit no jobs and write no leaderboard rows; only campaigns do.

## Studies

Studies cover the Run-1A stopping target (sensitivity, with beam-flash radiation damage as a constraint or second
objective) and the production target on G4beamline. `list_studies` gives the current set, and `leaderboard` the
results; published results are in Mu2e documents (for example Mu2e-doc-58092).

## Role in the Mu2e Genesis project

The engine of steps 2-5 of the Run-1 optimization workflow (`mu2e-run1-optimization`, Mu2e-doc-57514): proposing
configurations, running simulation, scoring and refitting. The phase 1 decision gate asks for closed-loop campaigns
on at least two external-constraint scenarios within a week each, and a Run-1a configuration that beats the
manually optimized baseline.

## Access and limitations

- Runs on Fermilab Mu2e interactive machines (stdio MCP), with the operator's own Kerberos ticket and grid token;
  campaigns submit grid jobs under that identity. Launching a campaign needs the operator's approval.
- One evaluation is many grid jobs, and a campaign runs many evaluations, so campaigns are long-running.
- Fast-simulation scores must be confirmed with full simulation before a design is recommended.
- The repository declares no license; ask the authors before reuse.
