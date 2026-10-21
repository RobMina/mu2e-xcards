---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-tracker-fastreco
name: Mu2e tracker fast reconstruction (batched GPU straight-line track fit, planned)
description: >-
  Planned second stage of the Mu2e fast reconstruction: a batched, vectorised
  re-implementation in JAX of the extracted-configuration (no magnetic field)
  straw-tracker reconstruction for GPUs (NVIDIA A100 on ALCF Polaris) and CPU:
  straw hit reconstruction, combo hits, time clustering, a straight-line seed
  and a KinematicLine (KinKal) track fit with drift-ambiguity resolution, as a
  fixed-iteration fit in double precision over many tracks at once. It reads
  the tracker fast simulation's steps or stock straw digis, needs no art
  framework, and writes the trk, trksegs and trkhits columns of the Mu2e
  EventNtuple, so track-to-CRV residuals come out together with the CRV fast
  reconstruction. Purpose: re-reconstruct each point of the tracker-CRV
  alignment and Monte Carlo response loop without the CPU art chain, with the
  stock Offline reconstruction as the validation reference. Status: first-draft
  plan; goals and thresholds are set once the CRV fast reconstruction works.

science:
  - particle-physics
keywords:
  - mu2e
  - straw tracker
  - track reconstruction
  - track fitting
  - fast reconstruction
  - gpu reconstruction
  - jax
  - kinkal
  - kinematic line fit
  - straight line fit
  - drift ambiguity
  - eventntuple
  - detector alignment
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
    target: mu2e-crv-fastreco
    target_label: Mu2e CRV fast reconstruction
  - type: compatible_with
    target: mu2e-tracker-fastsim
    target_label: Mu2e tracker fast simulation
  - type: compatible_with
    target: mu2e-crv-fastreco
    target_label: Mu2e CRV fast reconstruction
  - type: runs_on
    target: mu2e-alcf-polaris
    target_label: ALCF Polaris for Mu2e fast simulation and reconstruction

io_contract:
  input_modes:
    - application/x-hdf5
    - application/vnd.apache.parquet
  output_modes:
    - application/vnd.apache.parquet
    - application/json
  modalities:
    - tabular
  task_tags:
    - event reconstruction
    - track fitting
    - fast reconstruction

extension:
  kind: model
  architecture: >-
    Vectorised port (planned) of the extracted Offline tracker chain: straw hit
    reco, combo hits, time clustering, line seed and a fixed-iteration
    straight-line Kalman/least-squares fit with masked hit states
  framework: JAX (GPU and CPU), Python
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e tracker fast reconstruction (planned)

Stage 2 of the Mu2e Genesis fast reconstruction, after `mu2e-crv-fastreco`. **First-draft plan**: this card states
the intent and the interface; details follow once the CRV stage works.

## Plan in brief

| Stage | Stock reference (Offline) |
|---|---|
| straw hit reco | `StrawHitReco` |
| combo hits | `CombineStrawHits` |
| time cluster and seed | `SimpleTimeCluster`, `LineFinder` |
| track fit | `KinematicLineFit` (KinKal) |
| output columns | EventNtuple `trk`, `trksegs`, `trkhits` |

- **Fast digitisation:** either a port of the stock straw digitisation or a parametric hit model, to be decided.
- **Validation against the stock chain, matched by truth particle:**
  - hits and fits on identical inputs;
  - track yield, acceptance and residuals end to end;
  - the loop objective.

## Intended use

The tracker reconstruction tier of the tracker-CRV alignment and Monte Carlo response loop of the extracted
configuration.

## Limitations

- Not started. No-field (straight-line) tracks only; a GPU helix fit is out of scope.
- KPP data unpacking stays in the stock chain.
- Code: [RobMina/mu2e-tracker-fastsim](https://github.com/RobMina/mu2e-tracker-fastsim) (Apache-2.0), the `tracker/` submodule of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim), building on the shared core [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core).
