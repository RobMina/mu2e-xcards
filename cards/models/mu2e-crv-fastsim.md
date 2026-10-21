---
xCard:
  card_type: model
  version: '0.1'

id: mu2e-crv-fastsim
name: Mu2e CRV fast simulation (Geant4-free, GPU-accelerated cosmic simulation)
description: >-
  Geant4-free, GPU-accelerated fast simulation of cosmic-ray muons in the Mu2e
  Cosmic Ray Veto (CRV) for the extracted (KPP) detector configuration at
  Fermilab, with no magnetic field. It replaces the Geant4 transport stage of
  the stock CRY cosmic simulation: CRY primaries are pre-selected geometrically,
  muons are transported along straight lines through the passive material and
  the scintillator bars (Bethe-Bloch energy loss with Landau/Vavilov
  fluctuations, Highland multiple scattering, Birks saturation, ray-box bar
  crossings), and electromagnetic secondaries and non-muon primaries come from a
  library built from one Geant4 run. Output is a table of CRV steps
  (HDF5/Parquet) with the same content as the Offline CrvStep collection, so the
  stock Mu2e digitisation, reconstruction and EventNtuple run on it unchanged
  for validation. The CRV photon and SiPM response is ported to JAX for NVIDIA
  A100 GPUs, with a planned differentiable neural photon field (SIREN-style)
  replacing the lookup tables. Geometry comes from the Offline geometry service
  and its GDML export, so a module move is a parameter change. It runs in a
  container on ALCF Polaris, submitted through the DOE IRI API, and on CPU for
  tests. Purpose: many Monte Carlo variants of CRV geometry and response for
  MC/data agreement, module alignment and Bayesian-optimization response tuning.
  Status: in development, validated level by level against Geant4. Open source
  (Apache-2.0) at github.com/RobMina/mu2e-crv-fastsim.

science:
  - particle-physics
keywords:
  - mu2e
  - cosmic ray veto
  - crv
  - fast simulation
  - geant4 replacement
  - gpu simulation
  - jax
  - scintillator response
  - sipm response
  - cosmic ray muons
  - cry generator
  - muon transport
  - optical photon simulation
  - neural photon field
  - differentiable simulation
  - alcf polaris
  - iri api
  - kpp extracted configuration
  - detector alignment
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
  - type: runs_on
    target: mu2e-alcf-polaris
    target_label: ALCF Polaris for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-uva-hpc
    target_label: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-fermigrid
    target_label: FermiGrid for Mu2e

io_contract:
  input_modes:
    - application/x-hdf5
    - application/json
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
    - detector response

extension:
  kind: model
  architecture: >-
    Physics-based fast simulation: geometric pre-selection of CRY primaries,
    straight-line muon transport with parametric energy loss and multiple
    scattering, a Geant4-built secondary library, and a vectorised CRV photon
    and SiPM response from the Offline lookup tables; a neural photon field is
    the planned second tier
  framework: JAX (GPU and CPU), Python
  base_model: ''
  training_datasets: []
  metrics: []
---

# Mu2e CRV fast simulation (Geant4-free, GPU-accelerated)

A replacement for the Geant4 stage of the Mu2e extracted-configuration cosmic simulation, built by the Mu2e Genesis
team. Code: [RobMina/mu2e-crv-fastsim](https://github.com/RobMina/mu2e-crv-fastsim) (Apache-2.0), Python package `crvfastsim` with one CLI. The extracted configuration is the Kinetic Performance Prototype (KPP) setup in the Mu2e hall: tracker and CRV
modules read out together with no magnetic field.

## How it works

| Tier | What | Replaces |
|---|---|---|
| 1a | straight-line muon transport through the GDML material, parametric energy loss and scattering, bar crossings | Geant4 tracking of muons |
| 1b | non-muon primaries and muon-induced showers from a library built once with Geant4 | Geant4 tracking of secondaries |
| response | photon yield and SiPM charges on GPU, ported from the Offline CRV response | the CPU photon generation step |
| 2 (planned) | a differentiable neural photon field trained on the lookup tables, then on optical simulation | the lookup tables |

The interface is a CRV step table. A small art module reads it into the stock Offline chain (validation path A), so
the stock digitisation and reconstruction are the reference, and only the fast path differs.

## Validation

Level by level against a Geant4 reference sample generated from the same CRY primaries:

- geometry (every bar against the Geant4 world);
- muon crossings (count, path length, visible energy);
- response (photoelectrons, rates, coincidences, layer efficiency, on the same digitisation);
- non-muon component per sector;
- GPU against CPU response on identical steps.

Comparisons go by truth-particle identity and cover all CRV sectors. No free scale factors: the response parameters
are what downstream tuning fits. The thresholds are fixed in the project plan; results go to Mu2e documents, not this
card.

## Intended use

- Many Monte Carlo variants of CRV geometry (module alignment) and response (light yield, attenuation, thresholds) for
  MC/data agreement studies of the extracted configuration.
- The simulation tier of a Bayesian-optimization loop over CRV response parameters (with `mu2e-crv-fastreco`).

## Limitations

- Extracted configuration only: no magnetic field, no beam, no tracker yet (see `mu2e-tracker-fastsim`).
- The non-muon component is a resampled library, not a transport: its validity outside the library's configuration
  is a reported deficit, not a guarantee.
- The CRV response lookup tables are Mu2e-internal and are not distributed with the code or images.
- The repository holds code, configuration and the plan only: no Mu2e-internal inputs and no simulation outputs.
