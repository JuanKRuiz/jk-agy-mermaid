# 🛠️ Master Architecture & Operations Guide (jk-agy-mermaid)

This document provides an in-depth technical analysis, system map, and operational blueprints for the `jk-agy-mermaid` plugin. It reflects the real-world state of the plugin's structure, focusing on static database resolution and local agent injections.

---

## 🗺️ System Map & Directory Architecture

The project is structured modularly to guarantee scalability, fast indexing, and complete separation of concerns. Note that some local development agents are injected dynamically into the workspace, while the icon index database remains static:

```text
jk-agy-mermaid/
├── plugin.json                 # Metadata descriptor, skills catalog, agents, and rules
├── README.md                   # Clean, public-facing user guide
├── docs/
│   └── architecture_and_operations.md  # [This Document] In-depth technical architecture
├── .agents/                    # [GIT-IGNORED] Dynamically injected local Git agents
│   └── agents/
│       ├── chronicler.md       # Auto-changelog documentation manager
│       └── git-sentinel.md     # Pre-commit & stage compliance auditor
├── agents/                     # Versioned Antigravity system prompts
│   ├── mermaid-auditor.md      # Esthetic consistency, contrast, and "Zero-Style" rule auditor
│   ├── mermaid-linter-fixer.md # Preventive syntactic healer (parentheses, quotes, linkStyle)
│   └── mermaid-learner.md      # Learning loop and icon immunity orchestrator
├── rules/                      # Immutable operational rules and policies
│   ├── mermaid-flowchart-styling.md  # Esthetic manual, palettes, waypoints, and subgraphs
│   ├── mermaid-syntax-robustness.md  # Syntactic healing formulas and hierarchical flattening
│   └── mermaid-learning-loop.md      # Sequences and protocols for rendering glitches
└── skills/
    └── mermaid-designer/       # Master Skill encapsulating assets, scripts, and workflows
        ├── SKILL.md            # Skill descriptor with activation and execution directives
        ├── references/         # Detailed workflow guides
        │   └── workflows/
        │       ├── draw-flowchart.md       # Interactive design-from-scratch guide (TD/ELK)
        │       └── fix-broken-diagram.md   # Step-by-step triage and repair guide
        ├── resources/          # Indexable data catalogs of official iconography
        │   └── databases/
        │       ├── icons_cache.db          # [Pre-compiled] Master SQLite icons index
        │       ├── gcp_icons.json
        │       ├── aws_icons.json
        │       ├── azure_icons.json
        │       ├── svg_logos.json
        │       └── font_awesome_icons.json
        └── scripts/            # Autonomous high-speed automation scripts
            └── query_icons.py  # Batch-indexed icon finder (centralized SQLite)
```

---

## 👥 Specialized Agent Matrix

To optimize cognitive load, the plugin distributes responsibility across three versioned Antigravity agents, two git-ignored local agents, and one master skill:

### 🌐 Versioned Project Agents (Included in Repo)
| System Role | Technical Name | Primary Responsibility | Associated Rule/Asset |
| :--- | :--- | :--- | :--- |
| 👑 **Master Designer** | `mermaid-designer` | Skill orchestration. Translates architecture requirements into clean layouts, mapping icons, and applying hierarchical topologies. | `query_icons.py`, `draw-flowchart.md` |
| 🎨 **Style Auditor** | `mermaid-auditor` | Guarantees visual consistency, contrast, and corporate brand palettes. Audits and removes default yellow backgrounds, and enforces "Zero-Style". | `mermaid-flowchart-styling.md` |
| 🩺 **Syntactic Healer** | `mermaid-linter-fixer` | Analyzes code defensively. Corrects syntax, balances quotes, escapes parentheses in flowcharts, and flattens subgraphs. | `mermaid-syntax-robustness.md`, `fix-broken-diagram.md` |
| 🧠 **Learning Manager** | `mermaid-learner` | System immunity. Classifies rendering glitches, updates local exclusion markdown files, and hot-patches diagrams. | `mermaid-learning-loop.md` |

### 🔒 Injected Local Agents (Git-Ignored / Local Environment Only)
| System Role | Technical Name | Primary Responsibility | Interaction Target |
| :--- | :--- | :--- | :--- |
| 📝 **Auto-Chronicler** | `chronicler` | Audits git diffs and staging commits to automatically maintain a standardized, emoji-rich `CHANGELOG.md` following *Keep a Changelog*. | `CHANGELOG.md` |
| 🛡️ **Git Sentinel** | `git-sentinel` | Audits staging areas, enforces Conventional Commits, prevents hardcoded secrets, and blocks versioned build artifacts. | Git Staging Area |

---

## 🎨 Industrial Design Rules & Visual Standards

### 1. Standard Canvas Configuration (YAML Frontmatter)
The old initialization directive `%%{init: ...}%%` is deprecated. Professional diagrams must use the unified variables header in YAML Frontmatter format:

```yaml
---
config:
  layout: elk
  look: neo
  theme: default
themeVariables:
  fontFamily: 'Roboto, Google Sans, Helvetica, Arial, sans-serif'
  primaryColor: '#4285F4'
  secondaryColor: '#34A853'
  tertiaryColor: '#FBBC04'
  mainBkg: '#FFFFFF'
  nodeBorder: '#4285F4'
  clusterBkg: '#F8F9FA'
  clusterBorder: '#DADCE0'
  lineColor: '#5F6368'
  edgeLabelBackground: '#ffffff'
---
```

### 2. High-Contrast Pastel Color Palette
Five fixed, highly legible CSS classes are defined with pastel backgrounds and solid, high-saturation borders, forcing the font to pure black (`color:#000`):

