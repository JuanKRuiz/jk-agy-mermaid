# jk-agy-mermaid

*   **Author:** JuanK Ruiz
*   **Subject:** Master Operator & Architecture Guide for jk-agy-mermaid Plugin
*   **Version:** v1.0.0

---

## 1. Introduction and Project Purpose

**jk-agy-mermaid** is a specialized, autonomous, industrial-grade plugin designed for the **Google Antigravity** agentic AI ecosystem. Its primary mission is to equip agents with advanced capabilities to **conceive, diagram, audit, and hot-patch** complex **Mermaid.js** diagrams (including `flowchart`, `architecture-beta`, `sequenceDiagram`, and `classDiagram`).

The plugin solves the most common issues in AI-driven diagramming:
1.  **Compilation Errors and Broken Parsers:** Dynamically corrects syntactic imbalances, unescaped parentheses, and malformed connector declarations.
2.  **Poor Spatial Alignments:** Forces the use of the advanced `elk` spatial layout engine with hierarchical flattening rules.
3.  **Lack of Consistency and Branding:** Ensures the application of the official **Google Cloud (GCP-First)** palette and high-contrast neutrals, eradicating default yellow colors.
4.  **Visual Degradation of Brand Vectors:** Implements the strict **Zero-Style** rule on AWS, Azure, and third-party Logos, preventing custom CSS directives from flattening or covering native SVG gradients.
5.  **Self-Adaptive Learning Cycle:** Features a closed-loop feedback mechanism to record icon failures, update an exclusion blacklist, and hot-fix diagrams in microseconds.

---

## 2. Directory Architecture and System Map

The project is designed modularly to guarantee scalability, fast indexing, and separation of concerns:

```text
jk-agy-mermaid/
├── plugin.json                 # Metadata descriptor, skills catalog, agents, and rules
├── README.md                   # This master documentation of the independent project
├── agents/                     # System Prompt definitions for Specialized Subagents
│   ├── mermaid-auditor.md      # Esthetic consistency, contrast, and "Zero-Style" rule auditor
│   ├── mermaid-linter-fixer.md # Preventive syntactic healer (parentheses, quotes, linkStyle)
│   └── mermaid-learner.md      # Learning loop and icon immunity orchestrator
├── rules/                      # Immutable operational rules and compilation policies
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
        │       ├── gcp_icons.json
        │       ├── aws_icons.json
        │       ├── azure_icons.json
        │       ├── svg_logos.json
        │       └── font_awesome_icons.json
        └── scripts/            # Autonomous high-speed automation scripts
            ├── query_icons.py  # Batch-indexed icon finder (centralized SQLite)
            └── index_icons.py  # Compiler and regenerator of the SQLite icon database
```

---

## 3. Role Matrix and Specialized Subagents

The plugin distributes the AI's cognitive load across three specialized subagents and a Master Skill, ensuring that each design task is processed by the corresponding expert:

| System Role | Technical Name | Primary Responsibility | Interaction Tools |
| :--- | :--- | :--- | :--- |
| **Master Designer** | `mermaid-designer` | Primary orchestration skill. Translates technical architecture requirements into clean, high-fidelity layouts, mapping icons and applying hierarchical topologies. | `query_icons.py`, `draw-flowchart.md` |
| **Style Auditor** | `mermaid-auditor` | Guarantees visual consistency, contrast balance, and corporate palette compliance. Audits and removes default yellow background colors from subgraphs, and enforces the Zero-Style rule. | `mermaid-flowchart-styling.md` |
| **Syntactic Healer** | `mermaid-linter-fixer` | Analyzes code defensively. Corrects broken syntax, balances quotes, escapes parentheses in flowcharts, and flattens subgraphs to prevent layout deformations. | `mermaid-syntax-robustness.md`, `fix-broken-diagram.md` |
| **Learning Manager** | `mermaid-learner` | Manages system immunity. Classifies rendering glitches, updates the blacklist and special cases file, hot-patches diagrams, and regenerates the SQLite database. | `mermaid-learning-loop.md`, `index_icons.py` |

---

## 4. Industrial Design Rules and Visual Standards

### 4.1. Standard Canvas Configuration (YAML Frontmatter)
The use of the old initialization directive `%%{init: ...}%%` is forbidden. Every professional diagram must exclusively use the unified variables header in YAML Frontmatter format:

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

### 4.2. Brand Node Color Palette (High-Contrast Pastel)
Five fixed, highly legible CSS classes are defined with pastel backgrounds and solid, high-saturation borders, forcing the font to pure black (`color:#000`):

*   **gcpBlue (General/Web/API/Compute):** `#E8F0FE` (background), `#1967D2` (border)
*   **gcpGreen (Private Network/Security/Databases):** `#E6F4EA` (background), `#1E8E3E` (border)
*   **gcpYellow (Auth/IAM/Third-party):** `#FEF7E0` (background), `#B06000` (border)
*   **gcpRed (Alerts/Blocks/Errors):** `#FCE8E6` (background), `#D93025` (border)
*   **neutral (Support/Auxiliary/Generic):** `#F1F3F4` (background), `#5F6368` (border)

