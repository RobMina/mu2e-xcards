---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-esnet-east
name: ESnet East cloud compute (AWS) for Mu2e fast simulation and reconstruction
description: >-
  The Mu2e experiment's use of ESnet East, the ESnet cloud compute endpoint on
  Amazon Web Services (Kubernetes, CPU and NVIDIA GPU nodes with shared EFS
  storage) reached through the DOE Integrated Research Infrastructure (IRI) API
  v2 with an American Science Cloud (AmSC) personal access token, no facility
  account and no batch queue wait. Mu2e runs its Geant4-free fast simulation
  and fast reconstruction of the Cosmic Ray Veto there as containerised jobs
  from a public OCI image: CPU pods for the numpy chain and tests, NVIDIA T4
  pods for the GPU SiPM-charge and coincidence stages, with conditions tables
  fetched from CVMFS into the pod and deleted at exit. It demonstrates that the
  workflow is portable across DOE facilities and gives overflow capacity when
  leadership-class queues are busy.

science:
  - particle-physics
keywords:
  - esnet
  - aws
  - cloud compute
  - kubernetes
  - iri api
  - integrated research infrastructure
  - american science cloud
  - amsc
  - container
  - oci image
  - nvidia t4
  - jax
  - fast simulation
  - portability
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
  facility: ESnet
  iri_urn: ''
  capabilities:
    - Runs the Mu2e CRV fast simulation, fast reconstruction and their tests as Kubernetes jobs from a public OCI image
    - Job submission and file operations through the ESnet IRI API v2 with an AmSC personal access token
    - CPU pods and NVIDIA T4 or A100 GPU pods sized per job; open outbound network (PyPI, GitHub, CVMFS)
    - Conditions tables fetched from CVMFS into pod-local storage and deleted at exit; bulk outputs through Globus
  quantitative_values: {}
  access_protocol: 'DOE IRI API v2 at ESnet East (AmSC personal access token, Bearer), Kubernetes jobs with a container image'
  configuration:
    facility_systems: ESnet East low-priority compute (AWS EKS, Kueue), EFS storage, Globus DTN
---

# ESnet East cloud compute (AWS) for Mu2e fast simulation and reconstruction

How the Mu2e experiment uses the ESnet East IRI endpoint, cloud compute that ESnet runs on Amazon Web Services. This
card covers Mu2e's workflow on the endpoint, not the endpoint itself.

## Capabilities

- Containerised jobs: every job is a Kubernetes pod running a public OCI image
  (`ghcr.io/robmina/mu2e-fastsim`, `cpu` and `gpu` variants, built from the public
  [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim) repository).
- CPU pods for the numpy reference chain and the test suites; NVIDIA T4 pods for the GPU stages of the CRV response
  and reconstruction. An A100 pool exists but needs at least two GPUs per job.
- Job submission, status, cancellation and file operations (upload, list, view, download of small files) through
  the IRI API v2; larger outputs through the endpoint's Globus collection.

## Practical notes

- The job drivers are public in [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core) (`iri/`),
  the `core/` submodule of the umbrella repository.
- Pods start within one to two minutes (node scale-up and image pull included).
- The image's code directory is read-only for the pod user: outputs go to `/tmp` or the job directory.
- The JAX CUDA plugin needs cuFFT and cuDNN in the image even when the kernels do not use them, or JAX falls back to
  the CPU without an error.
- Physics kernels run in float64: a T4 matches an A100 on the memory-bound SiPM stage but is much slower on
  float64-heavy stages, so T4 pods suit the SiPM and coincidence stages and functional GPU checks.

## Access

AmSC identity and membership of an AmSC project with resources at ESnet; the personal access token from MyAmSC is
bound to that project and valid for 30 days. Globus transfers need membership of the collection's Globus group.

## Constraints

- Mu2e-internal inputs never go to the shared EFS storage; they are fetched into the pod and deleted before the job
  ends.
- No CVMFS mount, no Apptainer, no FUSE inside pods: the stock Mu2e Offline chain does not run here.
- Allocation-limited; the hackathon allocation is small and time-limited.
