---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-metacat-mcp
name: Mu2e File Catalog MCP Server (metacat)
description: >-
  Read-only MCP server that gives AI agents discovery of the Mu2e experiment's
  datasets and files through the MetaCat file catalog at Fermilab: raw detector
  data, simulation, digitized, reconstructed and ntuple (EventNtuple) datasets,
  both collaboration production and user datasets. Agents can find datasets by
  namespace, name pattern, creation date and file count; inspect a dataset with
  sample file metadata; and list a dataset's files filtered by run and subrun
  range, event count, size or creation date. Each file name can be translated to
  its storage path or streaming URL (xrootd or https, disk or tape) with the
  Mu2e naming convention, so an agent can hand inputs straight to a job. It is the
  data-discovery part of the Mu2e Genesis phase 1 simulation and analysis
  interfaces: agents locate cosmic-ray run data for data quality monitoring and
  simulation campaign outputs for the Run-1 optimization workflow of the Mu2e
  muon-to-electron conversion search. Runs on the Mu2e AI node at Fermilab;
  reachable only from the Fermilab network.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - metacat
  - file catalog
  - dataset discovery
  - file metadata
  - data management
  - simulation datasets
  - raw data
  - eventntuple
  - run and subrun
  - xrootd
  - dcache
  - data handling
  - mcp server
  - model context protocol
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '0.7.4'
last_updated: '2026-10-15'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/Mu2e/aitools/blob/main/LICENSE
relationships: []

io_contract:
  input_modes:
    - text/plain
    - application/json
  output_modes:
    - application/json
  modalities:
    - tabular
  task_tags:
    - data discovery
    - data retrieval

extension:
  kind: agent
  skills:
    - Find datasets by namespace, name pattern, creation date and file count (discover_datasets)
    - Inspect a dataset with a sample file and its metadata keys (get_dataset_details)
    - List a dataset's files filtered by run and subrun range, event count, size or date (query_dataset_files)
    - Translate file names to storage paths or xrootd and https streaming URLs on disk or tape
    - Report the catalog endpoints and safety notes (get_server_info)
  capabilities:
    streaming: true
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP streamable HTTP'
---

# Mu2e File Catalog MCP Server (metacat)

A read-only Model Context Protocol (MCP) server over Mu2e's MetaCat file catalog, using the `metacat-client` Python
API, with file-location translation from Mu2e's data-handling package (mdh). Any MCP client (Claude Code, Codex,
goose, or the Mu2e agentic workflows) can use it to find data. Software: `mcp/metacat` in
[Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0). This card describes the deployment that serves the
Mu2e collaboration, version 0.7.4 as of 2026-10-15.

## What it does

| Tool | Purpose |
|---|---|
| `discover_datasets` | Datasets by namespace (`mu2e` for production, a user name for personal), name wildcard, creation date, emptiness and file count |
| `get_dataset_details` | One dataset, with an optional sample file and its metadata keys |
| `query_dataset_files` | A dataset's files, filtered by creation date, size, event count, run and subrun range; sortable and paged |
| `get_server_info` | Catalog endpoints, URL-translation options and safety notes |

With `include_url`, file names come back as paths or URLs (schemas path, root (xrootd), http, dcap and sam;
locations disk, tape, scratch and nersc). Without an explicit location the server checks one file and prefers a disk
replica over tape.

Mu2e dataset names follow `data_tier.owner.description.configuration.file_format` (for example `raw`, `sim`, `dig`,
`mcs`, `nts` tiers); a file name adds a sequencer field.

## Content (2026-10-15)

8,521 datasets in the collaboration (`mu2e`) namespace, from raw cosmic-ray detector data to simulation and
EventNtuple production, plus user namespaces.

## How to use it

- Transport: MCP streamable HTTP, listed in the Mu2e MCP registry on the Mu2e AI node at Fermilab.
- Access: collaboration-internal. It is reachable only from the Fermilab network (on site, VPN or an SSH tunnel);
  outside traffic is blocked by the lab firewall. No per-user key is needed today. Reading the files it points to
  needs the usual Fermilab data-access credentials.
- Read-only: no tool creates, changes or declares datasets or files.

## Role in the Mu2e Genesis project

The data-discovery step of the simulation and analysis interfaces of the Mu2e Genesis phase 1 project, "Expedited
Discovery by Leveraging Agentic Workflows for the Mu2e Charged Lepton Flavor Violation Search" (Mu2e-doc-57514).
Agents use it to locate Cosmic Ray Run data for data quality monitoring, and simulation-campaign outputs for the
Run-1 optimization workflow, before launching analysis on FermiGrid.

## Limitations

- Counting files across many datasets is slow at broad scope; filter with `discover_datasets` first.
- Returned paths follow the naming convention. The probed location is known to exist; an explicitly requested
  location is not checked.
- No authentication beyond the Fermilab network boundary.
