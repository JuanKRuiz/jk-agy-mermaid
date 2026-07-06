# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-05

### Added
- 🚀 **Repository Initialization:** Set up Git repository under **GitHub Flow** standard in **Solo-Dev** mode.
- 🛡️ **Governance Files:** Created strict `.gitignore` (excluding compiled databases, `.pyc` files, and Antigravity logs), `LICENSE` (CC BY 4.0), and `DISCLAIMER.md` (liability disclaimer).
- 🧩 **Plugin Base Structure:** Cataloged the `jk-agy-mermaid` plugin with its respective skills (`mermaid-designer`), style and syntax rules, and specialized subagents (`mermaid-auditor`, `mermaid-linter-fixer`, `mermaid-learner`).
- 📂 **Icon Lookup:** High-speed Python automation scripts (`query_icons.py` and `index_icons.py`) and indexed SQLite icons database. Explicitly tracked the pre-built `icons_cache.db` file in Git, as it is the static icon support index for the plugin.
- 🤖 **Supervision Agents:** Created configuration manifests for local sentinel subagents `git-sentinel` and `chronicler` to automate repository hygiene audits and changelog updates.

### Changed
- 📂 **Flat Agent Structure (No Subfolders):** Simplified and flattened local subagents from `.agents/plugins/...` directly to flat Markdown files in `.agents/agents/git-sentinel.md` and `.agents/agents/chronicler.md`, removing unnecessary nesting and optimizing execution.
- 📝 **Format Modernization (Markdown-First):** Migrated local subagent configurations (`git-sentinel` and `chronicler`) from JSON (`.json`) to Markdown (`.md`) system format, adopting the latest Antigravity CLI (`agy`) agent definition convention and enabling rich system prompts.
- 🛡️ **Robust Gitignores (Immune Exclusion):** Updated ignore rule in `.gitignore` to the global highly resilient pattern `!**/icons_cache.db` to ensure the static index is immune to any inherited directory discard rules or accidental overrides.
- 🔌 **Dynamic Agent Injection (Zero-Commit):** Restructured the architecture so that local subagents (`git-sentinel` and `chronicler`) are dynamically injected from the skill and do not form part of the versioned codebase. Excluded the `.agents/` folder in `.gitignore` and safely removed it from the Git index, keeping them physically on disk only for local consumption and on-the-fly execution by Antigravity.
