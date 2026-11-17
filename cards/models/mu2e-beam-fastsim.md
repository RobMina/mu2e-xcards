---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-beam-fastsim
name: Mu2e muon-beam and conversion-electron fast simulation (Geant4-free, GPU)
description: >-
  GPU fast simulation that evaluates a Mu2e stopping-target geometry without
  Geant4: the muon beam and the signal electrons, in JAX on GPU with NumPy twins
  on CPU. It transports muons and pions from the
  transport-solenoid entrance through the transport and detector solenoids to the
  stopping target and records where they stop (stop fraction and stop profile),
  then generates conversion electrons, decay-in-orbit and radiative pion capture
  electrons from those stops and carries them to the tracker and calorimeter
  entrance, with energy loss and multiple scattering matched to Geant4. It writes
  the stock analysis formats (EdepAna ROOT files, EventNtuple-style tables), so the
  Mu2e analysis server scores a fast design point exactly like a stock one. Its
  purpose is to evaluate a candidate stopping-target geometry (foil radii,
  thicknesses, spacing) or beamline design cheaply in Bayesian optimization (Mu2eBO), with the stock Geant4 chain kept to
  confirm selected designs. Every workflow has switchable approximations with a
  stock-equivalent level, runs in float32 and float64, and is validated against
  held-out Geant4 and stock Offline samples in the Offline validation
  histograms. Open source (Apache-2.0) at github.com/RobMina/mu2e-fastsim,
  directory beam/.

science:
  - particle-physics
keywords:
  - mu2e
  - fast simulation
  - geant4-free
  - gpu simulation
  - jax
  - muon beam
  - muon stopping target
  - stopping target design
  - stopping target geometry
  - gpu fast simulation
  - design point evaluation
  - stopped muons
  - conversion electron
  - decay in orbit
  - energy loss
  - surrogate simulation
  - bayesian optimization
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.2'
last_updated: '2026-11-17'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-fastsim/tree/main/beam
relationships:
  - type: runs_on
    target: mu2e-uva-hpc
    target_label: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-fnal-eaf
    target_label: Fermilab Elastic Analysis Facility
  - type: compatible_with
    target: mu2e-analysis-mcp
    target_label: Mu2e analysis MCP server (scores the EdepAna output)
  - type: part_of
    target: mu2e-run1-optimization
    target_label: Mu2e Agentic Run-1 Experiment Optimization Workflow

io_contract:
  input_modes:
    - application/json
    - application/x-root
  output_modes:
    - application/x-root
    - application/json
  modalities:
    - tabular
    - simulation
  task_tags:
    - fast simulation
    - detector simulation
    - surrogate simulation

extension:
  kind: model
  architecture: >-
    Physics-based Monte Carlo transport (not a trained network): Geant4-matched
    energy loss, multiple scattering and stopping in the solenoid field and
    stopping-target material, vectorised over particles on the device.
  framework: JAX (GPU and CPU), NumPy
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e muon-beam and conversion-electron fast simulation

The `beam/` package (`beamfastsim`) of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim) (Apache-2.0)
replaces the Geant4 stages of the Mu2e beam and signal chain that a stopping-target design changes. It is not a
trained model: it is physics transport written for the GPU, checked stage by stage against Geant4 and stock Offline.

## What it covers

- **Muon beam to stops.** Muons and pions from stock transport-solenoid states through the transport and detector
  solenoids to the stopping target; stop fraction and stop profile per foil.
- **Electrons from stops.** Conversion electrons, decay-in-orbit and radiative pion capture electrons generated at
  the stops and carried to the tracker and calorimeter entrance.
- **Stock formats.** EdepAna ROOT files and EventNtuple-style tables, read by the Mu2e analysis server (card
  `mu2e-analysis-mcp`) without changes.
- **Approximations.** Each workflow lists its approximations, their fast and fidelity levels and the stock
  alternative (`docs/approximations.md`; `--approx-preset default|fast|fidelity`).

## How it is used

- In Mu2eBO (card `mu2e-mu2ebo`) through the `fastsimkit` kit, on a fork branch: one stopping-target design point
  becomes a batch job on an HPC endpoint.
- By agents through the fast-simulation MCP server (card `mu2e-fastsim-mcp`).

## Validation and limits

- Validated against held-out Geant4 and stock Offline samples: stop fractions on nominal and multi-foil targets,
  electron yields at the tracker entrance, and the Offline validation histograms; float32 and float64 both. Current
  values, samples and thresholds are in the repository's `docs/validation.md` and `docs/performance.md`; open items
  in `docs/limitations.md`.
- The inputs (stock beam states, conditions, tables) are Mu2e-internal; Mu2e members request the input release
  described in the repository. Results are Mu2e results and are not published through this card.
- A selected design must be confirmed with the stock Geant4 chain.
