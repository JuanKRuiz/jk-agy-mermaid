#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
High-Speed Icon Query Engine for the Plugin (query_icons.py)
Author: Antigravity

This script exclusively performs optimized microsecond-level queries 
on the pre-populated shared SQLite cache (icons_cache.db). It is 100% autonomous, 
lightweight, and free of indexing dependencies or residual development code.
"""

import os
import sys
import json
import sqlite3
from pathlib import Path

# Category configuration and priorities
CATEGORY_ORDER = [
    ("Cloud Providers (Priority 1)", "cloud"),
    ("SVG Logos (Priority 2)", "svg"),
    ("Font Awesome (Fallback - Priority 3)", "font_awesome"),
    ("Others", "other")
]

def clean_code(code_str):
    """
    Cleans the icon code from backticks and quotes.
    E.g.: "`gcp:compute-engine`" -> "gcp:compute-engine"
    """
    return code_str.replace("`", "").replace("'", "").replace('"', "").strip()

def get_icon_by_code(conn, icon_code):
    """
    Retrieves complete information of an icon by its exact code.
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT category, file_path, line_num, name, code, description, is_style_compatible, is_blacklisted, substitute_code, special_notes
            FROM icons
            WHERE code = ?
        """, (icon_code,))
        row = cursor.fetchone()
        if row:
            return {
                "category": row[0],
                "file": row[1],
                "line_num": row[2],
                "name": row[3],
                "code": row[4],
                "description": row[5],
                "is_style_compatible": row[6],
                "is_blacklisted": row[7],
                "substitute_code": row[8],
                "special_notes": row[9]
            }
    except sqlite3.Error:
        pass
    return None

def calculate_relevance(item, query_words):
    def normalize(text):
        return text.lower().replace("-", " ").replace(":", " ").strip()
        
    code_norm = normalize(item["code"])
    name_norm = normalize(item["name"])
    desc_norm = normalize(item["description"])
    
    score = 0
    query_str = " ".join(query_words)
    query_norm = normalize(query_str)
    
    if query_norm == name_norm or query_norm == code_norm:
        score += 1000
    elif query_norm in name_norm:
        score += 500
    elif query_norm in code_norm:
        score += 300
        
    for word in query_words:
        word_norm = normalize(word)
        if not word_norm:
            continue
            
        if word_norm == name_norm or f" {word_norm} " in f" {name_norm} ":
            score += 100
        elif word_norm in name_norm:
            score += 50
            
        if word_norm == code_norm or f" {word_norm} " in f" {code_norm} ":
            score += 80
        elif word_norm in code_norm:
            score += 40
            
        if f" {word_norm} " in f" {desc_norm} ":
            score += 20
        elif word_norm in desc_norm:
            score += 10
            
    return score

def query_single(conn, query_words):
    cursor = conn.cursor()
    results = {cat: [] for _, cat in CATEGORY_ORDER}
    
    conditions = []
    params = []
    for word in query_words:
        conditions.append("search_text LIKE ?")
        params.append(f"%{word}%")
        
    where_clause = " AND ".join(conditions)
    
    query = f"""
        SELECT category, file_path, line_num, name, code, description, is_style_compatible, substitute_code, special_notes 
        FROM icons 
        WHERE {where_clause} AND is_blacklisted = 0
        ORDER BY id ASC
    """
    
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        for row in rows:
            cat, file_path, line_num, name, code, description, style_comp, subst_code, notes = row
            results[cat].append({
                "file": file_path,
                "line_num": line_num,
                "name": name,
                "code": code,
                "description": description,
                "is_style_compatible": style_comp,
                "substitute_code": subst_code,
                "special_notes": notes
            })
            
        for cat in results:
            results[cat].sort(key=lambda item: calculate_relevance(item, query_words), reverse=True)
            
    except sqlite3.Error:
        pass
        
    return results

def map_to_display_category(db_cat, file_path):
    """
    Maps the database category to traditional readable names.
    """
    fp_lower = file_path.lower()
    if db_cat == "cloud":
        if "gcp" in fp_lower:
            return "Google Cloud Platform (GCP)"
        elif "aws" in fp_lower:
            return "Amazon Web Services (AWS)"
        elif "azure" in fp_lower:
            return "Microsoft Azure"
        return "Cloud Providers"
    elif db_cat == "svg":
        return "SVG Logos (Technologies, SaaS, Languages)"
    elif db_cat == "font_awesome":
        return "Font Awesome"
    return "Others"

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Standard Search: python3 query_icons.py <search_term...>")
        print("  Batch Search:    python3 query_icons.py --batch <term 1> <term 2> ...")
        print("  Code Query:      python3 query_icons.py --code <exact_icon_code>")
        sys.exit(1)

    is_batch = sys.argv[1] == "--batch"
    is_code = sys.argv[1] == "--code"

    # Determine plugin database file path in an encapsulated manner
    script_dir = Path(__file__).resolve().parent
    db_path = (script_dir / ".." / "resources" / "databases" / "icons_cache.db").resolve()

    if not db_path.exists():
        print(f"Error: Pre-populated SQLite database was not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    # Connect to the SQLite cache database
    try:
        conn = sqlite3.connect(db_path)
    except Exception as e:
        print(f"Error connecting to SQLite database at {db_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if is_batch:
        batch_terms = sys.argv[2:]
        batch_results = {}

        for term in batch_terms:
            query_words = [w.lower() for w in term.split() if w.strip()]
            if not query_words:
                continue

            results = query_single(conn, query_words)

            best_match = None
            for _, cat in CATEGORY_ORDER:
                if results.get(cat):
                    best_match = results[cat][0]
                    break

            batch_results[term] = best_match

        print(json.dumps(batch_results, indent=2, ensure_ascii=False))

    elif is_code:
        if len(sys.argv) < 3:
            print("Error: An icon code must be specified. E.g.: python3 query_icons.py --code logos:salesforce", file=sys.stderr)
            conn.close()
            sys.exit(1)

        icon_code = sys.argv[2].strip()
        icon_data = get_icon_by_code(conn, icon_code)
        print(json.dumps(icon_data, indent=2, ensure_ascii=False))

    else:
        term_str = " ".join(sys.argv[1:])
        query_words = [w.lower() for w in term_str.split() if w.strip()]

        if not query_words:
            print("Error: Empty search terms.", file=sys.stderr)
            conn.close()
            sys.exit(1)

        print(f"Searching for: '{term_str}' in the SQLite icon cache...")
        print("-" * 80)

        results = query_single(conn, query_words)
        matches_by_display = {}
        total_found = 0

        for cat, items in results.items():
            for item in items:
                disp_cat = map_to_display_category(cat, item["file"])
                if disp_cat not in matches_by_display:
                    matches_by_display[disp_cat] = []
                matches_by_display[disp_cat].append(item)
                total_found += 1

        display_order = [
            "Google Cloud Platform (GCP)",
            "Amazon Web Services (AWS)",
            "Microsoft Azure",
            "Font Awesome",
            "SVG Logos (Technologies, SaaS, Languages)",
            "Others"
        ]

        for disp_cat in display_order:
            matches = matches_by_display.get(disp_cat, [])
            if matches:
                print(f"\n[ Category: {disp_cat} - {len(matches)} matches ]")
                print("-" * 80)
                for idx, item in enumerate(matches[:15], 1):
                    print(f"  {idx}. Name:        {item.get('name')}")
                    print(f"     Code:        `{item.get('code')}`")
                    print(f"     Detail:      {item.get('description')}")
                    if item.get("is_style_compatible") == 0:
                        print("     Style:       [Zero-Style Required - No coloring class]")
                    if item.get("substitute_code"):
                        print(f"     Substitute:  `{item.get('substitute_code')}`")
                    if item.get("special_notes"):
                        print(f"     Notes:       {item.get('special_notes')}")
                    print()
                if len(matches) > 15:
                    print(f"     ... and {len(matches) - 15} more matches in this category.")

        if total_found == 0:
            print("\nNo icons matching the search were found.")
            print("Try more general keywords (e.g., 'load balancer', 'database', 'auth', 'kubernetes').")
        else:
            print("-" * 80)
            print(f"Total found: {total_found} icons.")

    conn.close()

if __name__ == "__main__":
    main()
