---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-uva-hpc
name: UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction
description: >-
  The Mu2e experiment's use of the University of Virginia Research Computing
  HPC system (Rivanna and Afton, one Slurm cluster with NVIDIA A100 and B200 GPU
  nodes, Apptainer and open outbound network) through a university allocation.
  Mu2e runs its Geant4-free fast simulation and fast reconstruction of the
  Cosmic Ray Veto there in an Apptainer image, one GPU per job, with
  conditions tables fetched from CVMFS into node memory and deleted at exit, and
  Mu2e-internal reference files streamed into the job and never stored on the
  cluster. Jobs are submitted over SSH and Slurm, by hand or by the fastsimkit
  kit of the Mu2eBO Bayesian-optimization engine, which runs one optimization
  point as one or many single-GPU Slurm jobs (single-GPU jobs start quickly
  where whole GPU nodes queue for hours). A university-allocation complement to the DOE
  leadership facilities for the fast chain.

science:
  - particle-physics
keywords:
  - university of virginia
  - rivanna
  - afton
  - slurm
  - hpc
  - nvidia a100
  - nvidia b200
  - apptainer
  - jax
  - fast simulation
  - fast reconstruction
  - cosmic ray veto
  - bayesian optimization
  - mu2ebo
  - mu2e
  - high energy physics
  - genesis mission
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.1.0'
last_updated: '2026-10-22'
license:
  spdx_id: NOASSERTION
  name: ''
  url: ''
relationships:
  - type: compatible_with
    target: mu2e-alcf-polaris
    target_label: ALCF Polaris for Mu2e fast simulation and reconstruction

extension:
  kind: infrastructure
  resource_class: compute
  facility: University of Virginia Research Computing
  iri_urn: ''
  capabilities:
    - Runs the Mu2e CRV fast simulation, fast reconstruction and their validation in an Apptainer image on one NVIDIA A100 or B200 per Slurm job
    - Job submission, status, cancellation and output retrieval over SSH and Slurm, including the Mu2eBO fastsimkit endpoint adapter
    - Conditions tables fetched from CVMFS into node memory per job and deleted at exit; Mu2e-internal reference files streamed into the job, never stored on cluster disk
    - Open outbound network from compute nodes (PyPI, GitHub, CVMFS)
  quantitative_values: {}
  access_protocol: 'SSH with a key to the UVA HPC login nodes (UVA network or UVA Anywhere VPN), Slurm batch jobs, Apptainer'
  configuration:
    facility_systems: Rivanna and Afton (Slurm partitions gpu and standard), scratch file system, Apptainer
---

# UVA Rivanna/Afton HPC for Mu2e fast simulation and reconstruction

How the Mu2e experiment uses the University of Virginia HPC system for its fast simulation and reconstruction. This
card covers Mu2e's workflow on the cluster, not the cluster itself.

## Capabilities

- GPU jobs in the public `mu2e-fastsim` Apptainer image, built on the cluster from the public
  [RobMina/mu2e-fastsim](https://github.com/RobMina/mu2e-fastsim) repository, one GPU per job with `--nv`.
- The same physics validation as on ALCF Polaris (photon and SiPM response with the real tables, pulse and
  coincidence reconstruction on KPP cosmic data, reproducibility per seed and between CPU and GPU), on A100 and B200.
- `fastsimkit`, the Mu2eBO native kit in [RobMina/mu2e-fastsim-core](https://github.com/RobMina/mu2e-fastsim-core)
  (`mu2efastsim.endpoints`), submits an optimization point as one Slurm job, or (task `chain_point`) as many
  single-GPU jobs whose Mu2e-internal inputs are streamed into each job's memory, and returns the merged metrics.

## Practical notes

- Job scripts and the endpoint adapter are public in `mu2e-fastsim-core` (`uva/`, `mu2efastsim/endpoints/`).
- The JAX CUDA plugin needs cuFFT and cuDNN in the image, or JAX falls back to the CPU without an error.
- The scratch path is a symbolic link: bind the resolved path into Apptainer.
- Compute nodes are not reachable by SSH; files go into a running job with `srun --overlap`.
- An A100 costs less per event than a B200 for this chain; B200 jobs need an image with a recent cuBLAS.
- Work is split into many single-GPU jobs: whole GPU nodes are rarely free, single GPUs usually are.
- Streaming the inputs from Fermilab dominates short jobs: give each job enough work to amortise it.

## Access

A UVA computing account in the Grouper group of an allocation; SSH keys work only from the UVA network or the UVA
Anywhere VPN, so automated submission needs a host there.

## Constraints

- Mu2e-internal inputs never go to shared or scratch storage; tables live in node memory for one job, reference files
  are streamed in, outputs are statistics only.
- No CVMFS mount on the cluster: the stock Mu2e Offline chain does not run here without a container route.
- Allocation-limited and shared with other projects of the allocation's group.
