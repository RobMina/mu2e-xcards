#!/usr/bin/env bash
# Check one card: template-diff (discovery-local check_card.py), then registry validation if a local stack answers.
#   scripts/check.sh CARD.md [--allow FIELD ...]
# DISCOVERY_LOCAL_DIR defaults to ../discovery-local relative to the ai-config root, if this repo sits in ai-config/mu2e.
set -euo pipefail
card="${1:?usage: $0 CARD.md [--allow FIELD ...]}"; shift
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dl="${DISCOVERY_LOCAL_DIR:-$(cd "$here/../.." 2>/dev/null && pwd)/discovery-local}"
[[ -f "$dl/templates/check_card.py" ]] || { echo "no discovery-local at $dl (set DISCOVERY_LOCAL_DIR)" >&2; exit 2; }
py="${PYTHON:-python3}"
"$py" -c "import yaml" 2>/dev/null || { echo "check_card.py needs PyYAML: set PYTHON to a venv python that has it" >&2; exit 2; }
"$py" "$dl/templates/check_card.py" "$card" "$@"
reg="http://localhost:${REGISTRY_PORT:-18100}"
if ! curl -fsS -m 3 "$reg/api/current/docs" >/dev/null 2>&1; then
  echo "registry not running at $reg: template check only"; exit 0
fi
echo "registry is up; validation means registering, which creates a card. Register with $dl/register_card.sh when ready."
