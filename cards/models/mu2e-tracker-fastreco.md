---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-tracker-fastreco
name: Mu2e tracker fast reconstruction (batched GPU straight-line track fit, in development)
description: >-
  Second stage of the Mu2e fast reconstruction, in development: a batched,
  vectorised re-implementation in JAX of the extracted-configuration (no
  magnetic field) straw-tracker reconstruction for GPUs (NVIDIA A100) and CPU:
  straw hit reconstruction, combo hits, time clustering, a straight-line seed
  and a KinematicLine (KinKal) track fit with drift-ambiguity resolution, as a
  fixed-iteration fit in double precision over many tracks at once. It reads
  the tracker fast simulation's steps or stock straw digis, needs no art
  framework, and writes the trk, trksegs and trkhits columns of the Mu2e
  EventNtuple, so track-to-CRV residuals come out together with the CRV fast
  reconstruction. Purpose: re-reconstruct each point of the tracker-CRV
  alignment and Monte Carlo response loop without the CPU art chain, with the
  stock Offline reconstruction as the validation reference. Status: every stage
  is ported, including a KinKal-faithful Kalman fit that runs batched on GPU;
  time clusters and seeds match the stock chain on identical hits, and the
  track fit is being compared track by track with the stock KinematicLine fit,
  not yet within the agreed thresholds.

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
version: '1.2.0'
last_updated: '2026-10-29'
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
  - type: runs_on
    target: mu2e-fnal-eaf
    target_label: Fermilab Elastic Analysis Facility

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
    Vectorised port of the extracted Offline tracker chain: straw hit reco,
    combo hits, time clustering, a JAX line seed, and fixed-iteration
    straight-line fits with masked hit states (a KinKal-faithful Kalman fit
    following the stock fit schedule with straw material, and a
    least-squares fit)
  framework: JAX (GPU and CPU), Python
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e tracker fast reconstruction (in development)

Stage 2 of the Mu2e Genesis fast reconstruction, after `mu2e-crv-fastreco`. Every stage is ported; the track fit's
validation against the stock chain is in progress.

## Chain

| Stage | Fast path | Stock reference (Offline) |
|---|---|---|
| straw hit reco | ported | `StrawHitReco` |
| combo hits | ported | `CombineStrawHits` |
| time cluster and seed | ported (seed in JAX); identical clusters and seeds on identical hits | `SimpleTimeCluster`, `LineFinder` |
| track fit | Kalman fit following KinKal's schedule with straw material, batched on GPU; a least-squares fit | `KinematicLineFit` (KinKal) |
| output columns | EventNtuple names and units | EventNtuple `trk`, `trksegs`, `trkhits` |

- **Fast digitisation:** a NumPy port of the stock straw digitisation, statistically equivalent to stock, comes with
  the tracker fast simulation (card `mu2e-tracker-fastsim`); a parametric hit model remains an option.
- **Validation against the stock chain, matched by truth particle:**
  - hits and fits on identical inputs: clusters and seeds pass; per-track fit agreement is close to, but not yet
    within, the agreed thresholds;
  - track yield, acceptance and residuals end to end;
  - the loop objective.
- An art dumper exports the stock chain's hits, clusters, seeds and fits (including the stock fit's internal state)
  for these comparisons.

## Intended use

The tracker reconstruction tier of the tracker-CRV alignment and Monte Carlo response loop of the extracted
configuration.

## Limitations

- In development and not yet validated; no Mu2eBO `fastsimkit` task uses it yet.
- No-field (straight-line) tracks only; a GPU helix fit is out of scope.
- KPP data unpacking stays in the stock chain.
- Code: [RobMina/mu2e-tracker-fastsim](https://github.com/RobMina/mu2e-tracker-fastsim) (Apache-2.0), the `tracker/` submodule of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim), building on the shared core [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core).
