#!/usr/bin/env bash
#
# Deploys this source repository into the active Antigravity/Jetski plugin
# directory (~/.gemini/config/plugins/jk-agy-mermaid).
#
# Why this script exists
# ----------------------
# 1. The installed plugin directory is a deploy target, NOT a git repository.
#    Keeping a .git inside the target creates two parallel git histories with
#    different SHAs for identical content. Version here, deploy there.
#
# 2. `agy plugin install <path>` registers the plugin, but it copies the entire
#    tree without filters, reintroducing `.git`, `.gitignore`, `.pytest_cache`,
#    and build trivia into the runtime environment.
#
# 3. Antigravity requires rules, agents, and skills to be explicitly registered
#    in plugin.json. An unlisted rule or agent is copied but silently ignored at
#    runtime. This script enforces 100% parity between disk components and plugin.json.
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

echo "==> Validating plugin.json parity against disk components..."
python3 - <<EOF
import json, sys
from pathlib import Path

source = Path("${SOURCE_DIR}")
plugin_file = source / "plugin.json"
with open(plugin_file) as f:
    data = json.load(f)

errors = []

# 1. Rules (must list all rules/*.md)
disk_rules = set(p.relative_to(source).as_posix() for p in source.glob("rules/*.md"))
json_rules = set(data.get("rules", []))
if disk_rules != json_rules:
    missing_in_json = disk_rules - json_rules
    if missing_in_json:
        errors.append(f"rules on disk not listed in plugin.json: {sorted(missing_in_json)}")
    extra_in_json = json_rules - disk_rules
    if extra_in_json:
        errors.append(f"rules in plugin.json not found on disk: {sorted(extra_in_json)}")

# 2. Agents (must list all agents/*.md)
disk_agents = set(p.relative_to(source).as_posix() for p in source.glob("agents/*.md"))
json_agents = set(data.get("agents", []))
if disk_agents != json_agents:
    missing_in_json = disk_agents - json_agents
    if missing_in_json:
        errors.append(f"agents on disk not listed in plugin.json: {sorted(missing_in_json)}")
    extra_in_json = json_agents - disk_agents
    if extra_in_json:
        errors.append(f"agents in plugin.json not found on disk: {sorted(extra_in_json)}")

# 3. Skills (must list all skills/* with SKILL.md)
disk_skills = set(p.parent.relative_to(source).as_posix() for p in source.glob("skills/*/SKILL.md"))
json_skills = set(data.get("skills", []))
if disk_skills != json_skills:
    missing_in_json = disk_skills - json_skills
    if missing_in_json:
        errors.append(f"skills on disk not listed in plugin.json: {sorted(missing_in_json)}")
    extra_in_json = json_skills - disk_skills
    if extra_in_json:
        errors.append(f"skills in plugin.json not found on disk: {sorted(extra_in_json)}")

if errors:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
print(f"  Parity verified: {len(disk_rules)} rules, {len(disk_agents)} agents, {len(disk_skills)} skills.")
EOF

echo "==> Running source pre-flight validation (agy plugin validate)..."
if command -v agy &>/dev/null; then
  agy plugin validate "${SOURCE_DIR}"
fi

# Check registration in Antigravity configuration files
python3 - <<EOF
import json
from pathlib import Path

home = Path.home()
manifest_file = home / ".gemini/config/import_manifest.json"
config_file = home / ".gemini/config/config.json"

registered = False
enabled = False

if manifest_file.is_file():
    try:
        with open(manifest_file) as f:
            m = json.load(f)
        for item in m.get("imports", []):
            if item.get("name") == "jk-agy-mermaid":
                registered = True
                break
    except Exception:
        pass

if config_file.is_file():
    try:
        with open(config_file) as f:
            c = json.load(f)
        p = c.get("plugins", {}).get("jk-agy-mermaid", {})
        if p.get("enabled", False) is True:
            enabled = True
    except Exception:
        pass

if not registered:
    print("WARNING: 'jk-agy-mermaid' is not registered in ~/.gemini/config/import_manifest.json.")
    print("         Antigravity might not index its components until registered.")
if not enabled:
    print("WARNING: 'jk-agy-mermaid' is not enabled in ~/.gemini/config/config.json.")
EOF

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

echo "==> Synchronizing files to ${TARGET_DIR}..."
rsync -a --delete ${DRY_RUN} --itemize-changes \
  --exclude='.git/' \
  --exclude='.gitignore' \
  --exclude='__pycache__/' \
  --exclude='*.py[co]' \
  --exclude='.pytest_cache/' \
  --exclude='scripts/deploy_plugin.sh' \
  "${SOURCE_DIR}/" "${TARGET_DIR}/"

if command -v agy &>/dev/null && [[ -z "${DRY_RUN}" ]]; then
  echo "==> Running target post-flight validation (agy plugin validate)..."
  agy plugin validate "${TARGET_DIR}"
fi

if [[ -z "${DRY_RUN}" ]]; then
  COMMIT="$(git -C "${SOURCE_DIR}" rev-parse --short HEAD)"
  echo
  echo "Successfully deployed ${COMMIT} -> ${TARGET_DIR}"
fi
