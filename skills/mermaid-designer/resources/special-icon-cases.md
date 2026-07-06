# Central Exception Registry: Special Icon Cases

This file is the single, centralized, and portable source of truth for all Mermaid vector icon rendering anomalies, design-exclusion rules (Zero-Style exceptions), and deprecation blacklists. It is designed to be easily read, parsed, and updated by both humans and autonomous agents (such as `mermaid-learner`).

---

## 1. Icons with Vector Problems (Zero-Style Rule)

The following icons are **strictly forbidden** from receiving background/fill styling classes (such as `:::gcpBlue` or `:::gcpGreen`) because they contain multi-color vector paths, pre-defined brand gradients, or 3D drop-shadows. Styling them overrides their SVG paths and flattens them into a solid block:

*   **Google Cloud Platform (GCP) Exceptions:**
    *   `gcp:cloud-load-balancing` (complex gradient / multi-color path)
    *   `gcp:private-service-connect` (complex gradient / multi-color path)
    *   `gcp:advanced-agent-modeling` (complex gradient / multi-color path)
*   **Amazon Web Services (AWS) Icons:**
    *   All icons matching `aws:*`
*   **Microsoft Azure Icons:**
    *   All icons matching `azure:*`
*   **Tech Logos / SaaS Icons:**
    *   All icons matching `logos:*` (e.g., `logos:google-gemini`, `logos:salesforce`, `logos:mongodb`, `logos:kubernetes`)

*Implementation Note:* Any node utilizing these icons must remain clean and transparent (zero-style) or use a typography-only CSS class.

---

## 2. Recommended Substitutions and Replacements

When a specific technology does not have a dedicated icon in the library, or when the existing icon is visually unappealing, the following standard substitutions should be used:

| Original Term / Concept | Attempted Code | Recommended Substitute Code | Justification |
| :--- | :--- | :--- | :--- |
| **Weaviate** | `logos:weaviate` | `logos:pinecone` | Weaviate is missing; Pinecone represents high-fidelity vector databases. |
| **Milvus** | `logos:milvus` | `logos:pinecone` | Milvus is missing; Pinecone represents high-fidelity vector databases. |
| **Elasticsearch** | `logos:elasticsearch` | `fa:database` | Resolves database search concepts using high-contrast Font Awesome fallback. |
| **Anthropic** | `logos:anthorpic` | `logos:google-gemini` | Corrects typo/missing icon to active LLM partner. |

---

## 3. Exclusion List (Blacklist)

The following icon codes are completely disabled and **must not** be generated because they are non-existent, deprecated, or corrupted in the current libraries:

*   `logos:weaviate` (Non-existent in SVG Logos library)
*   `logos:milvus` (Non-existent in SVG Logos library)
*   `logos:elasticsearch` (Corrupted SVG vectors / rendering failure)
*   `logos:anthorpic` (Typo of Anthropic / Non-existent)
*   `gcp:obsolete-service` (Deprecated cloud component)

---

## 4. How Agents Interact with this Registry

1.  **Read & Match:** Before applying color classes, the `mermaid-auditor` parses this file's lists. If the selected icon matches any entry in Section 1, the styling class is stripped.
2.  **Autonomous Learning Loop:** When a glitch is reported (e.g., "icon `X` renders as a black box"), the `mermaid-learner`:
    *   Appends `X` to the bulleted list under Section 1.
    *   Hot-patches the affected `.mmd` diagram.
    *   Triggers re-indexing of the SQLite database (`icons_cache.db`) so `is_style_compatible` is updated to `0` for `X` in microseconds.
