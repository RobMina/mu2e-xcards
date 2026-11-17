---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-fastsim-mcp
name: Mu2e fast simulation MCP server (mu2e-fastsim)
description: >-
  MCP server that lets an AI agent run the Mu2e Geant4-free GPU fast simulation
  as a tool. An agent can list the fast-simulation workflows (muon beam to the
  stopping target, conversion electrons to the tracker and calorimeter, the CRV
  cosmic chain, the stock-format EdepAna and EventNtuple writers), read which
  physics approximations each workflow makes and how to switch them to the
  stock-equivalent level, and evaluate one detector design point: a stopping-target
  geometry (foil radii, thicknesses, spacing, holes) or a CRV chain point is
  validated, rendered and submitted asynchronously as batch jobs on an HPC
  endpoint, in float32 and float64. The agent follows the jobs, fetches the
  metrics and output files (stopped muons, calorimeter energy deposition, an
  EdepAna ROOT file) and gets the exact call that scores them with the Mu2e
  analysis MCP server (approximate conversion-electron sensitivity, signal over
  square root of background). GPU work is sized first and needs explicit
  approval within a site budget cap; CPU design points run directly. Requests are
  idempotent per design-point name and can be cancelled. Built for agent-driven
  detector design optimization in the Mu2e Genesis phase 1 Run-1 optimization
  workflow, beside the Mu2eBO optimizer.

science:
  - particle-physics
keywords:
  - mu2e
  - fast simulation
  - mcp server
  - simulation as a tool
  - design point evaluation
  - stopping target
  - muon beam
  - conversion electron
  - cosmic ray veto
  - gpu simulation
  - jax
  - approximations
  - slurm
  - edepana
  - detector optimization
  - genesis mission
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.0'
last_updated: '2026-11-17'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-fastsim
relationships:
  - type: invokes
    target: mu2e-beam-fastsim
    target_label: Mu2e muon-beam and conversion-electron fast simulation
  - type: invokes
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation
  - type: invokes
    target: mu2e-crv-fastreco
    target_label: Mu2e CRV fast reconstruction
  - type: compatible_with
    target: mu2e-analysis-mcp
    target_label: Mu2e analysis MCP server (scores the fetched outputs)
  - type: compatible_with
    target: mu2e-mu2ebo
    target_label: Mu2eBO closed-loop Bayesian optimization (same kit underneath)
  - type: runs_on
    target: mu2e-uva-hpc
    target_label: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-fnal-eaf
    target_label: Fermilab Elastic Analysis Facility
  - type: part_of
    target: mu2e-run1-optimization
    target_label: Mu2e Agentic Run-1 Experiment Optimization Workflow

io_contract:
  input_modes:
    - application/json
  output_modes:
    - application/json
    - application/x-root
  modalities:
    - tabular
    - simulation
  task_tags:
    - fast simulation
    - design point evaluation
    - simulation orchestration
    - detector optimization

extension:
  kind: agent
  skills:
    - List the fast-simulation workflows with their input and output boundaries, packages, command-line tools and kit tasks (list_workflows)
    - Explain the physics approximations of a workflow or preset, their fast and fidelity levels and the stock alternative (describe_approximations)
    - Evaluate a stopping-target design point from an overlay of foil radii, thicknesses, spacing and holes, asynchronously, in float32 and float64 (run_design_point)
    - Run a CRV cosmic fast-chain point on GPU sub-jobs (run_crv_chain)
    - Follow the batch jobs of a design point (job_status)
    - Fetch metrics, energy-deposition summaries and the EdepAna ROOT file, with the analysis-server call that scores them (fetch_outputs)
    - Cancel a design point (cancel_design_point)
    - Size GPU work first and submit it only with approval inside a site GPU-hour cap
  capabilities:
    streaming: false
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP stdio'
---

# Mu2e fast simulation MCP server (mu2e-fastsim)

The `fastsim-mcp/` package of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim) (Apache-2.0) exposes
the Mu2e fast simulation to agents. It is a thin layer over the same `fastsimkit` kit that Mu2eBO uses (card
`mu2e-mu2ebo`), so an agent and the optimizer evaluate a design point in exactly the same way. It is under review in
the repository and not yet on its main branch.

## How it works

- **Discovery.** `list_workflows` and `describe_approximations` read the repository's own workflow and approximation
  tables, so an agent can see what a fast workflow replaces in the stock chain, which approximations it makes, and
  how to select the stock-equivalent level.
- **One design point.** `run_design_point` takes a stopping-target overlay (or a full geometry), checks it with the
  kit's own geometry validator, renders the simulation configuration and submits CPU or GPU batch jobs. It returns
  the job handles at once; the call is idempotent per point name.
- **Follow and fetch.** `job_status` reports the scheduler state; `fetch_outputs` returns the metrics, the
  energy-deposition summary and the EdepAna ROOT file, plus the exact `run_analysis` call of the Mu2e analysis
  server (card `mu2e-analysis-mcp`) that turns them into an approximate conversion-electron sensitivity.
- **GPU guard.** A GPU request is first answered with a sized estimate and `needs_approval`; it is submitted only on
  a repeat that allows it, inside a site GPU-hour cap (GPU off when no cap is set), after the kit has checked every
  job. A per-job budget limit in the kit applies on top.

## Access and limitations

- The server runs on the operator's machine as a kit host; compute runs on an HPC endpoint the operator can reach
  (Slurm over SSH, or the Fermilab Elastic Analysis Facility). Mu2e-internal inputs are streamed into each job and
  deleted afterwards, so the operator needs Mu2e access and an account on the endpoint.
- Float32 and float64 are both offered for the beam workflows; the CRV chain runs in float32 only through the kit.
- Fast results are approximations: confirm a selected design with the stock simulation before using it.
- The code is open source; the inputs and the results are Mu2e-internal.
