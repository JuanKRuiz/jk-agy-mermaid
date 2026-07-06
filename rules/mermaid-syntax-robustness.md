# Syntactic Robustness, Escaping, & Error Prevention Rule

This directive establishes the immutable syntactic standards and pre-validation logic (Linter) that every Mermaid code generator or corrector in the plugin must apply to guarantee diagrams 100% free of compilation failures in the renderer.

---

## 0. Phase 0: Pre-Existing Diagram Sanitization First (MANDATORY)

When working on an already created or pre-existing Mermaid diagram:
*   **IMMEDIATE ACTIVATION:** The syntactic linter (`mermaid-linter-fixer` subagent) must be activated **immediately as the absolute first step**.
*   **RATIONALE:** Pre-existing syntax errors must be completely resolved and healed before any new changes, brand icons, waypoint structures, or custom styling classes are applied. Modifying a broken diagram without first sanitizing it results in compounding parsing failures.

---

## 1. The Auto-Heal Algorithm (Syntactic Error Correction)

Any generated or corrected Mermaid code block must be subjected to the following structured sanity table:

| # | Detected Syntactic Error | Cause of Parser Failure | Required Automatic Correction Logic |
| :--- | :--- | :--- | :--- |
| **1** | **Parentheses inside Labels** <br>E.g., `Node[API (v1)]` | The engine interprets parentheses as physical definitions of circular/elliptical node shapes. | **Escape with Markdown String:** Wrap the entire content in double quotes and backticks: `` "`API (v1)`" `` or remove them if they are in subgraph names. |
| **2** | **Unbalanced Quotation Marks** <br>E.g., `node1["Label'}` | The parser expects the closure of a string literal. If not found, it crashes. | **Strict Balancing Regex:** Scan for quote openings and ensure the exact homologous closure before the end of the node or the class (`:::`). |
| **3** | **Semicolon at the end of `linkStyle`** <br>E.g., `linkStyle 3 stroke:#333;` | The `linkStyle` syntax in Mermaid does not support a trailing semicolon. The parser throws an error. | **Suffix Cleanup:** Remove via regex any semicolon `;` at the end of lines starting with `linkStyle`. |
| **4** | **Unescaped Special Characters** <br>E.g., `node["A > B & C < D"]` | The `>`, `<`, `&`, and `/` characters are reserved tokens for connectors or HTML injection. | **String Standardization:** Translate to safe entities (`&amp;`, `&lt;`, `&gt;`) or force comilla-backtick wrapping. |
| **5** | **Invalid or Mixed Connectors** <br>E.g., `--.-`, `-->|label|-->` | Line styles that do not belong to the Mermaid standard or spurious combinations of ELK layouts. | **Arrow Standardization:** Normalize exclusively to the 4 supported types:<br>- Standard solid: `-->`<br>- Thick solid: `==>`<br>- Dotted: `-.->`<br>- Invisible: `~~~` |
| **6** | **Inline Icons in Labels** <br>E.g., `node["fa:user Label"]` or `node["`gcp:storage` <br> Label"]` | Breaks geometry, causes severe misalignment, or renders incorrectly as plain text. | **Conversion to Separate Declaration:** Extract the icon code from the label and declare the icon independently on a new line using native Mermaid syntax: `node@{ icon: "category:icon-name" }`. |

---

## 2. Grammar Discrimination: `flowchart` vs `architecture-beta`

The sanitization engine must preventatively identify the diagram type before applying parenthesis escaping rules:

1.  **Detection:** If the source code begins with the `architecture-beta` keyword, Rule 1 (parenthesis escaping) is immediately **DISABLED**.
2.  **The Reason:** In beta architecture diagrams, parentheses are natively used to declare services, groups, and icons (e.g., `group client(fa:user)` or `service backend(gcp:cloud-run)`). Escaping these parentheses would corrupt the native syntax of this specification.
3.  **Execution:** Parenthesis escaping in labels only applies when the diagram type is `flowchart` or `graph`.

---

## 3. Hierarchy Control & Subgraph Flattening

To avoid visual distortion, box overlapping, and broken borders in the ELK layout engine:

1.  **Nesting Limit:** A maximum depth of **2 levels of subgraphs** is established. It is forbidden to nest a subgraph inside another second-level subgraph.
2.  **Logical Flattening:** If the design requires more levels (e.g., VPC -> Subnet -> Pod), the code must be flattened to a maximum of 2 hierarchical levels of subgraphs, representing internal hierarchies by grouping nodes with unified color classes or outlines, or aligning them with invisible links (`~~~`).
3.  **Invisible Stacking Links:** To force ELK to stack subgraphs or layers in an orderly top-to-bottom manner without forcing fake arrow markers:
    ```mermaid
    UserLayer ~~~ SecurityLayer ~~~ DataLayer
    ```
    And at the end of the file, hide the line so it doesn't render visually:
    `linkStyle INDEX stroke-width:0px,fill:none`
