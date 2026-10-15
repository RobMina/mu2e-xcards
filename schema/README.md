# Vendored xCard schema

`xcard.schema.json` is the Genesis spine schema exactly as the xCard Registry validates it, copied so cards can be
checked offline with `scripts/validate.py`.

| | |
|---|---|
| Copied from | `ghcr.io/ai-modcon/xcard-registry@sha256:e5703b8bb0fca6126c2180799036ce1ba8292c2d8279b45d5a3c5fa96a8ebe00` |
| Path in image | `/app/.venv/lib/python3.12/site-packages/hpdf_xcard_registry/schemas/xcard.schema.json` |
| Upstream | `gitlab.osti.gov/genesis/discovery-engine` `src/genesis/card_schema/xcard.schema.json`, revision `7fe6d044c523e3ae2b7f64bac4675bfc7a0b942c` (`GENESIS_SCHEMA_REVISION` in the registry's `xcard_validator.py`) |
| md5 | `1bff54fc74bb40ba7f0c1b19ca0e5e7d` |
| Copied | 2026-10-15 |

The registry's copy is newer than the one inside the engine image (it also accepts `card_type: dataset`), and it is
the one that decides whether a card registers, so it is the one vendored here.

What the registry does that `validate.py` does not: Genesis data card v2 content (the `supports_*` /
`discoverability` blocks) is also checked with LinkML against `genesis_datacard.yaml`. Register data cards against a
local stack before publishing.

## Refreshing

```bash
IMG=ghcr.io/ai-modcon/xcard-registry:latest
docker pull $IMG
docker run --rm --entrypoint cat $IMG \
  /app/.venv/lib/python3.12/site-packages/hpdf_xcard_registry/schemas/xcard.schema.json > schema/xcard.schema.json
docker image inspect $IMG --format '{{index .RepoDigests 0}}'   # record the digest above
```

Then rerun `scripts/validate.py` on every card and update the table.
