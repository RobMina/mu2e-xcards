---
xCard:
  card_type: agent
  version: '0.1'

id: mu2e-mu2ebo-reporter
name: Mu2eBO campaign reporting agent (mu2ebo-reporter)
description: >-
  Read-only reporting agent that writes a Markdown report on a Mu2e Bayesian
  optimization campaign and checks every number in it against the tool outputs.
  Mu2eBO starts it automatically when an optimization loop exits, and the agent
  driving a campaign can ask for interim reports through the start_report MCP tool;
  it also runs by hand on any campaign. It reads the campaign through Mu2eBO's own
  MCP servers (campaign status, leaderboard of evaluated configurations,
  Gaussian-process surrogate statistics) and adds context from Mu2e DocDB through
  the knowledge-base server. An LLM writes the report: summary, campaign setup,
  outcome by evaluation state, top configurations with objectives and knobs,
  campaign against the whole leaderboard, surrogate view, DocDB context, caveats.
  A deterministic fact check then flags any number that no tool returned, and the
  provenance section is written by the program from the actual calls. A report
  that passes the check can be stored in the Mu2e persistent agent memory server.
  The model sees only read-only tools and cannot launch, stop or refit anything.
  Works with any OpenAI-compatible endpoint (Fermilab vLLM by default, Fermilab
  LiteLLM, ALCF inference, AmSC Model Access Gateway) and with any agent harness.
  It is the reporting agent of the Mu2e Genesis phase 1 Run-1 optimization
  workflow.

science:
  - particle-physics
keywords:
  - mu2e
  - reporting agent
  - campaign report
  - optimization report
  - bayesian optimization
  - leaderboard summary
  - fact check
  - hallucination check
  - provenance
  - mu2ebo
  - autoresearch
  - mcp client
  - agent memory write-back
  - docdb context
  - genesis mission
  - high energy physics
sensitivity: reviewed
developed_by:
  - Mu2e Genesis team
version: '1.0.0'
last_updated: '2026-10-15'
license:
  spdx_id: Apache-2.0
  name: Apache License 2.0
  url: https://github.com/RobMina/mu2ebo-reporter
relationships:
  - type: part_of
    target: mu2e-run1-optimization
    target_label: Mu2e Agentic Run-1 Experiment Optimization Workflow
  - type: requires
    target: mu2e-mu2ebo
    target_label: Mu2eBO (autoresearch) campaign MCP server
  - type: invokes
    target: mu2e-mu2ebo
    target_label: Mu2eBO (autoresearch) campaign MCP server
  - type: invokes
    target: mu2e-mu2ebo-surrogate
    target_label: Mu2eBO GP surrogate MCP server
  - type: invokes
    target: mu2e-kb-mcp
    target_label: Mu2e Knowledge Base MCP Server
  - type: invokes
    target: mu2e-memory-mcp
    target_label: Mu2e Persistent Agent Memory MCP Server
  - type: runs_on
    target: mu2e-ai-node
    target_label: Mu2e AI Node and MCP Server Registry

io_contract:
  input_modes:
    - application/json
    - text/plain
  output_modes:
    - text/markdown
    - application/json
  modalities:
    - text
    - tabular
  task_tags:
    - report generation
    - summarization
    - fact checking
    - optimization monitoring

extension:
  kind: agent
  skills:
    - Write a Markdown report on one Mu2eBO optimization campaign from its status, leaderboard and surrogate statistics
    - Final report at every optimization loop exit, started automatically by Mu2eBO's closed loop
    - Interim (milestone) report when the driving agent asks through Mu2eBO's start_report MCP tool
    - Compare a campaign's best configurations with the whole leaderboard of a study
    - Add context from Mu2e DocDB documents on the same study (knowledge-base search)
    - Check every number in a report against the tool outputs and list the unsupported ones
    - Append a provenance section listing the MCP calls behind the numbers
    - Store a checked report in the Mu2e persistent agent memory server
    - Print an MCP server configuration and the read-only tool allow-list for other agent harnesses
  capabilities:
    streaming: false
    push_notifications: false
    state_transition_history: false
  protocol_version: 'MCP client (stdio and streamable HTTP); OpenAI-compatible chat completions'
---

# Mu2eBO campaign reporting agent (mu2ebo-reporter)

[RobMina/mu2ebo-reporter](https://github.com/RobMina/mu2ebo-reporter) is the reporting agent of the Mu2e Genesis
phase 1 Run-1 optimization workflow (Mu2e-doc-58092, sim/ana task list). It turns a Mu2eBO campaign into a report a
collaborator can read, and every number in the report can be traced to a tool call.

## How it works

1. **Facts.** A fixed set of read-only calls, made by the program and not the model: campaign status and two
   leaderboard reads from Mu2eBO's `autoresearch` server, `stats` from its `surrogate` server, and two `kb_search`
   queries on Mu2e DocDB. They are saved as `facts.json`.
2. **Report.** An LLM writes the Markdown report from those facts. It may call further read-only tools
   (`list_studies`, `show_study`, `campaign_status`, `leaderboard`, `list_problems`, `stats`, `predict`,
   `kb_search`, `kb_get`). It never sees tools that launch, check, stop or refit.
3. **Check.** Every number in the report is matched against the facts, allowing sign flips, percentages and the
   surrogate's `-log10` axes. Unsupported numbers are listed, and numbers on lines citing DocDB are listed
   separately for a manual look. The provenance section is appended by the program.
4. **Write-back (optional).** A report that passed the check goes to the persistent agent memory server.

## How it is started

| Trigger | By | Report |
|---|---|---|
| `exit` | Mu2eBO `graph.closed_loop`, at every loop exit (done, aborted or failed) | final |
| `milestone` | the agent driving the campaign, through Mu2eBO's `start_report` MCP tool, with a note saying why | interim, marked provisional |
| `manual` | an operator, `mu2ebo-report report --prefix P --study S` | final |

Inside Mu2eBO each report is a detached job under the campaign's directory, so it outlives the loop that started
it. `campaign_status` lists the reports, and the `report` tool returns the text.

## Model and harness

The client is the `openai` package against any OpenAI-compatible endpoint. Presets cover Fermilab vLLM (the default,
no key on-site), Fermilab LiteLLM, ALCF inference (Sophia, Metis) and the AmSC Model Access Gateway. It is its own
MCP client, so goose, Claude Code, Codex or cron can run it as a command. `mcp-config` and `prompt` print the server
configuration and tool allow-list for harnesses that load the servers themselves.

## Access and limitations

- Runs on Fermilab Mu2e machines beside a Mu2eBO checkout, in the published Mu2e analysis Python environment. The
  DocDB and memory servers need a collaboration key, and without one the report has no DocDB section.
- Reading another operator's campaign needs a snapshot of its records, because Mu2eBO's readers take file locks
  that need write access. Reports started by Mu2eBO run as the campaign's owner and are not affected.
- The number check cannot catch a wrong claim that carries no new number, for example a conclusion from a DocDB
  document presented as a property of the campaign. Read reports before passing them on; a claims reviewer is
  planned.
- Campaign results are unapproved Mu2e results: reports are marked internal.