*   **gcpBlue (General/Web/API/Compute):** `#E8F0FE` (background), `#1967D2` (border)
*   **gcpGreen (Private Network/Security/Databases):** `#E6F4EA` (background), `#1E8E3E` (border)
*   **gcpYellow (Auth/IAM/Third-party):** `#FEF7E0` (background), `#B06000` (border)
*   **gcpRed (Alerts/Blocks/Errors):** `#FCE8E6` (background), `#D93025` (border)
*   **neutral (Support/Auxiliary/Generic):** `#F1F3F4` (background), `#5F6368` (border)

### 3. "Zero-Style" Rule for Complex SVGs
To prevent vector flattening or opaque blobs in the renderer, **it is strictly forbidden to apply custom CSS styles** (fill/stroke) to nodes using icons from:
*   **Amazon Web Services:** Prefix `aws:*`.
*   **Microsoft Azure:** Prefix `azure:*`.
*   **SVG Logos:** Prefix `logos:*` (such as `logos:kubernetes`, `logos:mongodb`).
*   **Google Cloud Exceptions:** Brand gradients like `gcp:cloud-load-balancing`, `gcp:private-service-connect`, and `gcp:advanced-agent-modeling`.

### 4. Explicit Subgraph Styles
Default yellow subgraphs represent a severe design error. Every subgraph declared in the code **must possess an explicit styling rule** at the end of the file:
*   **GCP Cloud/Managed:** `style ID_SG fill:#e8f0fe,stroke:#1967D2,stroke-width:2px`
*   **Security/Data Private:** `style ID_SG fill:#e6f4ea,stroke:#1E8E3E,stroke-width:2px`
*   **External/Zero Trust:** `style ID_SG fill:#ffffff,stroke:#9E9E9E,stroke-dasharray:5 5,stroke-width:2px`
*   **Support/Generic:** `style ID_SG fill:#f9f9f9,stroke:#DADCE0,stroke-width:2px`

---

## 🩺 The Auto-Heal Algorithm (Preventive Linting)

```mermaid
graph TD
    Start([Input Code]) --> Triage{Starts with architecture-beta?}
    Triage -- Yes --> DisableEscape[Disable Parenthesis Escaping]
    Triage -- No --> EnableEscape[Enable Strict Escaping]
    
    DisableEscape & EnableEscape --> Balance[Balance Quotes & Brackets]
    Balance --> Flatten{Subgraph depth > 2?}
    
    Flatten -- Yes --> Elevate[Elevate 3rd level to 2nd level]
    Flatten -- No --> KeepHierarchy[Keep Hierarchies]
    
    Elevate & KeepHierarchy --> linkStyle[Heal linkStyle: Remove Trailing Semicolons]
    linkStyle --> Output[Clean Native Code]
```

1.  **Grammar Triage:** If `architecture-beta`, disables parenthesis escaping to preserve native service declarations. If `flowchart`, strict escaping is activated.
2.  **Literal Balancing:** Repairs open quotes and injects missing delimiters.
3.  **Subgraph Flattening:** If nesting depth > 2, it elevates third-level components to the second level to prevent box warping in the ELK renderer.
4.  **linkStyle Semicolon Removal:** Locates `linkStyle` expressions and removes any trailing semicolon `;`.

---

## ⚡ High-Speed SQLite Search Engine

To avoid slow sequential lookups across individual Markdown files or slow network resolutions, the plugin utilizes a pre-populated, static **SQLite3** index database (`icons_cache.db`) built as a core resource asset. 

**This database is static and immutable within the plugin distribution.** It is loaded directly by the query engine and is not compiled, written, or regenerated during runtime.

### Batch Search (One-Shot Batching)
To optimize agent execution times, a single consolidated call must be made with all keywords:

```bash
python3 jk-agy-mermaid/skills/mermaid-designer/scripts/query_icons.py --batch "load balancer" "entra id" "gcp:vertexai" "database" "user"
```

The script queries the local SQLite database and returns a structured JSON map:

```json
{
  "load balancer": {
    "file": "valid-icons-lists/aws_icons.md",
    "line_num": 803,
    "name": "Res-elastic load-balancing application load-balancer",
    "code": "aws:res-elastic-load-balancing-application-load-balancer",
    "description": "Represents Application Load Balancer (ALB).",
    "is_style_compatible": 0
  }
}
```

---

## 🧠 Systemic Immunity & Learning Loop

The `mermaid-learner` agent governs permanent visual immunity under the following feedback loop:

```text
    [Glitches or Rendering Errors Reported by the User]
                                │
                                ▼
             Step 1: Glitch Classification
             ├── Type A: Non-existent or deprecated icon (renders "?")
             └── Type B: Vector interference (solid black or opaque block)
                                │
                                ▼
             Steps 2 and 3: Knowledge Asset Update
             ├── Type A: Search for alternatives in DB. Register in Blacklist
             │           inside "special-icon-cases.md" indicating replacement.
             └── Type B: Add identifier or pattern to the Zero-Style exclusion
                         list in "special-icon-cases.md".
                                │
                                ▼
             Step 4: Hot-Patching of the Diagram (.mmd)
             ├── Replace the icon code with the approved alternative.
             └── Remove the conflicting color class from the node.
                                │
                                ▼
             Step 5: Professional Reporting
             └── Present report to the user with the updated local cases
                 file and the exact Git Diff of applied changes.
```

---

*jk-agy-mermaid Plugin by JuanK Ruiz - Engineering and Documentation Excellence.*
