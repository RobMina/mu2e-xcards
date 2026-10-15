---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-anl-lcrc
name: Argonne LCRC clusters for Mu2e simulation
description: >-
  Argonne National Laboratory's Laboratory Computing Resource Center (LCRC)
  clusters as used by the Mu2e experiment for Geant4 simulation: Improv (825
  nodes, two 64-core AMD EPYC 7713 per node, InfiniBand HDR200), Bebop (672 Intel
  Broadwell nodes) and Swing (A100 GPU nodes). Mu2e simulation code is deployed
  there and run at scale by Argonne Mu2e members. In the Mu2e Genesis phase 1
  project LCRC is, with NERSC, one of the HPC resources for the Run-1
  optimization workflow: agents launch reduced-statistics simulation campaigns
  to evaluate detector and beamline configurations. Access needs an LCRC account
  and a project allocation (Argonne staff and collaborators).

science:
  - particle-physics
keywords:
  - argonne
  - lcrc
  - improv
  - bebop
  - swing
  - hpc
  - cluster
  - geant4 simulation
  - simulation campaign
  - mu2e
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '2026-10-15'
last_updated: '2026-10-15'
license:
  spdx_id: NOASSERTION
  name: ''
  url: ''
relationships: []

extension:
  kind: infrastructure
  resource_class: compute
  facility: Argonne National Laboratory LCRC
  iri_urn: ''
  capabilities:
    - Batch execution of Mu2e Geant4 simulation on CPU clusters (Improv, Bebop)
    - A100 GPU nodes (Swing) for machine-learning work
  quantitative_values:
    improv_nodes: 825
    improv_cores_per_node: 128
    bebop_public_nodes: 672
    swing_public_gpu_nodes: 6
    swing_gpus_per_node: 8
  access_protocol: 'LCRC account and project allocation; batch submission on the clusters'
  configuration: {}
---

# Argonne LCRC clusters for Mu2e simulation

Argonne's Laboratory Computing Resource Center runs the Improv, Bebop and Swing clusters. This card describes them
from Mu2e's side. System figures are from the LCRC system pages (lcrc.anl.gov, read 2026-10-15).

## Capabilities

| System | Size | Node |
|---|---|---|
| Improv | 825 nodes, 2.51 PFlop/s Linpack | 2x AMD EPYC 7713 (64 cores each), InfiniBand HDR200 |
| Bebop | 672 public nodes | 36 Intel Broadwell cores, 128 GB, Omni-Path |
| Swing | 6 public GPU nodes | 8x NVIDIA A100, 128 CPU cores, 1-2 TB memory |

Mu2e Geant4 simulation code is deployed at LCRC and routinely executed at scale (Mu2e-doc-57514).

## Role in the Mu2e Genesis project

HPC resource, alongside NERSC, for the simulation step of the Run-1 optimization workflow
(`mu2e-run1-optimization`); the proposal plans agent-launched campaigns within existing LCRC allocations.

## Access

An LCRC account and an allocated project; Mu2e use is through Argonne members of the collaboration.

## Constraints

- Allocation-limited; the size of the Mu2e allocation is not stated here.
- Outputs must be transferred to Fermilab storage for the analysis step.
