#!/usr/bin/env bash
#
# Deploys this source repository into the active Antigravity/Jetski plugin
# directory.
#
# Why this script exists
# ----------------------
# The installed plugin directory used to be a second git repository kept in sync
# by hand with `cp` plus a re-commit of the same message. That produced two
# parallel histories with different SHAs for byte-identical content, and every
# change had to be committed twice. The installed directory is a build artifact:
# it carries no history of its own. Version here, deploy there.
#
# Usage:
#   ./scripts/deploy_plugin.sh            # deploy
#   ./scripts/deploy_plugin.sh --dry-run  # show what would change

set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${HOME}/.gemini/config/plugins/jk-agy-mermaid"

DRY_RUN=""
if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN="--dry-run"
  echo "DRY RUN — no files will be written."
fi

if [[ ! -f "${SOURCE_DIR}/plugin.json" ]]; then
  echo "ERROR: ${SOURCE_DIR} does not look like the plugin source (no plugin.json)." >&2
  exit 1
fi

# Refuse to deploy a source tree that still has uncommitted work: the whole point
# is that the deployed copy is always reproducible from a known commit.
if [[ -z "${DRY_RUN}" ]] && [[ -n "$(git -C "${SOURCE_DIR}" status --porcelain --untracked-files=no)" ]]; then
  echo "ERROR: source tree has uncommitted changes. Commit them first, so the" >&2
  echo "       deployed plugin always maps to a known commit." >&2
  git -C "${SOURCE_DIR}" status --short >&2
  exit 1
fi

# A .git directory inside the target means someone reintroduced the mirror
# anti-pattern. Fail loudly rather than deploying on top of it.
if [[ -d "${TARGET_DIR}/.git" ]]; then
  echo "ERROR: ${TARGET_DIR}/.git exists. The installed plugin must not be a git" >&2
  echo "       repository. Remove it and re-run this script." >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

rsync -a --delete ${DRY_RUN} --itemize-changes \
  --exclude='.git/' \
  --exclude='.gitignore' \
  --exclude='__pycache__/' \
  --exclude='*.py[co]' \
  --exclude='.pytest_cache/' \
  --exclude='scripts/deploy_plugin.sh' \
  "${SOURCE_DIR}/" "${TARGET_DIR}/"

if [[ -z "${DRY_RUN}" ]]; then
  COMMIT="$(git -C "${SOURCE_DIR}" rev-parse --short HEAD)"
  echo
  echo "Deployed ${COMMIT} -> ${TARGET_DIR}"
fi
