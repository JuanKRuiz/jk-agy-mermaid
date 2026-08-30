#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encapsulated CLI to update icon compatibility, blacklist status, and substitutions
in the icons cache SQLite database (icons_cache.db).
Author: Antigravity
"""

import os
import sys
import sqlite3
from pathlib import Path

def clean_code(code_str):
    """
    Cleans the icon code from backticks, quotes, and wrapping delimiters.
    E.g.: "`gcp:compute-engine`" -> "gcp:compute-engine"
    """
    if not code_str:
        return ""
    stripped = code_str.strip(" \t\n\r`'\"()[]{},;!?")
    return stripped.replace("`", "").replace("'", "").replace('"', "").strip()

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 update_icon.py --blacklist <icon_code> <0_or_1>")
        print("  python3 update_icon.py --style-compatible <icon_code> <0_or_1>")
        print("  python3 update_icon.py --substitute <icon_code> <substitute_code_or_none>")
        sys.exit(1)

    # Database path relative to this script (with optional environment variable override)
    script_dir = Path(__file__).resolve().parent
    env_db = os.environ.get("ICONS_DB_PATH")
    db_path = Path(env_db).resolve() if env_db else (script_dir / ".." / "resources" / "databases" / "icons_cache.db").resolve()

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        sys.exit(1)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
    except Exception as e:
        print(f"Connection error: {e}", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1]
    icon_code = clean_code(sys.argv[2])

    try:
        if action == "--blacklist":
            if len(sys.argv) < 4:
                print("Error: Specify 0 or 1 for blacklist value.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            raw_val = sys.argv[3].strip()
            if raw_val not in ("0", "1"):
                print(f"Error: Invalid blacklist value '{raw_val}'. Specify 0 or 1.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            val = int(raw_val)
            cursor.execute("UPDATE icons SET is_blacklisted = ? WHERE code = ?", (val, icon_code))
            if cursor.rowcount == 0:
                print(f"Error: Icon code '{icon_code}' was not found in the database.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            conn.commit()
            print(f"Updated {icon_code} ({cursor.rowcount} row(s)): is_blacklisted = {val}")

        elif action == "--style-compatible":
            if len(sys.argv) < 4:
                print("Error: Specify 0 or 1 for style compatibility.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            raw_val = sys.argv[3].strip()
            if raw_val not in ("0", "1"):
                print(f"Error: Invalid style compatibility value '{raw_val}'. Specify 0 or 1.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            val = int(raw_val)
            cursor.execute("UPDATE icons SET is_style_compatible = ? WHERE code = ?", (val, icon_code))
            if cursor.rowcount == 0:
                print(f"Error: Icon code '{icon_code}' was not found in the database.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            conn.commit()
            print(f"Updated {icon_code} ({cursor.rowcount} row(s)): is_style_compatible = {val}")

        elif action == "--substitute":
            if len(sys.argv) < 4:
                print("Error: Specify substitute icon code or 'none' to clear.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            raw_sub = sys.argv[3].strip()
            if not raw_sub or raw_sub.lower() == "none":
                sub = None
            else:
                sub = clean_code(raw_sub)
                cursor.execute("SELECT 1 FROM icons WHERE code = ?", (sub,))
                if not cursor.fetchone():
                    print(f"Error: Substitute icon code '{sub}' was not found in the database.", file=sys.stderr)
                    conn.close()
                    sys.exit(1)

            cursor.execute("UPDATE icons SET substitute_code = ? WHERE code = ?", (sub, icon_code))
            if cursor.rowcount == 0:
                print(f"Error: Icon code '{icon_code}' was not found in the database.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            conn.commit()
            print(f"Updated {icon_code} ({cursor.rowcount} row(s)): substitute_code = {sub}")

        else:
            print(f"Error: Unknown action '{action}'", file=sys.stderr)
            conn.close()
            sys.exit(1)

    except sqlite3.Error as e:
        print(f"SQLite transaction error: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    conn.close()

if __name__ == "__main__":
    main()