### 4.3. Mandatory "Zero-Style" Rule for Complex Icons
To prevent vector flattening, solid black spots, or opaque blobs in the renderer, **it is strictly forbidden to apply custom CSS styles** (fill classes `fill` or stroke classes `stroke`) to nodes using icons from:
*   **Amazon Web Services:** Icon set with `aws:*` prefix.
*   **Microsoft Azure:** Icon set with `azure:*` prefix.
*   **SVG Logos:** Icon set with `logos:*` prefix (such as `logos:kubernetes`, `logos:mongodb`).
*   **Google Cloud Exceptions:** Icons with complex brand gradients like `gcp:cloud-load-balancing`, `gcp:private-service-connect`, and `gcp:advanced-agent-modeling`.

### 4.4. Prohibition of Default Yellow Subgraph Backgrounds
Any subgraph rendered in Mermaid's default yellow color represents a severe design error. All subgraphs declared in the code **must possess an explicit styling rule** at the end of the file:
*   **Managed Zones/GCP Cloud:** `style ID_SG fill:#e8f0fe,stroke:#1967D2,stroke-width:2px`
*   **Security/Secure Data Zones:** `style ID_SG fill:#e6f4ea,stroke:#1E8E3E,stroke-width:2px`
*   **External/Zero Trust Zones:** `style ID_SG fill:#ffffff,stroke:#9E9E9E,stroke-dasharray:5 5,stroke-width:2px`
*   **Support/Generic Zones:** `style ID_SG fill:#f9f9f9,stroke:#DADCE0,stroke-width:2px`

### 4.5. Prohibition of Inline Icons
Injecting icon codes directly into the text or label of a node is not allowed. Icons must be declared autonomously and independently on the line immediately following:
*   *Correct:*
    ```mermaid
    EndUser["`**Frontline User**`"]:::gcpBlue
    EndUser@{ icon: "fa:user" }
    ```

### 4.6. Original File Preservation Policy (Sibling Creation Policy)
When optimizing, improving, or refactoring an existing diagram, **it is strictly forbidden to overwrite the original file**. You must always create a parallel file with the suffix `_improved.mmd` or `_optimized.mmd` in the same directory (e.g., from `infra/net.mmd` to `infra/net_improved.mmd`).

---

## 5. The Auto-Heal Algorithm (Syntactic Robustness)

The preventive syntactic healer processes Mermaid code line by line under the following deterministic scheme:

1.  **Grammar Triage:** Identifies if the diagram starts with `architecture-beta`. If so, it **suspends** parenthesis escaping to preserve the native declaration of services and icons. If it is `flowchart`, strict escaping is activated.
2.  **Literal Balancing:** Repairs open quotes and injects missing delimiters in text labels.
3.  **Subgraph Flattening (Depth > 2):** If subgraph nesting with 3 or more levels of depth is detected, it elevates third-level components to the second level, removing the third-level grouping and associating them with unified classes or color outlines to mitigate box warping in the ELK renderer.
4.  **linkStyle Healing:** Locates `linkStyle` expressions and systematically removes any trailing semicolon `;` at the end of the line.
5.  **Parenthesis Escaping:** Transforms problematic labels like `db[DB (Standard)]` into formats protected by Markdown strings: `db["`DB (Standard)`"]`.

---

## 6. Icon Search Engine and Automation

The plugin implements a centralized **SQLite3** indexed database solution for ultra-fast icon search. **It is forbidden to interact in a manual or ad-hoc manner using inline python terminal scripts with sqlite3**, and the autonomous search and batching script must be called exclusively.

### 6.1. Batch Search and Resolution (One-Shot Batching)
To optimize agent execution times, a single consolidated call must be made with all keywords and diagram variants:

```bash
python3 jk-agy-mermaid/skills/mermaid-designer/scripts/query_icons.py --batch "load balancer" "entra id" "gcp:vertexai" "database" "user"
```

The search script queries the local database and returns a structured JSON map with the heuristic relevance of each term, blacklist validation, and style suitability:

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

### 6.2. Compilation and Indexing
When the icon lists in Markdown are modified or the exceptions file `special-icon-cases.md` is updated, the centralized database must be regenerated using the indexing script:

```bash
python3 jk-agy-mermaid/skills/mermaid-designer/scripts/index_icons.py
```

---

## 7. Learning Loop and Adaptive Feedback

The plugin is equipped with permanent systemic immunity governed by `mermaid-learner` under the following sequential protocol:

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
             Step 5: Re-Indexing and Professional Reporting
             ├── Execute "index_icons.py" to apply database changes.
             └── Present report to the user with the updated cases
                 file and the exact Git Diff of applied changes.
```

---

*jk-agy-mermaid Plugin by JuanK Ruiz - Engineering and Documentation Excellence.*
