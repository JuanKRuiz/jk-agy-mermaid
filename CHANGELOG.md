# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 🚀 **Native Headless Cloudtop Rendering Engine & Aspect Ratio Auto-Padding Pipeline:** Integrated a fully self-contained rendering pipeline inside `skills/mermaid-designer/scripts/` (`render_pipeline.py`, `render_native.js`, `pad_diagram.py`) and mirrored via plugin root `scripts/`. Controls headless Google Chrome via Puppeteer, bundles local Mermaid.js and offline Iconify vector icon packs (`gcp`, `logos`, `material-symbols`, `fa6-solid`, `mdi`, `carbon`, `aws`, `azure`), generating 3x HiDPI PNGs. Automatically evaluates vertical aspect ratio $\frac{H}{W}$ and applies symmetric white padding (`#FFFFFF`) to guarantee $\frac{H}{W} \le 1.15$ (`_padded.png`) for seamless fit in Google Docs Pageless canvas, PDFs, and slide decks. Eradicated external cross-project script references.
- 📐 **Dagre Ranking Invariant & Symmetrical 2-Column Grid Pattern:** Formalized Dagre ranking mechanics for invisible connections (`~~~` enforcing `rank(B) >= rank(A) + 1`) in `rules/mermaid-flowchart-styling.md` (Section 9) and introduced the canonical Symmetrical 2-Column Grid Pattern in `skills/mermaid-designer/SKILL.md` (Step 4) with dual-waypoint coupling, horizontal rank-pinning, and milestone footer centering to eliminate asymmetric vertical staggering.

- 🛡️ **True Teleporter Waypoints Governance:** Formalized the True Teleporter Waypoint standard across `mermaid-flowchart-styling.md`, `mermaid-syntax-robustness.md`, `skills/mermaid-designer/SKILL.md`, `mermaid-linter-fixer.md`, and `mermaid-auditor.md`. Mandated zero physical cross-cluster connecting lines between waypoints to guarantee decoupled layout and compact geometry. Enforced multi-line tokenization (`<br>`) to optimize circle diameter.
- ⚡ **Auto-Activation YAML Frontmatter:** Injected standard Jetski/Antigravity `trigger: model_decision` YAML frontmatter headers with descriptive triggers across all plugin rule files (`mermaid-flowchart-styling.md`, `mermaid-syntax-robustness.md`, `agentic-orchestration-pipeline.md`, `mermaid-learning-loop.md`), ensuring automatic discovery and progressive disclosure by the model in system prompts.
- 🛡️ **Target-Aware Snippet Handling & Header Discrimination:** Formalized Section 2.4 in `rules/mermaid-flowchart-styling.md`, Rule 8 & Section 4 in `rules/mermaid-syntax-robustness.md`, and Rule 7 in `agents/mermaid-linter-fixer.md`. Establishes strict channel discrimination between standalone files (`.mmd`, repository docs, where 100% of advanced features, YAML frontmatter, and extended diagrams are preserved) and the Jetski Conversational Chat UI (where syntax snippets for reading must be fenced with ` ```text ` or wrapped in minimal valid diagram headers, eliminating client-side header parsing crashes).


### Fixed
- 🐛 **Category Prioritization Masking in Batch Search (`query_icons.py`):** Resolved relevance masking where higher-priority categories (cloud) superseded exact or high-relevance matches in subsequent categories (SVG logos, Font Awesome). Implemented global candidate relevance ranking with category priority tie-breaking and brevity ratio bonus.
- 🐛 **Natural Language & Stop Words Resolution (`query_icons.py`):** Added intelligent filtering of Spanish and English stop words (`el`, `la`, `de`, `para`, etc.) in multi-word queries, whole-word boundary enforcement for short tokens (<= 2 chars), and whole-phrase description bonuses. Multi-word phrases like `"el balanceador de carga"`, `"la base de datos"`, and `"el usuario"` now reliably resolve to load balancers, databases, and user icons instead of coincidental substring matches.
- 🐛 **Syntax Robustness on Empty Queries (`query_icons.py`):** Guarded `query_single()` against empty query words, returning an empty result set immediately without executing malformed SQL (`WHERE  AND is_blacklisted = 0`) or swallowing exceptions.
- 🐛 **Validation and Silent Failure Prevention (`update_icon.py`):** Added explicit `cursor.rowcount` validation so attempts to update non-existent icon codes fail with an informative error on stderr and exit code 1. Enforced strict binary validation (`0` or `1`) on `--blacklist` and `--style-compatible` flags. Fixed `--substitute` missing argument bug where passing fewer than 4 arguments silently cleared substitute codes; added validation that substitute icon codes exist in the database.
- 🐛 **Code Input Sanitization (`query_icons.py` & `update_icon.py`):** Integrated enhanced `clean_code()` across all CLI modes to automatically strip surrounding punctuation, brackets, parentheses, backticks, and quotes from icon codes and query terms (e.g. `(docker)`, `salesforce!`, `[python]`).
- 🛡️ **Test Database Isolation (`query_icons.py` & `update_icon.py`):** Added `ICONS_DB_PATH` environment variable override support to both CLIs, enabling the test suite to execute against an isolated temporary database copy without polluting or mutating the production `icons_cache.db`.

### Changed
- 🛡️ **Deduplicate Taxonomic Redundancies & Enforce Uniqueness (`icons_cache.db`):** Consolidated 389 duplicate icon code groups (410 redundant rows) across `logos:*` categories, merged search keyword vocabularies into the primary records, applied `CREATE UNIQUE INDEX idx_icons_code ON icons(code)`, and reclaimed ~356 KB of disk space via SQLite `VACUUM`.
- 📚 **Documentation & License Harmonization:** Aligned open-source license statement in `README.md` to Creative Commons Attribution 4.0 International Public License (`CC BY 4.0`) matching `LICENSE` and badge. Removed references to nonexistent JSON database files from `SKILL.md` and `docs/architecture_and_operations.md`, and registered `update_icon.py` in the directory architecture tree.

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

### Changed
- 🛡️ **Robust Gitignores (Immune Exclusion):** Updated ignore rule in `.gitignore` to the global highly resilient pattern `!**/icons_cache.db` to ensure the static index is immune to any inherited directory discard rules or accidental overrides.

### Fixed
- 🐛 **Icon Database Enforcement:** Enforced database-only icon validation requirements to prevent visual rendering failures from unsupported or deprecated icons.
- 🐛 **Auditor Verification Rules:** Added a mandatory icon verification section to `agents/mermaid-auditor.md` to require querying the database via `query_icons.py` and implementing standardized substitution fallbacks.
- 🐛 **Orchestration Diagram Alignments:** Corrected deprecated and unsupported icons in `rules/agentic-orchestration-pipeline.md` (replacing `fa:robot` with `gcp:advanced-agent-modeling`, `fa:stethoscope` with `fa:circle-check`, `fa:magnifying-glass` with `fa:eye`, and `fa:graduation-cap` with `fa:lightbulb`).
- 🐛 **Styling Guide Rules:** Added strict icon verification guidelines to `rules/mermaid-flowchart-styling.md`, establishing mandatory pre-styling checks against `icons_cache.db`.
