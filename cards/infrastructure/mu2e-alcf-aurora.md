---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-alcf-aurora
name: ALCF Aurora for Mu2e fast simulation and reconstruction
description: >-
  The Mu2e experiment's use of the Aurora exascale supercomputer at the Argonne
  Leadership Computing Facility (ALCF, DOE Office of Science) for its
  Geant4-free fast simulation and fast reconstruction of the Cosmic Ray Veto.
  Each node runs one simulation process per Intel Data Center GPU Max tile,
  with the detector response on the tile and the pulse and coincidence
  reconstruction on the node's Xeon CPUs. The JAX code runs unchanged through
  the upstream JAX oneAPI plugin, with a few backend-specific code paths that
  avoid compiler and runtime limits of that experimental backend. Jobs are
  submitted with PBS from an Aurora login node; Mu2e conditions tables are
  fetched from CVMFS, and Mu2e-internal inputs are streamed into node memory,
  never written to the shared file system. It is an optional second GPU
  resource beside ALCF Polaris for the detector response tuning loop.

science:
  - particle-physics
keywords:
  - alcf
  - aurora
  - argonne
  - exascale
  - intel data center gpu max
  - ponte vecchio
  - oneapi
  - sycl
  - jax
  - pbs
  - flare filesystem
  - fast simulation
  - mu2e
  - high energy physics
  - genesis mission
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.0'
last_updated: '2026-10-21'
license:
  spdx_id: NOASSERTION
  name: ''
  url: ''
relationships: []

extension:
  kind: infrastructure
  resource_class: compute
  facility: ALCF
  iri_urn: ''
  capabilities:
    - Runs the Mu2e CRV fast simulation chain end to end on whole nodes, one process per Intel GPU tile
    - Detector response (photons, SiPM charges, waveforms) on the GPU tiles, pulse and coincidence reconstruction on the node CPUs
    - Python/JAX environment on the Flare project file system, with the upstream JAX oneAPI plugin
    - Conditions tables fetched from CVMFS over HTTP into node memory and deleted at job exit
  quantitative_values: {}
  access_protocol: 'PBS on Aurora (ssh to an Aurora login node with ALCF multi-factor authentication); not reachable through the ALCF IRI API'
  configuration:
    facility_systems: Aurora (compute), Flare (storage)
---

# ALCF Aurora for Mu2e fast simulation and reconstruction

How the Mu2e experiment uses Aurora at ALCF. This card covers Mu2e's workflow on the machine, not the machine itself.

## Capabilities

- Whole-node jobs of the CRV fast simulation chain: cosmic-ray generator tables in, coincidence clusters out, with
  one process per GPU tile and per-process summaries merged at the end of the job.
- Detector response on Intel Data Center GPU Max tiles in float64; reconstruction on the node's Xeon CPUs, where it
  runs faster than on the tiles.
- The same validation checks as on Polaris: the GPU stages agree with the validated numpy references, and the
  reconstruction reproduces the stock Mu2e reconstruction on Monte Carlo and test-stand data.

## Practical notes

The job templates are public in [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core)
(`aurora/`), the `core/` submodule of [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim).

- JAX comes from the upstream `jax[oneapi]` extra, matching the JAX version used elsewhere; its oneAPI runtime
  library must come before the system oneAPI module on the library path.
- The oneAPI backend is experimental. The Mu2e code keeps three backend-specific paths: one coincidence-finder padding
  size is skipped, one fused response kernel is split, and waveform synthesis groups work into fewer, larger calls.
  Results agree with the CPU and CUDA paths.
- One process per tile is set with the flat device hierarchy and an affinity mask; the node has no local disk, so
  temporary data lives in memory.
- Compute nodes reach PyPI, GitHub and the CVMFS servers through the ALCF proxy, but not the Fermilab conditions
  database: conditions travel as text files.

## Access

ALCF accounts on a Genesis-provided ALCF project with Aurora access; jobs are submitted from an Aurora login node
after multi-factor authentication. The ALCF IRI API does not implement Aurora compute.

## Constraints

- Mu2e-internal inputs (conditions tables, simulation libraries, reference data) never go to the shared Flare file
  system: they are streamed into node memory for the job and deleted at exit.
- The GPU reconstruction kernels run much slower on the tiles than on NVIDIA A100s, so reconstruction stays on CPUs.
- Submission needs an interactive login, so unattended operation needs a user-run Globus Compute endpoint.
- Allocation-limited and time-limited.
