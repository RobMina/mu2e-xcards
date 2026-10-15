---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-fnal-eaf
name: Fermilab Elastic Analysis Facility (EAF) for Mu2e
description: >-
  Fermilab's Elastic Analysis Facility (EAF), a Kubernetes-based interactive
  analysis service with Jupyter notebooks, CPU and GPU sessions and access to
  Fermilab dCache storage, as used by the Mu2e experiment: Python analysis with
  the Mu2e analysis environment from CVMFS and reading EventNtuple files from
  dCache. In the Mu2e Genesis phase 1 project EAF provides the GPUs for training
  and benchmarking machine-learning anomaly detection models (transformer TranAD
  and autoencoder models) on Mu2e detector data quality metrics, for the agentic
  data quality monitoring workflow. Access
  needs a Fermilab account and is through a web browser.

science:
  - particle-physics
keywords:
  - elastic analysis facility
  - eaf
  - fermilab
  - jupyter
  - gpu
  - interactive analysis
  - kubernetes
  - machine learning training
  - anomaly detection
  - python analysis
  - mu2e
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.0'
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
    - Interactive Jupyter sessions with CPU or GPU, launched from a web browser
    - Mu2e Python analysis environment from CVMFS
    - Reads Mu2e files from Fermilab dCache
    - GPU training of machine-learning models on Mu2e data
  quantitative_values: {}
  access_protocol: 'Web browser (JupyterHub) with a Fermilab account'
  configuration: {}
---

# Fermilab Elastic Analysis Facility (EAF) for Mu2e

Fermilab's Elastic Analysis Facility is a shared, Kubernetes-based interactive analysis service (described in
Chavez et al., "The Elastic Analysis Facility's Contribution to the Future of Analysis at Multi-Experiment
Institutions and Future Colliders", 2025). This card describes Mu2e's use of it.

## Capabilities

- Jupyter sessions with CPU or GPU resources, launched from a browser.
- The Mu2e Python analysis environment (from CVMFS) works on EAF as on the Mu2e interactive machines, and Mu2e
  tutorials cover EAF use (Mu2e-doc-52003).
- Reading Mu2e files from dCache.

## Role in the Mu2e Genesis project

GPU resource for the machine-learning half of the agentic DQM workflow (`mu2e-agentic-dqm`): training and
benchmarking transformer (TranAD) and autoencoder anomaly-detection models on Mu2e detector metrics
(Mu2e-doc-57514).

## Access

A Fermilab computing account; sessions start from the EAF web portal on the Fermilab network.

## Constraints

- Shared, interactive facility: GPU availability varies, and long training runs may suit batch resources better.
- No public endpoint; Fermilab account required.
