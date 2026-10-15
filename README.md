# mu2e-xcards

xCards for Mu2e resources in the DOE Genesis Mission: Markdown cards with YAML front matter that the
[Genesis Discovery Engine](https://github.com/AI-ModCon/discovery-local) indexes and the xCard Registry stores.
They describe the agents, MCP servers, models, datasets, facilities and workflows built or used by the Mu2e Genesis
phase 1 project ("Expedited Discovery by Leveraging Agentic Workflows for the Mu2e CLFV Search", Mu2e-doc-57514).

This repository holds only the card sources. Each card file is the source of truth; registering a card copies it
into a registry, which assigns its own id.

## Layout

| Directory | `xCard.card_type` | Registry endpoint |
|---|---|---|
| `cards/agents/` | `agent` | `agent_card` |
| `cards/models/` | `model` | `model_card` |
| `cards/datasets/` | `data` | `data_card` |
| `cards/infrastructure/` | `infrastructure` | `resource_card` |
| `cards/workflows/` | `workflow` | none (loaded through storage, see discovery-local) |

File name = the card `id` + `.md`; ids are lowercase, hyphenated and prefixed `mu2e-`.

## Writing a card

Start from the matching template in `discovery-local/templates/` (or use its `xcard-author` skill), never from
scratch. Then:

```bash
scripts/check.sh cards/agents/mu2e-kb-mcp.md   # template-diff check + registry validation if a stack is up
```

Conventions for Mu2e cards:

- `description`, `keywords` and `skills` carry everything search should find; the body is for readers only.
- `sensitivity`: `general` only for public resources. FNAL-only or collaboration-internal services are
  `reviewed` or `restricted`. `unreviewed` is shown to everyone.
- `io_contract` MIME types: `application/x-root` (any ROOT file), `application/vnd.mu2e.art+root`,
  `application/vnd.mu2e.eventntuple+root`, `application/vnd.mu2e.dqm-metrics+json`, `application/x-fhicl`,
  `text/markdown` (reports). List the generic type next to a `vnd.mu2e` one wherever outside tools can read the file.
- Relationships come only from `datasets:`, `base_model:` and `new_version:`, naming existing card ids.
- No secrets, tokens, internal hostnames with credentials, or non-public data locations in a card: this
  repository is public.

## Registering

Registering is a deliberate act (a second registration of the same file creates a second card). With a local stack
running:

```bash
<discovery-local>/register_card.sh cards/agents/mu2e-kb-mcp.md
```

## License

Apache-2.0 for the card text (see `LICENSE`), matching the Discovery Engine and most Mu2e repositories. A card's own
`license:` field describes the resource it documents, not the card.
