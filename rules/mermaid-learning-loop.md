# Permanent Auto-Adaptive Learning Loop Rule

This directive establishes the formal and immutable protocol that the `mermaid-learner` subagent must follow autonomously to register icon rendering errors, update knowledge databases, and hot-patch diagrams, ensuring adaptive immunity against visual glitches.

---

## 1. The 5-Step Learning Protocol

When the user reports an icon rendering glitch (e.g., "the logos:weaviate icon is not visible" or "icon X has a black block around it"), the agent **MUST** execute the following sequence without requiring manual design confirmation:

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant Learner as mermaid-learner Agent
    participant Config as special-icon-cases.md
    participant TargetMMD as Diagram in Development (.mmd)

    User->>Learner: "The logos:weaviate icon shows as '?' or has coloring issues"
    
    rect rgb(240, 245, 255)
        note over Learner: Step 1: Glitch Analysis and Classification
        Learner->>Learner: Classify error:<br>- Missing Icon<br>- Vector Interference (Zero-Style Required)
    end

    alt Scenario A: Non-existent icon (Code ?)
        note over Learner: Step 2: Indexed Search for Substitute
        Learner->>Learner: Execute query on SQLite DB (grep_search)
        Learner->>Config: Record obsolete icon in section 3 (Blacklist) with reason and substitute
        Learner->>TargetMMD: Hot-patch the .mmd replacing the obsolete icon
    else Scenario B: Coloring interference (Black / Opaque Box)
        Learner->>Config: Record icon code in section 1 (Zero-Style Exceptions)
        Learner->>TargetMMD: Hot-patch the .mmd removing the color class
    end

    note over Learner: Step 5: Report Generation & Re-indexing
    Learner->>Learner: Recompile SQLite database to apply changes in microseconds
    Learner->>User: Present learning report, updated special-icon-cases.md, and .mmd change diff
```

---

## 2. Protocol Steps Detail

### Step 1: Interception and Classification of the Glitch
Analyze the reported symptom to classify the error into one of these two categories:
*   **Type A (Missing Icon / `?`):** The icon code is not found in Mermaid's active libraries or has been renamed/deprecated.
*   **Type B (Contrast Glitch / Black Box):** The icon renders, but appears distorted, covered by the node's background color, or inside a solid block due to the CSS injection of an inappropriate class.

### Step 2: Finding a Viable Alternative (For Type A)
Using exclusively the authorized native command tool `python3 [path/to/]skills/mermaid-designer/scripts/query_icons.py --batch "<term>"` or `grep_search` over local databases, the agent must perform queries for similar keywords (e.g., if Weaviate fails, search for "vector database" or "pinecone"). **It is strictly forbidden** to run manual SQLite SQL queries with `python3 -c "import sqlite3; ..."` from the terminal, or to use unsupported/help flags.

### Step 3: Updating Plugin Knowledge Assets
The agent must perform hot modifications on the unified configuration file:
*   **Type A:** Add the disapproval entry under section "**3. Exclusion List (Blacklist)**" of `skills/mermaid-designer/resources/special-icon-cases.md` detailing the reason and suggested alternative.
*   **Type B:** Add the icon identifier or exact pattern under section "**1. Icons with Vector Problems (Zero-Style Rule)**" of `skills/mermaid-designer/resources/special-icon-cases.md`, permanently forbidding any association with background color styles.

### Step 4: Hot-Patching the Diagram (.mmd)
The agent opens the affected `.mmd` file and applies the exact corrective measure (replaces the icon with the substitute, or removes the background color class from the node).

### Step 5: Re-Indexing and Professional Report
*   Execute `python3 [path/to/]skills/mermaid-designer/scripts/index_icons.py` (if applicable) or query tools to ensure SQLite database reflects changes.
*   Present a confirmation to the user detailing:
    1.  Which knowledge assets were updated (`skills/mermaid-designer/resources/special-icon-cases.md`).
    2.  Why this technical decision was made.
    3.  A **Git Diff** block showing exactly the changes made to the source diagram `.mmd` file.
