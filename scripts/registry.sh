#!/usr/bin/env bash
# Register or update cards in an xCard Registry without creating duplicates, then resync the engine.
#   scripts/registry.sh push CARD.md ...     validate, then PUT if the card is known to this registry, else POST
#   scripts/registry.sh ids                  show the local card-id -> registry-id map
# The registry assigns its own id on POST; the map (.registry-ids.<host_port>.tsv, untracked) remembers it per
# registry so later pushes replace the card (PUT, new version) instead of adding a copy.
# Env: REGISTRY_URL (default http://localhost:18100), ENGINE_URL (default http://localhost:18000), PYTHON.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
reg="${REGISTRY_URL:-http://localhost:18100}"
eng="${ENGINE_URL:-http://localhost:18000}"
py="${PYTHON:-python3}"
map="$root/.registry-ids.$(printf %s "${reg#*://}" | tr -c 'A-Za-z0-9' '_').tsv"
touch "$map"

subtype_of() {  # card_type -> endpoint and media type
  case "$1" in
    agent) echo "agent_card agent-card" ;;
    model) echo "model_card model-card" ;;
    data|dataset) echo "data_card data-card" ;;
    infrastructure) echo "resource_card resource-card" ;;
    *) return 1 ;;
  esac
}

field() { "$py" - "$1" "$2" <<'PY'
import sys, yaml
text = open(sys.argv[1], encoding="utf-8").read().removeprefix("\ufeff").split("\n---", 1)[0]
fm = yaml.safe_load(text.split("---", 1)[1])
v = fm.get("id") if sys.argv[2] == "id" else (fm.get("xCard") or {}).get("card_type")
print(v or "")
PY
}

# Workflow cards have no registry subtype. Write them to the registry's storage the way the engine's own
# "save workflow" does (card_builder.py): a fixed key derived from the card id, so a re-push replaces it.
push_workflow() {
  local card="$1" cid="$2" ctr="${API_CONTAINER:-genesis-local-api-1}" dk
  dk="$(command -v docker || echo "$HOME/.docker/bin/docker")"
  [[ -x "$dk" ]] || { echo "$card: workflow cards need docker exec into the api container" >&2; return 1; }
  "$dk" exec -i -e CARD_ID="$cid" "$ctr" python -c '
import os, sys, uuid
from genesis.knowledge._registry_source import XCardRegistrySource
ns = uuid.UUID("3f5c1d90-6b2a-4e77-9d14-2c8ab5e30f61")  # card_builder._WORKFLOW_NAMESPACE
cid = os.environ["CARD_ID"]
prefix = (os.environ.get("XCARD_STORAGE_PREFIX") or "registry").strip("/")
key = f"{prefix}/resource_card/{uuid.uuid5(ns, cid)}/versions/1-{uuid.uuid5(ns, cid + chr(58) + chr(49))}.md"
XCardRegistrySource()._put_sync(key, sys.stdin.read(), None)
print(f"{cid} -> storage {key}")
' < "$card"
}

push() {
  local card="$1" cid ctype sub media rid out code
  "$py" "$root/scripts/validate.py" "$card" >/dev/null || { "$py" "$root/scripts/validate.py" "$card"; return 1; }
  cid="$(field "$card" id)"; ctype="$(field "$card" type)"
  if [[ "$ctype" == workflow ]]; then push_workflow "$card" "$cid"; return; fi
  read -r sub media < <(subtype_of "$ctype") || { echo "$card: card_type '$ctype' cannot be registered" >&2; return 1; }
  rid="$(awk -F'\t' -v k="$cid" '$1==k {print $2}' "$map" | tail -1)"
  if [[ -n "$rid" ]] && [[ "$(curl -s -o /dev/null -w '%{http_code}' "$reg/api/current/registry/$sub/$rid")" == 200 ]]; then
    out="$(curl -s -X PUT "$reg/api/current/registry/$sub/$rid" -H "Content-Type: text/vnd.genesis.$media+markdown" \
      --data-binary @"$card" -w '\n%{http_code}')"
  else
    out="$(curl -s -X POST "$reg/api/current/registry/$sub" -H "Content-Type: text/vnd.genesis.$media+markdown" \
      --data-binary @"$card" -w '\n%{http_code}')"
  fi
  code="${out##*$'\n'}"; out="${out%$'\n'*}"
  if [[ "$code" != 200 && "$code" != 201 ]]; then echo "$card: registry said HTTP $code: $out" >&2; return 1; fi
  rid="$(printf %s "$out" | "$py" -c 'import json,sys; print(json.load(sys.stdin)["id"])')"
  ver="$(printf %s "$out" | "$py" -c 'import json,sys; print(json.load(sys.stdin)["version"])')"
  awk -F'\t' -v k="$cid" '$1!=k' "$map" > "$map.tmp"
  printf '%s\t%s\n' "$cid" "$rid" >> "$map.tmp"; mv "$map.tmp" "$map"
  echo "$cid -> $sub/$rid version $ver (HTTP $code)"
}

case "${1:-}" in
  push)
    shift; [[ $# -gt 0 ]] || { echo "push needs card files" >&2; exit 2; }
    rc=0; for c in "$@"; do push "$c" || rc=1; done
    curl -fsS -X POST "$eng/api/v1/admin/resync" >/dev/null && echo "engine resynced" || { echo "engine resync failed at $eng" >&2; rc=1; }
    exit $rc ;;
  ids) cat "$map" ;;
  *) sed -n '2,8p' "$0" >&2; exit 2 ;;
esac
