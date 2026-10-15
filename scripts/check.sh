#!/usr/bin/env bash
# Check cards before registering: offline schema + Mu2e-convention validation, then the template-diff check.
#   scripts/check.sh [CARD.md ...]          (default: every card)
# PYTHON: a python with pyyaml + jsonschema (environment.yml / requirements.txt). DISCOVERY_LOCAL_DIR: optional,
# enables discovery-local's check_card.py (defaults to ../../discovery-local when this repo sits in ai-config/mu2e).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
py="${PYTHON:-python3}"
"$py" "$here/scripts/validate.py" "$@"
dl="${DISCOVERY_LOCAL_DIR:-$(cd "$here/../.." 2>/dev/null && pwd)/discovery-local}"
if [[ -f "$dl/templates/check_card.py" && $# -gt 0 ]]; then
  for c in "$@"; do "$py" "$dl/templates/check_card.py" "$c"; done
fi
