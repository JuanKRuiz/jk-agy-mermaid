# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [1.1.0] - 2026-07-05

### Added
- 🛡️ **Icon Compliance Standard:** Integrated a strict, mandatory database-only icon compliance rule in `skills/mermaid-designer/SKILL.md` to prohibit any icon that is not physically present in `icons_cache.db`, enforcing query checks via `query_icons.py`.
- 🛡️ **Phase 0 Sanitization Rule:** Enforced a mandatory "Pre-Existing Diagram Sanitization First" rule across syntax robustness guidelines and the linter-fixer agent prompt, requiring immediate activation of `mermaid-linter-fixer` as the entry gate before applying modifications or styling.
- 🧩 **6-Step Diagramming Workflow:** Integrated the "Master 6-Step Diagramming & Sanitization Workflow Guide" in `skills/mermaid-designer/SKILL.md` and related agent/pipeline prompts. This includes the new **Icon Dual-Path Policy** (using database-approved icons or falling back to iconless shapes) and complexity reduction techniques (Waypoints & Junction Buses).

### Changed
- 🔄 **Workflow Layout Flattening:** Flattened the repository structure by moving `references/workflows/*` directly to `workflows/*` and removing the redundant `references/` directory, updating all path references across documentation, skills, and agent instructions.
- 🔄 **YAML Frontmatter Transition:** Replaced the deprecated class diagram single-line initialization directive (`%%{init: ...}%%`) with standard YAML Frontmatter configuration block in `skills/mermaid-designer/SKILL.md` to improve syntax compatibility and maintainability of theme variables.
- 🔄 **README Flowchart Display Compatibility:** Converted the sample flowchart code block in `README.md` from `mermaid` to plaintext (`text`) and embedded a pre-rendered high-quality image preview to handle GitHub's native inability to load custom icons (`@{ icon: "..." }`).

### Fixed
- 🐛 **Sequence Diagram Rendering Crash:** Fixed sequence diagram rendering crash in GitHub's native Markdown viewer by replacing the ampersand character (`&`) with standard text `and` within the `README.md` sequence diagram notes.

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
- 🛡️ **Dynamic Agent Injection (Zero-Commit):** Restructured the architecture so that local subagents (`git-sentinel` and `chronicler`) are dynamically injected from the skill and do not form part of the versioned codebase. Excluded the `.agents/` folder in `.gitignore` and safely removed it from the Git index, keeping them physically on disk only for local consumption and on-the-fly execution by Antigravity.

### Fixed
- 🐛 **Icon Database Enforcement:** Enforced database-only icon validation requirements to prevent visual rendering failures from unsupported or deprecated icons.
- 🐛 **Auditor Verification Rules:** Added a mandatory icon verification section to `agents/mermaid-auditor.md` to require querying the database via `query_icons.py` and implementing standardized substitution fallbacks.
- 🐛 **Orchestration Diagram Alignments:** Corrected deprecated and unsupported icons in `rules/agentic-orchestration-pipeline.md` (replacing `fa:robot` with `gcp:advanced-agent-modeling`, `fa:stethoscope` with `fa:circle-check`, `fa:magnifying-glass` with `fa:eye`, and `fa:graduation-cap` with `fa:lightbulb`).
- 🐛 **Styling Guide Rules:** Added strict icon verification guidelines to `rules/mermaid-flowchart-styling.md`, establishing mandatory pre-styling checks against `icons_cache.db`.
