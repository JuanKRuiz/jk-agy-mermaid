# Professional Mermaid Diagram Style & Presentation Rule

This directive establishes the mandatory aesthetic, contrast, and colorization standards for all diagrams in the workspace. Any agent or script that generates or edits Mermaid code must strictly adhere to these specifications.

---

## 1. Brand Color Palette & Contrast Formulas

To guarantee industrial readability of nodes, custom style classes with pastel backgrounds and high-saturation solid borders must be used. The font color **MUST** always be forced to pure black (`color:#000`) or pure white (`color:#fff`) to override browser gray inheritance.

```mermaid
%% Standard Design Class Declarations
classDef gcpBlue fill:#E8F0FE,stroke:#1967D2,stroke-width:2px,color:#000,font-family:Roboto;
classDef gcpGreen fill:#E6F4EA,stroke:#1E8E3E,stroke-width:2px,color:#000,font-family:Roboto;
classDef gcpYellow fill:#FEF7E0,stroke:#B06000,stroke-width:2px,color:#000,font-family:Roboto;
classDef gcpRed fill:#FCE8E6,stroke:#D93025,stroke-width:2px,color:#000,font-family:Roboto;
classDef neutral fill:#F1F3F4,stroke:#5F6368,stroke-width:2px,color:#000,font-family:Roboto;
```

*   **GCP Blue (Web, General Traffic, API, Compute):** `fill:#E8F0FE,stroke:#1967D2,stroke-width:2px,color:#000`
*   **GCP Green (Private Network, VPN, Security, Secure Databases):** `fill:#E6F4EA,stroke:#1E8E3E,stroke-width:2px,color:#000`
*   **GCP Yellow (Authentication, IAM, Third-party, External Providers):** `fill:#FEF7E0,stroke:#B06000,stroke-width:2px,color:#000`
*   **GCP Red (Failure, Alert, Block, Critical Return):** `fill:#FCE8E6,stroke:#D93025,stroke-width:2px,color:#000`
*   **Neutral (Secondary, Redundant, or Support Elements):** `fill:#F1F3F4,stroke:#5F6368,stroke-width:2px,color:#000`

---

## 2. Mandatory Header Configuration (YAML Frontmatter) & ELK Layout

Every Mermaid diagram generated or edited in this project **MUST** start with a header in **YAML Frontmatter** format (delimited by three hyphens `---` at the beginning and the end).

*   **STRICT PROHIBITION:** It is **absolutely forbidden** to use the old Mermaid initialization syntax of style `%%{init: ...}%%` to define base configurations or theme variables (`themeVariables`).
*   **DEFAULT LAYOUT:** The default spatial distribution and rendering engine **MUST** always be `elk` (`layout: elk`), as it guarantees order and clarity for complex architectures.
*   **COMPLETE STANDARD CONFIGURATION:**
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
    *(The `edgeLabelBackground: '#ffffff'` variable is mandatory to inject a protective white background behind line connector labels).*

---

## 3. "Zero-Style" Rule for AWS, Azure, Logos, and Excluded GCP (Icons as Brands)

It is **strictly forbidden** to apply style classes that define background color (`fill`) or border (`stroke`) to nodes representing brands or using vector icons of:
1.  **AWS** (`aws:*`)
2.  **Azure** (`azure:*`)
3.  **Logos** (`logos:*`, e.g., `logos:google-gemini`, `logos:salesforce`, `logos:mongodb`, `logos:kubernetes`)
4.  **GCP Exceptions** with complex vector gradients and 3D shadows (such as `gcp:cloud-load-balancing`, `gcp:private-service-connect`, and `gcp:advanced-agent-modeling`).

**Justification:** These icons are **registered trademarks** and have complex pre-defined internal vector structures and chromatic identities. Injecting a CSS class with background (`fill`) or border (`stroke`) overrides and interferes with the SVG path rendering, "flattening" the image into a solid opaque block (black, blue, or gray) and ruining the visualization.

**Implementation Standard:**
*   The safest and recommended way is **NOT to apply any class suffix** (e.g., `:::class`) to these nodes. The node will inherit a transparent neutral background and display the logo perfectly.
*   *Correct:*
    ```mermaid
    AppGemini["`**Gemini Enterprise**<br>Web App`"]
    AppGemini@{ icon: "logos:google-gemini" }
    ```
*   *Incorrect (Prohibited style filling on brands):*
    ```mermaid
    AppGemini["`**Gemini Enterprise**<br>Web App`"]:::gcpYellow
    AppGemini@{ icon: "logos:google-gemini" }
    ```
*   If exceptionally a typography, size, or thickness style is required, use a class free of `fill` and `stroke` properties:
    ```mermaid
    classDef neutralZeroStyle color:#000,stroke-width:2px,font-family:Roboto;
    ```

---

## 4. Visual Waypoint (Teleporter) Design & Color Palette

Visual teleportation waypoints must look consistent and professional. They are declared using triple parentheses (concentric circular shape) and a single uppercase letter or number (e.g., `wpA(((A))):::wp_blue`).

### Mandatory Color Palette for Waypoints:
*   **Web / API / General Traffic (GCP Blue):**
    `classDef wp_blue fill:#1A73E8,stroke:#0D47A1,stroke-width:2px,color:#fff,font-weight:bold;`
*   **Security / VPN / Private Network (GCP Green):**
    `classDef wp_green fill:#34A853,stroke:#1B5E20,stroke-width:2px,color:#fff,font-weight:bold;`
