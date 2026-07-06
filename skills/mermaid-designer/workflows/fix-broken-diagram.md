# Workflow Guide: Recovery, Sanitization, and Syntactic Patching

This guide establishes the sequential protocol to diagnose, heal, and repair Mermaid diagrams that do not display, contain compilation errors, or show rendering warnings in the browser.

---

## Step 1: Triage and Syntactic Failure Capture
When the Mermaid renderer fails or the user reports that a diagram does not compile:
1.  **Capture the Error Message:** Identify the line and approximate token where the compiler failed (e.g., "Parse error on line 14: ...").
2.  **Identify the Diagram Type:** Check the first line of the diagram code to determine the active grammar:
    *   If it is `architecture-beta`, completely disable parenthesis escaping rules on native service elements.
    *   If it is `flowchart` or `graph`, enable strict parenthesis escaping in labels.

---

## Step 2: Line-by-Line Syntactic Analysis
Examine the diagram source code line by line to locate the 4 most common physical "bugs" in the production database:

### 1. Unescaped Parentheses in Node Labels (Flowcharts Only):
*   *Bug:* `nodeA[API Gateway (V2)]`
*   *Correction:* Replace the label wrapping with double quotes and backticks:
    `nodeA["`API Gateway (V2)`"]`

### 2. Unbalanced Quotes or Brackets:
*   *Bug:* `nodeB["Authentication Service` or `nodeC["Web App"}`
*   *Correction:* Balance the quotes and associate the correct node shape before classes:
    `nodeB["Authentication Service"]` or `nodeC["Web App"]`

### 3. Terminal Semicolons in linkStyle:
*   *Bug:* `linkStyle 5 stroke:#EA4335,stroke-width:2px;`
*   *Correction:* Systematically remove the trailing semicolon:
    `linkStyle 5 stroke:#EA4335,stroke-width:2px`

### 4. Unescaped Reserved Special Characters:
*   *Bug:* `nodeD["Clients > Servers & API < Databases"]`
*   *Correction:* Translate special characters to safe HTML entities or force double-quote backtick wrapping:
    `nodeD["`Clients &gt; Servers &amp; API &lt; Databases`"]`

---

## Step 3: Hierarchical Sanitization of Subgraphs
Review the structure of subgraphs to eliminate deformations in the ELK rendering engine:
1.  **Scan Nesting:** Count indentation levels and `subgraph` declarations.
2.  **Flatten Third Level:** If there are subgraphs declared inside a second-level subgraph, elevate all third-level components to the second level.
3.  **Safe Removal:** Remove the opening and closing statements of the third-level `subgraph` block.
4.  **Grouping by Style:** Associate the elevated components with unified style classes to maintain visual distinction on the canvas without degrading the layout geometry.

---

## Step 4: Rendering Tests and Aesthetic Integrity
Once the code has been healed:
1.  **Aesthetic Class Validation:** Ensure no classes with background color (`fill`) are applied to AWS, Azure, Logos, or excepted GCP icons (Zero-Style).
2.  **Warning Verification:** Verify that the code does not throw secondary syntactic warnings. The code must be 100% pure and immediate.
3.  **Clean Delivery:** Deliver the repaired code to the user in a native code block, detailing which sanitization rules were applied in the report.
