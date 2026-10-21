---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-crv-fastreco
name: Mu2e CRV fast reconstruction (batched GPU pulse fit and coincidence finder)
description: >-
  Batched, vectorised re-implementation in JAX of the Mu2e Cosmic Ray Veto (CRV)
  reconstruction chain, for GPUs (NVIDIA A100 on ALCF Polaris) and CPU: SiPM
  waveform generation and digitisation, pulse finding with a Gumbel pulse fit
  (fixed-iteration Levenberg-Marquardt in double precision, vmapped over all
  waveforms, subtract-and-repeat for secondary pulses), and the per-sector
  coincidence finder and clustering. It reads the CRV fast simulation's output
  directly, needs no art framework and no conditions database (text-file
  conditions), and writes the same crvpulses and crvcoincs columns as the Mu2e
  EventNtuple. A direct charge-to-pulse model is prototyped alongside the
  waveform path. Purpose: one Bayesian-optimization point of the CRV response
  tuning loop (resimulate and re-reconstruct on cached events) in minutes on one
  GPU node instead of hours of CPU, with the stock Offline reconstruction as the
  validation reference. Validated against the stock reconstruction on Monte
  Carlo and KPP cosmic data (identical coincidences, matching pulses) on
  NVIDIA A100 and B200 and on CPU; callable from the Mu2eBO optimizer through
  the fastsimkit kit. A CPU version of the faster pulse fit is proposed for
  Offline.
  Open source (Apache-2.0) in github.com/RobMina/mu2e-crv-fastsim (the crv/
  submodule of github.com/RobMina/mu2e-fastsim), package crvfastsim.reco.

science:
  - particle-physics
keywords:
  - mu2e
  - cosmic ray veto
  - crv
  - fast reconstruction
  - gpu reconstruction
  - jax
  - pulse fitting
  - waveform fit
  - gumbel fit
  - levenberg-marquardt
  - coincidence finder
  - sipm waveforms
  - eventntuple
  - bayesian optimization loop
  - detector response tuning
  - alcf polaris
  - iri api
  - high energy physics
  - genesis mission
  - open source
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.2.0'
last_updated: '2026-10-21'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-crv-fastsim
relationships:
  - type: requires
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation
  - type: compatible_with
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation
  - type: runs_on
    target: mu2e-alcf-polaris
    target_label: ALCF Polaris for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-alcf-aurora
    target_label: ALCF Aurora for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-uva-hpc
    target_label: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction

io_contract:
  input_modes:
    - application/x-hdf5
    - application/vnd.apache.parquet
  output_modes:
    - application/vnd.apache.parquet
    - application/json
  modalities:
    - tabular
    - time-series
  task_tags:
    - event reconstruction
    - pulse fitting
    - detector response
    - fast reconstruction

extension:
  kind: model
  architecture: >-
    Vectorised port of the Offline CRV reconstruction: JAX waveform and
    digitisation model, peak finder and fixed-iteration Gumbel fit with the
    stock parameter limits and failed-fit fallback, per-sector coincidence
    finder on dense pulse tensors; optional direct charge-to-pulse model
  framework: JAX (GPU and CPU), Python
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e CRV fast reconstruction

The reconstruction half of the CRV fast chain, paired with `mu2e-crv-fastsim` and living in the same package and
container: [RobMina/mu2e-crv-fastsim](https://github.com/RobMina/mu2e-crv-fastsim), package `crvfastsim.reco` (Apache-2.0). The stock Offline chain (`CrvRecoPulsesFinder`, `CrvCoincidenceFinder`) stays the reference.

## Chain

| Stage | Fast path | Stock reference |
|---|---|---|
| waveforms and digis | JAX port of the SiPM waveform and digitisation model | `CrvWaveforms`, `CrvDigi` |
| pulses | peak finding, fixed-iteration Gumbel fit, failed-fit fallback, subtract and repeat | `CrvRecoPulsesFinder` (Minuit2 fits) |
| coincidences | per-sector layer, time and slope cuts and clustering, vectorised over events | `CrvCoincidenceFinder` |
| output | `crvpulses` / `crvcoincs` columns with EventNtuple names and units | EventNtuple |

## Validation

- **Waveforms:** identical to the stock model without noise, statistically equal with noise.
- **Pulses on identical digis:** the same pulses found, failed-fit flags in agreement, photoelectrons and times within
  fixed tolerances, no sector-dependent bias.
- **Coincidences on identical pulses:** identical clusters.
- **End to end:** compared with the stock chain on the CRV observables of the analysis.
- **Objective:** the same optimum of the tuning objective.

Passed on existing Monte Carlo and KPP data digis (Polaris A100, Aurora PVC, UVA A100 and B200, CPU); the end-to-end
and objective checks need the fast simulation's charges.

## Intended use

- The reconstruction tier of the CRV response-tuning loop driven by Bayesian optimization (Mu2eBO). Fast-path points
  screen; final points are confirmed with the stock chain.
- A faster CPU pulse fit for Offline, upstreamed separately after validation.

## Limitations

- Extracted configuration only; the veto-efficiency extension to the full detector is in development.
- Reproduces what the stock digitisation models; effects missing there are added to both paths together.
