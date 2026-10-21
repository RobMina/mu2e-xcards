---
xCard:
  card_type: workflow
  version: '0.1'

id: mu2e-crv-response-tuning
name: Mu2e CRV and tracker response tuning with GPU fast simulation and reconstruction
description: |-
  Planned workflow of the Mu2e Genesis team for tuning the Monte Carlo detector response and alignment of the Mu2e
  Cosmic Ray Veto (CRV), and later the straw tracker, against cosmic-ray data from the extracted (KPP) configuration
  at Fermilab. Each point of the loop resimulates and re-reconstructs cached cosmic events with Geant4-free,
  GPU-accelerated fast simulation and fast reconstruction on ALCF Polaris (submitted through the DOE IRI API),
  computes the CRV and track observables, compares them with data, and returns one objective to a Bayesian
  optimizer (Mu2eBO). Fast-path points screen the response space (light yield, attenuation, thresholds, timing,
  noise) and module poses; the best points are confirmed with the stock Geant4 and Offline chain on FermiGrid.
  Goal: a CRV response-tuning point in minutes on one GPU node instead of hours of CPU and days of grid latency,
  so the alternating alignment and response fit becomes a same-day campaign.

  Steps:
  1. Cache: generate CRY cosmic primaries once and run the fast simulation (card mu2e-crv-fastsim; tracker stage
     card mu2e-tracker-fastsim) to cached step tables on Polaris (card mu2e-alcf-polaris); a geometry move
     regenerates them, a response-only point does not.
  2. Propose: the Bayesian optimizer (card mu2e-mu2ebo, surrogate card mu2e-mu2ebo-surrogate) proposes response
     parameters or module poses.
  3. Resimulate the response and re-reconstruct on GPU (cards mu2e-crv-fastreco, mu2e-tracker-fastreco).
  4. Score: CRV and track observables against data, one objective per point.
  5. Confirm: the best points run through the stock Geant4 and Offline chain on FermiGrid (card mu2e-fermigrid);
     fast and stock points are kept as different fidelities.
  6. Report the campaign (card mu2e-mu2ebo-reporter).

  Inputs: CRY cosmic primaries, Mu2e geometry exported from Offline, text-file conditions, KPP cosmic data
  observables. Outputs: tuned response parameters and module poses, a leaderboard per campaign, and a report.

science:
  - particle-physics
keywords:
  - mu2e
  - cosmic ray veto
  - crv
  - straw tracker
  - detector response tuning
  - detector alignment
  - mc data agreement
  - bayesian optimization
  - fast simulation
  - fast reconstruction
  - gpu workflow
  - multi-fidelity
  - alcf polaris
  - iri api
  - kpp extracted configuration
  - genesis mission
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.2.0'
last_updated: '2026-10-21'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2e-xcards/blob/main/LICENSE

datasets: []
relationships:
  - type: has_part
    target: mu2e-crv-fastsim
    target_label: Mu2e CRV fast simulation
  - type: has_part
    target: mu2e-crv-fastreco
    target_label: Mu2e CRV fast reconstruction
  - type: has_part
    target: mu2e-tracker-fastsim
    target_label: Mu2e tracker fast simulation
  - type: has_part
    target: mu2e-tracker-fastreco
    target_label: Mu2e tracker fast reconstruction
  - type: has_part
    target: mu2e-mu2ebo
    target_label: Mu2eBO (autoresearch) closed-loop Bayesian optimization
  - type: has_part
    target: mu2e-mu2ebo-surrogate
    target_label: Mu2eBO Gaussian-process surrogate MCP server
  - type: has_part
    target: mu2e-mu2ebo-reporter
    target_label: Mu2eBO campaign reporting agent
  - type: runs_on
    target: mu2e-alcf-polaris
    target_label: ALCF Polaris for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-alcf-aurora
    target_label: ALCF Aurora for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-uva-hpc
    target_label: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction
  - type: runs_on
    target: mu2e-fermigrid
    target_label: FermiGrid for Mu2e
---

# Mu2e CRV and tracker response tuning with GPU fast simulation and reconstruction

A planned workflow that puts the fast simulation and fast reconstruction cards into a Bayesian-optimization loop.
The CRV stage comes first; the tracker stage and the Mu2eBO integration follow once the fast path exists.

## Steps

| # | Step | Component | Card |
|---|---|---|---|
| 1 | Cache primaries and fast-simulated steps; regenerate on geometry moves only | CRV (and tracker) fast simulation on Polaris | `mu2e-crv-fastsim`, `mu2e-tracker-fastsim`, `mu2e-alcf-polaris` |
| 2 | Propose response parameters or poses | Mu2eBO and its surrogate | `mu2e-mu2ebo`, `mu2e-mu2ebo-surrogate` |
| 3 | Resimulate response, re-reconstruct | GPU fast reconstruction | `mu2e-crv-fastreco`, `mu2e-tracker-fastreco` |
| 4 | Score against data | observables and objective | — |
| 5 | Confirm best points with the stock chain | Geant4 and Offline on the grid | `mu2e-fermigrid` |
| 6 | Report | reporting agent | `mu2e-mu2ebo-reporter` |

## Code

The fast simulation and reconstruction: [RobMina/mu2e-crv-fastsim](https://github.com/RobMina/mu2e-crv-fastsim) (Apache-2.0).

## Caveats

- The CRV fast reconstruction is validated and reachable from Mu2eBO through the `fastsimkit` kit (UVA endpoint,
  card `mu2e-uva-hpc`), with a throughput smoke task so far; the response and objective tasks and the tracker stage
  are in development.
- Fast-path results are a screening tier; recommendations are confirmed with the stock chain.
- Results are reported in Mu2e documents, not in this card.
