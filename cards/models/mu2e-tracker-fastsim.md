---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-tracker-fastsim
name: Mu2e tracker fast simulation (Geant4-free straw-tracker cosmic simulation, planned)
description: >-
  Planned second stage of the Mu2e Geant4-free fast simulation: cosmic-ray muons
  in the Mu2e straw tracker for the extracted (KPP) configuration at Fermilab,
  with no magnetic field. It extends the CRV fast simulation's straight-line
  muon transport to crossings of the straw gas, with thin-absorber energy-loss
  sampling, and writes a table with the content of the Offline StrawGasStep
  collection, so the stock straw digitisation, track reconstruction and
  EventNtuple run on it unchanged for validation. One fast event carries both
  tracker and CRV steps from the same primaries. Straw positions come from the
  Offline geometry, so a tracker panel or plane move is a parameter change.
  Purpose: resimulate displaced tracker and CRV geometries for the tracker-CRV
  alignment loop and its Monte Carlo response tuning without Geant4. GPU-ready
  JAX code on ALCF Polaris and CPU. Status: first-draft plan; scope, goals and
  validation thresholds are set once the CRV stage is validated.

science:
  - particle-physics
keywords:
  - mu2e
  - straw tracker
  - tracker simulation
  - fast simulation
  - geant4 replacement
  - gpu simulation
  - jax
  - cosmic ray muons
  - muon transport
  - strawgasstep
  - detector alignment
  - kpp extracted configuration
  - alcf polaris
  - high energy physics
  - genesis mission
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.1.0'
last_updated: '2026-10-16'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-tracker-fastsim
relationships:
  - type: based_on
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation
  - type: requires
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation
  - type: runs_on
    target: mu2e-alcf-polaris
    target_label: ALCF Polaris for Mu2e fast simulation and reconstruction

io_contract:
  input_modes:
    - application/x-hdf5
  output_modes:
    - application/x-hdf5
    - application/vnd.apache.parquet
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
    Physics-based fast simulation (planned): the CRV stage's straight-line
    transport extended to straw-gas crossings, with energy-loss sampling in
    thin gas and straw-wall scattering; secondaries possibly from a
    Geant4-built library
  framework: JAX (GPU and CPU), Python
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e tracker fast simulation (planned)

Stage 2 of the Mu2e Genesis fast simulation, after `mu2e-crv-fastsim`. **First-draft plan**: this card states the
intent and the interface; details follow once the CRV stage passes its validation.

## Plan in brief

- **Interface:** a StrawGasStep table, read into the stock Offline chain by a small art module (validation path A).
  The stock straw digitisation is the reference.
- **Primaries and transport:** shared with the CRV stage, so tracker and CRV steps of one event come from the same
  muon.
- **Generator filter:** tracker AND CRV, as in the production cosmic samples.
- **Validation against Geant4 on the same primaries:**
  - straw geometry;
  - crossings and ionisation per straw;
  - hit distributions;
  - track yield and track-to-CRV residuals in all CRV sectors, matched by truth particle.

## Intended use

Displaced-geometry simulation and per-iteration resimulation in the tracker-CRV alignment and Monte Carlo response
loop of the extracted configuration.

## Limitations

- Not started. Extracted (no field) configuration only; field-on transport is out of scope.
- Code: [RobMina/mu2e-tracker-fastsim](https://github.com/RobMina/mu2e-tracker-fastsim) (Apache-2.0), the `tracker/` submodule of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim), building on the shared core [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core).
