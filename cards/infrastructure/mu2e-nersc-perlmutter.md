---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-nersc-perlmutter
name: NERSC Perlmutter for Mu2e simulation (project m4599)
description: >-
  The Mu2e experiment's use of the Perlmutter supercomputer at NERSC (DOE Office
  of Science, Berkeley Lab) for Geant4 simulation production, under NERSC
  project m4599: CPU nodes run Mu2e simulation campaigns submitted from Fermilab
  through HEPCloud, with outputs transferred back to Fermilab storage
  automatically. Mu2e simulation code is deployed there and routinely run at
  scale (about 0.8 million CPU-hours equivalent in a recent campaign). In the Mu2e
  Genesis phase 1 project it is one of the HPC resources for the Run-1
  optimization workflow, running reduced-statistics simulation campaigns that
  agents launch to evaluate detector and beamline configurations, with full
  statistics reserved for the selected configurations. Access goes through Mu2e
  production and HEPCloud, not individual NERSC logins.

science:
  - particle-physics
keywords:
  - nersc
  - perlmutter
  - hpc
  - supercomputer
  - hepcloud
  - m4599
  - geant4 simulation
  - simulation production
  - cpu nodes
  - mu2e
  - fermilab
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
relationships:
  - type: runs_on
    target: perlmutter-compute
    target_label: Perlmutter HPC System (NERSC)

extension:
  kind: infrastructure
  resource_class: compute
  facility: NERSC
  iri_urn: ''
  capabilities:
    - Runs Mu2e Geant4 simulation production on Perlmutter CPU nodes
    - Receives jobs from Fermilab through HEPCloud; outputs return to Fermilab dCache automatically
    - Mu2e software from CVMFS
  quantitative_values:
    allocation_node_hours: 20000
    mu2e_recent_campaign_cpu_hours_equivalent: 800000
  access_protocol: 'Mu2e production submission through Fermilab HEPCloud'
  configuration:
    nersc_project: m4599
---

# NERSC Perlmutter for Mu2e simulation (project m4599)

How the Mu2e experiment uses Perlmutter at NERSC. The machine itself is described by the NERSC card
`perlmutter-compute` (HPE Cray EX, CPU and A100 GPU nodes); this card covers Mu2e's allocation and workflow.

## Capabilities

- Geant4 simulation production on Perlmutter CPU nodes under NERSC project m4599 (20,000 node-hours, as stated in
  the Mu2e Genesis phase 1 proposal, Mu2e-doc-57514).
- Jobs are routed from Fermilab through HEPCloud; outputs are transferred back to Fermilab dCache automatically.
- Mu2e re-commissioned NERSC running in 2025 and simulation jobs now regularly use it (Mu2e analysis coordination,
  Mu2e-doc-54868); a recent campaign used about 0.8 million CPU-hours equivalent there (Mu2e-doc-57514).

## Role in the Mu2e Genesis project

HPC resource for the simulation step of the Run-1 optimization workflow (`mu2e-run1-optimization`):
agent-launched, reduced-statistics campaigns that score candidate configurations, within the existing allocation.

## Access

Through Mu2e simulation production and HEPCloud; individual collaborators do not need NERSC accounts.

## Constraints

- Allocation-limited (yearly NERSC allocation); figures here are from the 2026 proposal and change each year.
- Batch latency is set by the NERSC queue, so it suits campaigns more than quick single jobs.
