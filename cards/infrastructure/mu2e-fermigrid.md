---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-fermigrid
name: FermiGrid for Mu2e (Fermilab grid computing and storage)
description: >-
  Fermilab's distributed batch computing and storage as used by the Mu2e
  experiment: grid jobs submitted with jobsub, Mu2e software from CVMFS,
  files in dCache (persistent disk, scratch and tape-backed storage), with extra
  opportunistic capacity through the Open Science Grid (OSG). Mu2e runs Geant4
  simulation production, digitization and reconstruction, EventNtuple production
  and analysis jobs here, and stores raw detector data from the Cosmic Ray Run.
  In the Mu2e Genesis phase 1 project it is where agent-launched analyses run
  (figures of merit for the Run-1 optimization workflow, data quality monitoring
  histograms) and where simulation outputs are stored, located through the Mu2e
  MetaCat file catalog. A recent Mu2e production campaign used about 1.6 million
  CPU-hours here. Access needs a Fermilab account, Mu2e membership and grid
  credentials.

science:
  - particle-physics
keywords:
  - fermigrid
  - fermilab
  - grid computing
  - batch computing
  - htcondor
  - jobsub
  - dcache
  - tape storage
  - open science grid
  - osg
  - cvmfs
  - simulation production
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
  facility: Fermilab
  iri_urn: ''
  capabilities:
    - Batch execution of Mu2e simulation, reconstruction and analysis jobs submitted with jobsub
    - Mu2e Offline software and Python environments from CVMFS on every worker
    - dCache disk, scratch and tape-backed storage for raw data, simulation and ntuples
    - Opportunistic extra capacity through the Open Science Grid
  quantitative_values:
    mu2e_recent_campaign_cpu_hours: 1600000
  access_protocol: 'jobsub_lite submission with a Fermilab grid token; data through dCache paths, xrootd or https'
  configuration: {}
---

# FermiGrid for Mu2e (Fermilab grid computing and storage)

Fermilab's shared grid computing facility and its dCache storage, described from Mu2e's side: how the experiment
uses it and how the Genesis phase 1 workflows depend on it.

## Capabilities

- **Batch computing**: Mu2e production and user jobs (Geant4 simulation, digitization, reconstruction, EventNtuple
  production, analysis) submitted with `jobsub_lite`; Mu2e Offline and the Python analysis environment come from
  CVMFS. The Open Science Grid extends capacity opportunistically.
- **Storage**: dCache persistent disk, scratch and tape-backed areas for raw detector data, simulation and
  ntuples. Files are catalogued in MetaCat (card `mu2e-metacat-mcp`), which can translate names into paths or
  xrootd and https URLs.
- **Scale**: a recent Mu2e production campaign used about 1.6 million CPU-hours on FermiGrid (Mu2e-doc-57514).

## Role in the Mu2e Genesis project

The analysis step of both phase 1 workflows runs here: figures of merit for the Run-1 optimization workflow
(`mu2e-run1-optimization`) and data quality monitoring histograms for the agentic DQM workflow
(`mu2e-agentic-dqm`). Simulation outputs produced at NERSC are transferred back and stored here.

## Access

A Fermilab computing account, Mu2e membership and a grid token. Agents act through tools that submit jobs with the
user's own credentials; there is no shared agent account.

## Constraints

- Shared facility: throughput depends on the queue and on the experiment's quota.
- Tape-backed files must be staged before reading; disk replicas are preferred.
