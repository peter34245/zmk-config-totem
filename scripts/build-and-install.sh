#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMMIT_MESSAGE="${1:-Update keymap}"

cd "${ROOT}"

./scripts/build-firmware-github.sh "${COMMIT_MESSAGE}"
./scripts/install-uf2-macos.py --firmware-dir "${ROOT}/firmware"
