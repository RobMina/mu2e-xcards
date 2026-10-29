---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-tracker-fastsim
name: Mu2e tracker fast simulation (Geant4-free straw-tracker cosmic simulation, in development)
description: >-
  Second stage of the Mu2e Geant4-free fast simulation, in development:
  cosmic-ray muons in the Mu2e straw tracker for the extracted (KPP)
  configuration at Fermilab, with no magnetic field. It extends the CRV fast
  simulation's straight-line muon transport through the tracker, with the
  materials of the Offline GDML export, multiple scattering in the tracker
  interior and straw walls, energy-loss sampling in the straw gas and a
  Geant4-built library of secondaries, and transports every muon of
  multi-muon cosmic events. It writes a table with the content of the Offline
  StrawGasStep collection, which a small art module turns into the stock
  collection, so the stock straw digitisation, track reconstruction and
  EventNtuple run on it unchanged for validation. A NumPy port of the stock
  straw digitisation, statistically equivalent to it on the same steps, feeds
  the tracker fast reconstruction directly. One fast event carries both
  tracker and CRV steps from the same primaries. Straw positions come from the
  Offline geometry, so a tracker panel or plane move is a parameter change.
  Purpose: resimulate displaced tracker and CRV geometries for the tracker-CRV
  alignment loop and its Monte Carlo response tuning without Geant4. NumPy and
  JAX backends (GPU and CPU). Status: validated level by level against Geant4
  on the same primaries; the ionisation and track-yield checks are still open.

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
version: '1.2.0'
last_updated: '2026-10-29'
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
    Physics-based fast simulation: the CRV stage's straight-line transport
    extended through the tracker interior (GDML materials, banded multiple
    scattering with a single-scattering tail, kinks at thick supports) to
    straw-gas crossings, with energy-loss sampling in thin gas, straw-wall
    scattering and secondaries from a Geant4-built library
  framework: JAX (GPU and CPU), Python
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e tracker fast simulation (in development)

Stage 2 of the Mu2e Genesis fast simulation, after `mu2e-crv-fastsim`. The code runs end to end into the stock
chain; validation against Geant4 is in progress.

## How it works

- **Interface:** a StrawGasStep table, read into the stock Offline chain by a small art module (validation path A).
  The stock straw digitisation is the reference.
- **Fast digitisation:** a NumPy port of the stock straw digitisation (no JAX version yet), statistically
  equivalent to stock on the same StrawGasSteps; it writes digis in the format the fast hit reconstruction reads
  (card `mu2e-tracker-fastreco`).
- **Primaries and transport:** shared with the CRV stage, so tracker and CRV steps of one event come from the same
  muons. Every muon of a multi-muon cosmic event is transported.
- **Tracker interior:** materials from the Offline GDML export, the calorimeter as convex pieces, thick supports
  split into scattering kinks.
- **Secondaries:** sampled from a library built with Geant4, in the straw and off axis.
- **Generator filter:** tracker AND CRV, as in the production cosmic samples.
- **Backends:** NumPy (reference, with per-component diagnostic ledgers) and JAX (GPU and CPU).

## Validation against Geant4 on the same primaries

- straw geometry;
- crossings and ionisation per straw;
- hit distributions;
- track yield and track-to-CRV residuals in all CRV sectors, matched by truth particle.

Straw geometry and the primary-muon crossing checks pass; the per-straw ionisation and the reconstructed track yield
are close to Geant4 but not yet within the agreed thresholds. Results are reported in Mu2e documents, not in this
card.

## Intended use

Displaced-geometry simulation and per-iteration resimulation in the tracker-CRV alignment and Monte Carlo response
loop of the extracted configuration.

## Limitations

- In development and not yet validated; no Mu2eBO `fastsimkit` task uses it yet.
- Extracted (no field) configuration only; field-on transport is out of scope.
- Code: [RobMina/mu2e-tracker-fastsim](https://github.com/RobMina/mu2e-tracker-fastsim) (Apache-2.0), the `tracker/` submodule of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim), building on the shared core [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core).
