---
xCard:
  card_type: infrastructure
  version: '0.1'

id: mu2e-ai-node
name: Mu2e AI Node and MCP Server Registry (Fermilab)
description: >-
  Fermilab virtual machine that hosts the Mu2e experiment's Model Context Protocol
  (MCP) servers for AI agents and the registry that lists them. Agents and MCP
  clients (Claude Code, Codex, goose, the Mu2e Genesis workflows) fetch the
  registry to discover the servers, each with its URL, description and whether it
  needs a key, then connect over streamable HTTP. Hosted servers: the Mu2e DocDB
  knowledge base, data quality monitoring metrics, run database, electronic
  logbook, MetaCat file catalog, persistent agent memory, and arXiv and
  INSPIRE-HEP literature search. It is the shared tool-access layer of the Mu2e
  Genesis phase 1 project, run by the Mu2e AI infrastructure group; collaboration
  members reach it from the Fermilab network, with a per-user Mu2e key for the
  servers holding internal information.

science:
  - particle-physics
keywords:
  - mu2e
  - fermilab
  - mcp registry
  - mcp server host
  - model context protocol
  - tool discovery
  - agent infrastructure
  - ai node
  - streamable http
  - service catalog
  - genesis mission
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
relationships:
  - type: has_part
    target: mu2e-kb-mcp
    target_label: Mu2e Knowledge Base MCP Server
  - type: has_part
    target: mu2e-dqm-mcp
    target_label: Mu2e Data Quality Monitoring MCP Server
  - type: has_part
    target: mu2e-runs-mcp
    target_label: Mu2e Run Database MCP Server
  - type: has_part
    target: mu2e-ecl-mcp
    target_label: Mu2e Electronic Logbook MCP Server
  - type: has_part
    target: mu2e-metacat-mcp
    target_label: Mu2e File Catalog MCP Server
  - type: has_part
    target: mu2e-memory-mcp
    target_label: Mu2e Persistent Agent Memory MCP Server
  - type: has_part
    target: mu2e-arxiv-mcp
    target_label: arXiv Paper Search MCP Server
  - type: has_part
    target: mu2e-inspirehep-mcp
    target_label: INSPIRE-HEP Literature MCP Server

extension:
  kind: infrastructure
  resource_class: service
  facility: Fermilab
  iri_urn: ''
  capabilities:
    - Hosts the Mu2e MCP servers as long-running services over streamable HTTP
    - Serves a registry of the hosted servers (URL, description, key requirement) as MCP, JSON and HTML
    - Authenticates internal servers with per-user Mu2e keys
    - Reads Fermilab services (DocDB, DQM database, run database, ECL, MetaCat) on the agents' behalf
  quantitative_values: {}
  access_protocol: 'MCP streamable HTTP on the Fermilab network; registry as an MCP tool and as plain HTTP JSON'
  configuration:
    service_manager: systemd user services, one versioned release per server
---

# Mu2e AI Node and MCP Server Registry (Fermilab)

A Fermilab virtual machine dedicated to Mu2e's AI tooling. It runs the experiment's MCP servers as long-running
services and a small registry server that lists them, so that any agent can discover the Mu2e tools from one place.
Software for the servers and the registry: `mcp/` in [Mu2e/aitools](https://github.com/Mu2e/aitools) (Apache-2.0),
and [Mu2e/kb-mcp](https://github.com/Mu2e/kb-mcp) (MIT) for the knowledge base.

## Capabilities

| Server | Key needed | Card |
|---|---|---|
| Knowledge base (DocDB) | yes | `mu2e-kb-mcp` |
| Data quality monitoring metrics | no | `mu2e-dqm-mcp` |
| Run database | yes | `mu2e-runs-mcp` |
| Electronic logbook (ECL) | yes | `mu2e-ecl-mcp` |
| MetaCat file catalog | no | `mu2e-metacat-mcp` |
| Persistent agent memory | yes | `mu2e-memory-mcp` |
| arXiv search | no | `mu2e-arxiv-mcp` |
| INSPIRE-HEP literature | no | `mu2e-inspirehep-mcp` |

The registry is offered as an MCP tool (`list_mcp_servers`) and as plain HTTP (JSON for client configuration, HTML
for people). Each entry has the server URL, a description an agent can use to choose, and whether a key is needed.

## Access

- From the Fermilab network (on site, VPN or an SSH tunnel); the lab firewall blocks outside traffic.
- Servers holding collaboration-internal information need a personal Mu2e MCP key (a bearer token), issued by the
  Mu2e AI infrastructure maintainers. Keys are per person; a shared key gives shared identity (relevant for the
  memory server).
- Services run under a dedicated service account; users do not log in to run tools.

## Constraints

- A small virtual machine without GPUs: it hosts tools, not model inference or training.
- The servers are read-only except the memory server, which only appends.
- Model inference for agents comes from elsewhere (AmSC Model Access Gateway, ALCF or lab endpoints).
