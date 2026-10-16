---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-alcf-polaris
name: ALCF Polaris for Mu2e fast simulation and reconstruction
description: >-
  The Mu2e experiment's use of the Polaris GPU supercomputer at the Argonne
  Leadership Computing Facility (ALCF, DOE Office of Science) for its
  Geant4-free, GPU-accelerated fast simulation and fast reconstruction of the
  Cosmic Ray Veto and tracker. Jobs are submitted from Fermilab machines through
  the DOE Integrated Research Infrastructure (IRI) API with Globus
  authentication and run under PBS on NVIDIA A100 nodes, from a JAX Python
  environment and a container on the Eagle project file system. Compute nodes
  reach the internet only through the ALCF proxy and cannot reach the Fermilab
  conditions database, so Mu2e conditions travel as text files and no CVMFS is
  assumed. In the Mu2e Genesis phase 1 project it is the GPU resource for
  resimulating and re-reconstructing cached cosmic events per point of the
  detector response and alignment tuning loop.

science:
  - particle-physics
keywords:
  - alcf
  - polaris
  - argonne
  - gpu supercomputer
  - nvidia a100
  - iri api
  - integrated research infrastructure
  - globus
  - pbs
  - eagle filesystem
  - container
  - jax
  - fast simulation
  - mu2e
  - high energy physics
  - genesis mission
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.1.0'
last_updated: '2026-10-16'
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
    - Runs the Mu2e CRV (and later tracker) fast simulation and fast reconstruction on A100 GPU nodes
    - Job submission from Fermilab through the ALCF IRI API (Globus token, ALCF identity), scheduled by PBS
    - Python/JAX environment and container on the Eagle project file system; node-local NVMe for caches
    - Outbound network only through the ALCF proxy; Mu2e conditions as text files, no Fermilab database access
  quantitative_values: {}
  access_protocol: 'DOE IRI API at ALCF (Globus authentication), PBS batch'
  configuration:
    facility_systems: Polaris (compute), Eagle (storage)
---

# ALCF Polaris for Mu2e fast simulation and reconstruction

How the Mu2e experiment uses Polaris at ALCF. This card covers Mu2e's workflow on the machine, not the machine
itself; the Discovery Engine corpus has no ALCF facility card yet to point to.

## Capabilities

- GPU nodes (NVIDIA A100) for the JAX fast simulation (`mu2e-crv-fastsim`, `mu2e-tracker-fastsim`) and fast
  reconstruction (`mu2e-crv-fastreco`, `mu2e-tracker-fastreco`).
- Batch submission through the IRI API from Fermilab machines; jobs run under PBS.
- Code synchronised to the Eagle project file system; caches on node-local NVMe.

## Practical notes

The job drivers are public in [RobMina/mu2e-crv-fastsim](https://github.com/RobMina/mu2e-crv-fastsim) (`iri/`).


- The ALCF IRI API implements less than its published OpenAPI specification: no file upload, and a limited command
  form. Mu2e job scripts are therefore shipped inline in the job specification.
- Python comes from a project environment on Eagle; environment modules are not available in IRI job shells.
- Compute nodes have no direct route to GitHub or Fermilab services: code and conditions are staged in advance,
  through the ALCF proxy.
- Physics kernels set full float32 or float64 matrix precision: the A100 default (TF32) is not accurate enough
  for the validation tolerances.

## Access

ALCF accounts on a Genesis-provided ALCF project; IRI tokens through Globus with the ALCF identity.

## Constraints

- Allocation-limited and time-limited; the tracker stage needs an allocation beyond the current one.
- No CVMFS assumed, so the stock Mu2e Offline chain (the validation reference) runs on FermiGrid, not here.
