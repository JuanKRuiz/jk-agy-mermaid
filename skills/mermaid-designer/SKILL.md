---
name: mermaid-designer
description: Master skill for professional Mermaid diagramming, architectural top-down layout styling, auto-heal syntax linting, and auto-adaptive icon lookup.
---

# Google Antigravity Mermaid Designer Master Skill (mermaid-designer)

This skill equips the Antigravity agent with industrial-grade, expert capabilities to conceive, design, audit, and heal complex Mermaid diagrams (flowcharts, beta architecture diagrams, etc.).

---

## 1. Directories and Resource Map

This skill organizes its knowledge assets progressively. Depending on the type of operation required, you can access detailed documentation and tools in:

### A. Workflow Guides
*   **Design from Scratch:** [references/workflows/draw-flowchart.md](references/workflows/draw-flowchart.md)
    *   *Usage:* Step-by-step interactive workflow to create TB diagrams with clean subgraphs and high-contrast theme variables.
*   **Sanitization and Repair:** [references/workflows/fix-broken-diagram.md](references/workflows/fix-broken-diagram.md)
    *   *Usage:* Triage and auto-healing algorithms to fix loose quotes, parentheses, and remove semicolons.

### B. Automation Tools (Scripts)
*   **Indexed Icon Finder (MANDATORY):** 
    To avoid slow or outdated sequential searches, you must use the fast search engine over the SQLite database. **IT IS STRICTLY FORBIDDEN** to run manual SQL queries by writing inline terminal code like `python3 -c "import sqlite3; ..."` to connect to the database, and it is **FORBIDDEN** to run discovery or help commands (`--help`). You must exclusively use the authorized encapsulated script with its exact signatures.
    
    Authorized execution path based on current directory context:
    - **From the Plugin Root Directory:** `python3 skills/mermaid-designer/scripts/query_icons.py`
    - **From a Parent Workspace Directory:** `python3 jk-agy-mermaid/skills/mermaid-designer/scripts/query_icons.py`
    
    This script accesses the plugin's central SQLite cache and supports the following high-speed operational signatures:
    1.  **Batch Mode (MANDATORY for diagrams):**
        `python3 [path/to/]skills/mermaid-designer/scripts/query_icons.py --batch "<term 1>" "<term 2>" ...`
        *Description:* Resolves multiple concepts in a single agent turn. Returns a JSON map where each key is the search term and the value is the icon with the highest heuristic relevance and its full metadata. Abbreviations such as `--batc` are not allowed (it must be exactly `--batch`).
        *Example output:*
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
    2.  **Exact Code Query Mode:**
        `python3 jk-agy-mermaid/skills/mermaid-designer/scripts/query_icons.py --code "<exact icon code>"`
        *Description:* Returns the complete metadata of a unique icon in JSON format to verify if it is style-compatible (`is_style_compatible`), blacklisted (`is_blacklisted`), or has substitutes.

### C. Data Resources and Catalogs (Resources)
*   **JSON Icon Databases:**
    *   `resources/databases/gcp_icons.json` (Google Cloud Platform)
    *   `resources/databases/aws_icons.json` (Amazon Web Services)
    *   `resources/databases/azure_icons.json` (Microsoft Azure)
    *   `resources/databases/svg_logos.json` (SaaS, Brands, and Consolidated Technologies)
    *   `resources/databases/font_awesome_icons.json` (Standard Favicons)
*   **Encapsulated SQLite Index (`icons_cache.db`):** [resources/databases/icons_cache.db](resources/databases/icons_cache.db)
    *   *Usage:* Central SQLite database cache compiling all icon metadata including category, file path, line numbers, descriptions, style compatibility flags, blacklist flags, and recommended substitute codes. Future exceptions are written directly to this index.

---

## 2. Smart Activation and Triggers

This skill automatically activates when any of the following conversation contexts are detected:
*   Requests to create or modify architecture diagrams.
*   Requests for help with Mermaid syntax ("parsing error", "broken diagram", "does not render").
*   Mentions of GCP, AWS, Azure, Font Awesome icons, or Logos for visual representations.
*   Queries on how to sort, simplify, or structure complex data flows in networks or clouds.

---

## 3. Mandatory Operational Principles

