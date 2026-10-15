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
conda env create -f environment.yml            # once (or: pip install -r requirements.txt into any venv)
conda activate mu2e-xcards
python scripts/validate.py                     # every card; or name files; --strict fails on warnings too
scripts/check.sh cards/agents/mu2e-kb-mcp.md   # validate.py + discovery-local's template-diff check
```

`validate.py` checks a card offline exactly as the registry does (front matter parsing, Draft 2020-12 validation
against `schema/xcard.schema.json`, the registry's own copy of the Genesis spine schema), plus Mu2e conventions as
warnings. A secret or non-public path is always an error. It agrees with the registry on the
bundled Discovery Engine corpus (the same 2 of 330 cards rejected; the 5 framework and workflow cards the registry never saw are flagged too).
It does not run the registry's LinkML check of data card v2 content, so register data cards against a local stack
before publishing. GitHub Actions runs it on every push.

Conventions for Mu2e cards:

- `description`, `keywords` and `skills` carry everything search should find; the body is for readers only.
- `sensitivity`: `general` only for public resources. FNAL-only or collaboration-internal services are
  `reviewed` or `restricted`. `unreviewed` is shown to everyone.
- `io_contract` MIME types: `application/x-root` (any ROOT file), `application/vnd.mu2e.art+root`,
  `application/vnd.mu2e.eventntuple+root`, `application/vnd.mu2e.dqm-metrics+json`, `application/x-fhicl`,
  `text/markdown` (reports). List the generic type next to a `vnd.mu2e` one wherever outside tools can read the file.
- Relationships: typed entries in `relationships:` (`type` one of the schema's enum, e.g. `has_part`, `based_on`,
  `runs_on`, `requires`; `target` an existing card id) do create graph edges for spine cards (verified 2026-10-15;
  the discovery-local templates say otherwise, which holds only for legacy non-spine cards). `datasets:`,
  `base_model:` and `new_version:` also work. Workflow cards list their component cards with `has_part`.
- No secrets, tokens, internal hostnames with credentials, or non-public data locations in a card: this
  repository is public.

## Registering

Registering is a deliberate act. A second POST of the same file creates a second card, so use `scripts/registry.sh`,
which validates, then creates the card once and replaces it (new version, same registry id) on later pushes, and
resyncs the engine:

```bash
scripts/registry.sh push cards/agents/mu2e-kb-mcp.md   # REGISTRY_URL / ENGINE_URL default to the local stack
scripts/registry.sh ids                                # local card id -> registry id map (untracked)
```

Workflow cards have no registry subtype; `registry.sh push` writes them to the registry's storage with `docker exec`
into the local engine container, using the same fixed key the engine's own "save workflow" uses, so a re-push
replaces the card. Registry `DELETE` is a soft delete that the engine does not see; remove a card from storage and
restart the `api` container to drop it from search.

## License

Apache-2.0 for the card text (see `LICENSE`), matching the Discovery Engine and most Mu2e repositories. A card's own
`license:` field describes the resource it documents, not the card.