*   **Authentication / Identity / IAM (GCP Yellow):**
    `classDef wp_yellow fill:#FBBC04,stroke:#F29900,stroke-width:2px,color:#000,font-weight:bold;`
*   **Alert / Failure / Return (GCP Red):**
    `classDef wp_red fill:#EA4335,stroke:#C5221F,stroke-width:2px,color:#fff,font-weight:bold;`
*   **Data Layer / Persistence / AWS (AWS Squid / Dark):**
    `classDef wp_dark fill:#232F3E,stroke:#000,stroke-width:2px,color:#fff,font-weight:bold;`

---

## 5. Mandatory Native Syntax for Icons (Prohibition of Inline Icons)

To guarantee that icons render with maximum fidelity and do not break node geometries, the following mandatory syntactic rule is established:

1.  **STRICT PROHIBITION OF INLINE ICONS IN LABELS:**
    *   It is **totally forbidden** to inject icon codes (such as `fa:`, `gcp:`, `azure:`, `logos:`) inside the node text or label (e.g., `node["fa:circle-user <br> Label"]` or `node["`azure:mobile` <br> **Label**"]`).
    *   *Reason:* Inline icon labels cause severe visual alignment failures, distort the text box, and are incompatible with modern Mermaid layout engines.

2.  **MANDATORY SEPARATE DECLARATION SYNTAX:**
    *   All icons must be declared autonomously and independently on the line immediately subsequent to the node definition, using the syntax:
        ```mermaid
        id["`**Node Label**`"]:::styleClass
        id@{ icon: "category:icon-name" }
        ```
    *   *Correct Example:*
        ```mermaid
        FinalUser["`**First Line User**`"]:::gcpBlue
        FinalUser@{ icon: "fa:user" }
        ```
    *   *Incorrect Example (FORBIDDEN):*
        ```mermaid
        FinalUser["`fa:circle-user` <br> **First Line User**"]
        ```

---

## 6. Prohibition of Default Subgraph Yellow Backgrounds & Zone Semantics

Subgraph colorization is not a decorative element; it represents the operational and security nature of the infrastructure outlined in the blueprint.

*   **STRICT PROHIBITION (NO DEFAULT YELLOW):** It is **strictly forbidden** for a subgraph to adopt Mermaid's default background yellow color (`#FBBC04` / `#fef7e0`). If a subgraph renders in default yellow, it is a **severe design error** that violates corporate standards. All subgraphs must have explicit styles applied according to their semantics.
*   **OBLIGATION TO DECLARE EXPLICIT STYLE (MANDATORY SYNTAX):**
    To override Mermaid's default yellow background, **you must add** a `style <SubgraphId>` styling directive at the end of the file for each subgraph declared in the diagram. Omitting this directive in any subgraph is not allowed.
*   **ZONE STYLING NARRATIVE SEMANTICS AND SYNTAX EXAMPLES:**
    1.  **Platform Unified (Managed / GCP Cloud):**
        *   *Meaning:* Managed, robust physical or PaaS infrastructure (secure cloud environments).
        *   *Style:* Soft Brand Background (GCP Blue `#e8f0fe` or GCP Green `#e6f4ea`) with saturated solid brand borders.
        *   *GCP Blue Syntax:* `style SUBGRAPH_ID fill:#e8f0fe,stroke:#1967D2,stroke-width:2px`
        *   *GCP Green Syntax (Secure DB / Network):* `style SUBGRAPH_ID fill:#e6f4ea,stroke:#1E8E3E,stroke-width:2px`
    2.  **Logical/External / Zero Trust Zones:**
        *   *Meaning:* Logical access zones, ephemeral perimeters, external providers, or on-premises networks under zero trust.
        *   *Style:* Pure White Background (`#ffffff`) with dashed or dotted gray border.
        *   *Syntax:* `style SUBGRAPH_ID fill:#ffffff,stroke:#9E9E9E,stroke-dasharray:5 5,stroke-width:2px`
    3.  **Neutral or Generic Zones:**
        *   *Meaning:* Generic groupers or secondary infrastructure.
        *   *Style:* Soft light gray (`#f9f9f9`) or Pure White (`#ffffff`) with solid gray border.
        *   *Gray Syntax:* `style SUBGRAPH_ID fill:#f9f9f9,stroke:#DADCE0,stroke-width:2px`
        *   *White Syntax:* `style SUBGRAPH_ID fill:#ffffff,stroke:#DADCE0,stroke-width:2px`
    4.  **Forbidden / Default Yellow:**
        *   *Action:* Any subgraph that ends up with the default yellow background must be re-styled immediately to one of the options above. No subgraph without explicit styling will be tolerated.

---

## 7. Strict Limitation to Database-Supported Icons (MANDATORY)

To ensure consistency, portability, and reliable rendering within the offline execution limits of the Antigravity system, a strict rule for brand and typography icons is established:

*   **DATABASE ONLY REQUIREMENT:** It is **strictly prohibited** to use any icon (whether it is Font Awesome `fa:*`, Cloud `gcp:*`/`aws:*`/`azure:*`, or logo `logos:*`) that does not physically exist in the pre-populated SQLite database index (`icons_cache.db`).
*   **REJECTION OF EXTERNAL OR DEPRECATED ICONS:** Any diagram utilizing an icon not present in the database violates compliance and **must be rejected** by the auditor.
*   **VERIFICATION PROCESS:** Before applying any icon, the agent or script must query the code via `query_icons.py --code <icon_code>` or search terms via `query_icons.py --batch "<term>"` to verify its existence and fetch its compliance attributes (e.g., `is_style_compatible` or `is_blacklisted`).