1.  **Native UTF-8 (Spanish Resilience):** All scripts, files, and JSON databases of this skill must be read and written forcing UTF-8 encoding, ensuring that the plugin works regardless of whether the paths contain Spanish-specific characters (such as `/mnt/d/Gemini/Gráficas Mermaid`).
2.  **No Markdown-Wrappers on Export:** Any direct export or modification of `.mmd` files must be pure native Mermaid code, without wrapping it in Markdown code blocks (```), allowing external tools to render it directly.
3.  **Style Compliance and Exceptions:** Strictly apply the Zero-Style directive to multi-colored icons (AWS, Azure, Logos, and special GCP exceptions) to preserve the visual integrity of their SVGs, reserving aesthetic classes only for stable GCP and Font Awesome icons.
4.  **Strict Sibling Creation Policy:** When optimizing, improving, or refactoring an existing diagram (e.g., `folder/filename.mmd`), it is **strictly forbidden** to modify or overwrite the original file. Instead, you must **always create a new file** in the same folder as the original, renaming it with the suffix `_improved.mmd` or `_optimized.mmd` (e.g., `folder/filename_improved.mmd`).
5.  **Prohibition of Inline Icons and Use of Separate Native Syntax:** It is completely forbidden to use icon codes within node text or labels (such as `["fa:user Label"]`). You must strictly use separate native icon declaration syntax: `id["Label"]` and on the immediately following line `id@{ icon: "category:name" }`.
6.  **Prohibition of Yellow Backgrounds in Subgraphs and Explicit Styling:** It is **strictly forbidden** to leave subgraphs with Mermaid's default yellow background color (`#FBBC04` or `#fef7e0`). Every subgraph declared in the diagram must have its corresponding explicit styling directive declared at the end of the flowchart (e.g., `style SGId fill:#ffffff,stroke:#9E9E9E,stroke-width:2px`). If a subgraph remains yellow, it is considered a severe design error.

---

## 4. Ultra-Fast Zero-Exploration Workflow Guide

When invoked to create, modify, audit, or improve a Mermaid diagram in this workspace, **YOU ARE FORBIDDEN** to improvise, explore the file system, perform directory listings, or rewrite search scripts. You must strictly follow this 5-step consecutive flow and call only the indicated tools:

### Step 1: Read the Original Diagram (or Input File)
If the user provides an `.mmd` file or a path to improve, read it **immediately** using the `view_file` tool on its absolute path.
*   *Forbidden Action:* DO NOT list folders (`ListDir`) or perform file searches (`grep_search`) to locate the file.
*   *Tool:* `view_file` (e.g., `view_file {AbsolutePath: "/mnt/d/Gemini/.../file.mmd"}`)

### Step 2: Batch Icon Resolution (One-Shot Batching Policy)
Exhaustively analyze the diagram or input text. **YOU ARE FORBIDDEN** to make iterative or sequential refinement calls to search for icons or variants. You must plan and consolidate all information into **A SINGLE MASSIVE CALL** covering:
1.  **Literal Terms:** Specific diagram concepts (e.g., `"vpc service controls"`, `"notebook"`).
2.  **Technological Variants and Synonyms:** Different ways of naming the technology (e.g., `"entra id"`, `"entra-id"`, `"active directory"`).
3.  **Intuitive Brand Prefixes:** If you know it is GCP, Azure, AWS, or Font Awesome, add the prefix for an exact match (e.g., `"gcp:virtual-private-cloud"`, `"azure:entra-verified-id"`, `"fa:user"`, `"logos:flutter"`).
4.  **Fallback Generic Terms:** If the brand fails, generic concepts that can provide a semantically valid icon (e.g., `"user"`, `"mobile"`, `"search"`, `"shield"`, `"database"`).

*Example of Exhaustive Consolidation in a single call:*
`python3 jk-agy-mermaid/skills/mermaid-designer/scripts/query_icons.py --batch "user" "fa:user" "mobile app" "logos:flutter" "microsoft entra id" "azure:entra-verified-id" "active directory" "workload identity federation" "vpc service controls" "gcp:virtual-private-cloud" "gemini" "gcp:vertexai" "notebook" "search engine" "azure:search" "microsoft 365" "logos:microsoft" "bigquery" "gcp:bigquery" "shield" "database"`

*   *Forbidden Action:* DO NOT launch consecutive refinement calls. If you missed a term, it is a critical planning failure. Plan all terms and their variants before executing the tool. DO NOT list directories or query help commands.
*   *Tool:* `run_command` with the plugin's autonomous script.
*   *Exact Formula:*
    `python3 jk-agy-mermaid/skills/mermaid-designer/scripts/query_icons.py --batch "term1" "term2" "term3" "term4" ...`

### Step 3: Structuring and Applying Design Rules
Write the Mermaid code applying the following fixed design rules:
1.  **Premium Markdown Labels:** Format node text elegantly using `"`**Text**`"`.
2.  **Separated Icon Declaration:** Always declare the node on one line and its icon on the immediately following line:
    ```mermaid
    Id["`**Name**`"]
    Id@{ icon: "category:name" }
    ```
3.  **Zero-Style for External Brands:** If the query in Step 2 indicates that the icon has `"is_style_compatible": 0` (like AWS, Azure, and Logos logos), **DO NOT** apply any CSS styling class (neither `zeroStyle` nor colors). Leave them clean and transparent so they preserve their SVG intact.
4.  **Pastel Classes for GCP/FA:** If the icon has `"is_style_compatible": 1` (GCP and Font Awesome), you can associate the standard pastel classes (`:::gcpBlue`, `:::gcpGreen`, `:::gcpYellow`) defined at the end of the diagram.
5.  **Mandatory Styling for ALL Subgraphs:** Apply explicit styles at the end of the diagram for all subgraphs using **exclusivamente** one of these pastel combinations:
    *   *Client/External:* `style ID_SG fill:#ffffff,stroke:#9E9E9E,stroke-dasharray:5 5,stroke-width:2px;`
    *   *Security/Private:* `style ID_SG fill:#e6f4ea,stroke:#1E8E3E,stroke-width:2px;`
    *   *GCP Compute/Infrastructure:* `style ID_SG fill:#e8f0fe,stroke:#1967D2,stroke-width:2px;`
    *   *Support/Secondary:* `style ID_SG fill:#f9f9f9,stroke:#DADCE0,stroke-width:2px;`

### Step 4: Creating the Output File (Improved Suffix)
Write the new diagram in the same directory as the original with the suffix `_improved.mmd` using the `write_to_file` tool.
*   *Forbidden Action:* DO NOT overwrite the original file. DO NOT use Markdown code block backticks (```) inside the file.
*   *Tool:* `write_to_file` with `Overwrite: true`.

Follow this strict sequential flow. Any detour or unnecessary file exploration will be considered a runtime optimization failure.

---

## 5. Style Directives for Other Diagram Types

In addition to the `flowchart` format, this plugin formally supports **Sequence**, **Architecture (Beta)**, and **Class** diagrams, under strict premium design guidelines (Google Cloud Palette, White Canvas, zero yellow backgrounds, no Markdown wrapping code in `.mmd` files).

### A. Architecture Diagrams (Beta) (`architecture-beta`)

To represent network topologies, data flows, and physical architectures with native icon support, follow these directives:

1.  **Mandatory Structure and Initialization:**
    Every architecture diagram must begin with the `architecture-beta` clause and the following configuration header at the top:
    ```yaml
    ---
    config:
      fontFamily: Roboto, Arial, sans-serif
      theme: default
      themeVariables:
        fontFamily: Roboto, Arial, sans-serif
    ---
    ```
2.  **Critical Connection Syntax (Avoid Crashes):**
    *   **GOLDEN RULE:** Connections are defined **only** between `services` or `junctions`. **NEVER** connect lines to or from a `group` directly (causes an immediate parsing error in the rendering engine).
    *   **No Labels:** Do not use text labels on connection lines. Instead, use an explanatory comment `%%` on the previous line.
    *   **Simple Connection:** Do not use multiple connection syntax on a single line (e.g., `A --> B & C` is forbidden). Declare each connection on a separate line.
    *   **Character Restriction:** In `architecture-preview`, group or service labels must not contain special characters such as `:`, `-`, `(-)`, or accents.

3.  **Advanced Layout Patterns (Rendering Engine Control):**
    *   **External Actor Pattern:** Model external actors (such as users) as a `group` with an empty internal service `[ ]` as the connection anchor point.
    *   **Group Gateway Pattern:** To connect to services inside a group, place a `junction` inside the group to serve as a gateway (official entry point) and connect externally to that junction.
    *   **Connection Bus Pattern:** Use global `junction` nodes to group concurrent flows from multiple services and avoid spaghetti-like line crossings.
    *   **Spacer Connection Pattern:** If two complex adjacent groups overlap, define a `junction` in each and create an invisible connection between them using the `{group}` border property (e.g., `anchorA{group}:R -- L:anchorB{group}`) to force the engine to physically separate them.

---

### B. Sequence Diagrams (`sequenceDiagram`)

For step-by-step transactional and detailed messaging flows, follow these directives:

1.  **Standard Theme Configuration (Google Style - No Yellow):**
    It is mandatory to override the default yellow color of notes and activation bars in Mermaid. Place this block in the YAML frontmatter:
    ```yaml
    themeVariables:
      fontFamily: 'Roboto, Arial, sans-serif'
      primaryColor: '#4285F4'       # Google Blue
      mainBkg: '#ffffff'            # White Canvas
      signalColor: '#4285F4'        # Arrow color
      signalTextColor: '#4285F4'    # Arrow text color
      actorBorder: '#4285F4'
      activationBorderColor: '#4285F4'
      actorBkg: '#ffffff'           # White actor background
      activationBkgColor: '#ffffff' # White activation bar background
      noteBkgColor: '#e3f2fd'       # Light Blue (Google Style - Information Notes)
      noteBorderColor: '#1967D2'
    ```
2.  **Actor Definition and Emojis:**
    *   Use semantically representative unicode emojis for all participants (`👤` for users, `💻` for web, `📱` for mobiles, `🔐` for Auth, `☁️` for clouds, `🗄️` for databases).
    *   Define all participants clearly with short aliases and multi-line descriptive labels:
        ```mermaid
        participant User as 👤 User
        participant Web as 💻 Web App<br>(React)
        ```
3.  **Grouping Boxes (Boxes):**
    *   Group participants by logical domain using the `box` syntax.
    *   Force a pure white background by declaring `box rgb(255, 255, 255) "Group Name"`.

4.  **Semantic Transaction Blocks (Rects):**
    Highlight logical blocks according to their state using the `rect` syntax with the following specific colors:
    *   **Happy Path / Success:** `rect rgb(230, 255, 230)` (very pale green).
    *   **Error Handling / Failure:** `rect rgb(255, 235, 238)` (very pale red).
    *   **Informational / Security / Neutral:** `rect rgb(232, 240, 254)` (pale brand blue).

---

### C. Class Diagrams (`classDiagram`)

To model object-oriented software structures and code relationships, follow these directives:

1.  **Single-Line Initialization (Init Directive):**
    The technical initialization directive must be written compactly on the **first line of the file and on a single line** to guarantee compatibility with all versions of the Mermaid parser:
    ```
    %%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'Roboto', 'primaryColor': '#ffffff', 'mainBkg': '#ffffff', 'clusterBkg': '#ffffff', 'background': '#ffffff', 'edgeLabelBackground': '#ffffff'}}}%%
    ```
2.  **Clean and Hierarchical Topology:**
    *   Always declare the vertical direction: `direction TB`.
    *   The diagram must adjust to the required level of detail (Simplified/Executive, Complete, or Advanced). Hide trivial getters/setters or private plumbing details that do not add value.
    *   Avoid the spaghetti effect by limiting excessive relationship lines. Use notes or connect only to top-level classes.

3.  **Class Definition with Brand Styles (Google Cloud Palette):**
    Associate specific semantic color borders to classes based on their function. The background (`fill`) must always be `#ffffff`:
    *   **Core / Orchestrators:** Google Blue (`#4285F4`, border width `3px` or `2px`).
    *   **Helpers / Data Services:** Google Green (`#34A853`, `2px`).
    *   **Auth / Config / Security:** Google Yellow (`#FBBC04`, `2px`).
    *   **App Entry / Infra:** Google Grey (`#5F6368`, `2px`).
    *   **External / APIs:** Google Red (`#EA4335`, `2px`).

4.  **Mandatory Styling Syntax at the End:**
    *   Use the `:::class` assignment on the same line as the node definition and **declare all `classDef` definitions at the absolute end of the `.mmd` file** (after all relationships) to guarantee they correctly override the base theme in all viewers.
    *   Alternatively, for specific rendering environments, use the direct style method `style` at the end in the same way:
        ```
        style MyClass fill:#ffffff,stroke:#4285F4,stroke-width:2px,color:#000
        ```
