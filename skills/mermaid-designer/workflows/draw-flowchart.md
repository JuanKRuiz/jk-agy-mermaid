# Workflow Guide: High-Fidelity Flowchart Design and Construction

This interactive guide establishes the mandatory logical steps to design, structure, and diagram technology architectures from scratch using the Mermaid Flowchart syntax.

---

## Step 1: Requirements Analysis and Network Topology
Before drawing a single line of code, analyze the provided technical input:
1.  **Main Components:** Identify servers, load balancers, databases, network gateways, and clients.
2.  **Hierarchical Boundaries:** Group components into layers or logical zones (e.g., Public Network, Private Network, Data Layer).
3.  **Data Flows:** Define relationships and communication protocols between components.

---

## Step 2: Canvas Setup and Theme Variables
Every professional diagram must start with a standard initialization header to configure the base typography, edge label background, and layout orientation:

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
flowchart TD
```

*   **Default Orientation:** Use `flowchart TD` (Top-Down) for diagramming network architectures or logical layers, as it distributes subgraphs in a much more readable manner than horizontal `LR` orientation.

---

## Step 3: Service Icon Lookup and Validation (High-Speed Batching)
To equip the diagram with industrial-grade brand presence, search for official icons in a consolidated manner:
*   **Execution (Mandatory Batching):** Extract the list of all required node concepts and make **a single batch call** to the search engine using the `--batch` flag (it is strictly forbidden to execute manual SQL queries with `python3 -c "import sqlite3; ..."` from the terminal, or to use help or incomplete commands):
    `python3 [path/to/]skills/mermaid-designer/scripts/query_icons.py --batch "load balancer" "lambda" "database"`
    This will instantly return a JSON map mapping each concept to its best icon, including metadata like `is_style_compatible` and `substitute_code`.
*   **Automatic Filtering:** The SQLite search engine automatically filters out icons marked as blacklisted (`is_blacklisted = 1`) inside the `icons_cache.db` index.
*   **Database Attribute Support:** Use the `--code <code_string>` parameter in `query_icons.py` to verify style compatibility or special icon notes directly from the database.

---

## Step 4: Structuring and Limited Subgraphs (Flattening)
Draw container subgraphs respecting the strict hierarchy limit to prevent the ELK engine from collapsing:
*   **Limit:** Maximum **2 depth levels**.
*   **Syntax:**
    ```mermaid
    subgraph VPC ["Virtual Private Cloud (Prod)"]
        subgraph SubnetPrivada ["Private Subnet (10.0.1.0/24)"]
            instancia1["`**App Server 1**`"]:::gcpBlue
            instancia1@{ icon: "gcp:compute-engine" }
        end
    end
    ```

---

## Step 5: Topological Simplification (Teleportation and Junction Bus)
If the diagram begins to get cluttered with crossed connectors (spaghetti effect), evaluate mathematical triggers to simplify the canvas:

1.  **Teleportation with Waypoints (Crossings > 4 or Boundaries > 1):**
    Instead of crossing a physical arrow through multiple intermediate zones, declare local circular teleportation ports at the source and destination:
    *   At source: `server --> wp1(((1))):::wp_blue`
    *   At destination: `wp2(((1))):::wp_blue --> database`
2.  **Junction Bus Pattern (Architecture-Beta or dense Flowcharts):**
    For parallel connections pointing to a single recipient, create a linear sequence of `junction` connections within the receiving subgraph to consolidate traffic into a single orderly line, eliminating crossed arrows.

---

## Step 6: Colorization Styles and Final Zero-Style
Apply final aesthetic touches at the end of the diagram file:
1.  **Pastel Color Classes:** Associate the corresponding classes for stable GCP or Font Awesome icons (e.g., `:::gcpBlue`, `:::gcpGreen`).
2.  **Zero-Style Rule:** Leave nodes with AWS, Azure, and Logos icons in their neutral format with no background color (associating `:::awsStyle` if necessary) to ensure the render of their SVGs is not ruined.
3.  **Connector Contrast Formulas:** Define specific high-contrast `linkStyle` rules for connectors representing failures (red), secure links (green), or general traffic (blue).
4.  **Mandatory Subgraph Styling (No Yellow):** Every subgraph declared in the diagram must explicitly receive a style to prevent Mermaid from coloring it yellow `#FBBC04`/`#FEF7E0` by default. Declare these directives at the end of the file in the following format:
    `style <SubgraphId> fill:#ffffff,stroke:#9E9E9E,stroke-width:2px` (for external/white zones)
    `style <SubgraphId> fill:#e8f0fe,stroke:#4285F4,stroke-width:2px` (for GCP/blue zones)
    `style <SubgraphId> fill:#e6f4ea,stroke:#34A853,stroke-width:2px` (for private/green zones)
    `style <SubgraphId> fill:#f9f9f9,stroke:#DADCE0,stroke-width:2px` (for generic/neutral zones)
