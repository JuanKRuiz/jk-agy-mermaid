#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encapsulated CLI to update icon compatibility, blacklist status, and substitutions
in the icons cache SQLite database (icons_cache.db).
Author: Antigravity
"""

import sys
import sqlite3
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 update_icon.py --blacklist <icon_code> <0_or_1>")
        print("  python3 update_icon.py --style-compatible <icon_code> <0_or_1>")
        print("  python3 update_icon.py --substitute <icon_code> <substitute_code_or_none>")
        sys.exit(1)

    # Database path relative to this script
    script_dir = Path(__file__).resolve().parent
    db_path = (script_dir / ".." / "resources" / "databases" / "icons_cache.db").resolve()

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
    icon_code = sys.argv[2]

    try:
        if action == "--blacklist":
            if len(sys.argv) < 4:
                print("Error: Specify 0 or 1 for blacklist value.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            val = int(sys.argv[3])
            cursor.execute("UPDATE icons SET is_blacklisted = ? WHERE code = ?", (val, icon_code))
            print(f"Updated {icon_code}: is_blacklisted = {val}")

        elif action == "--style-compatible":
            if len(sys.argv) < 4:
                print("Error: Specify 0 or 1 for style compatibility.", file=sys.stderr)
                conn.close()
                sys.exit(1)
            val = int(sys.argv[3])
            cursor.execute("UPDATE icons SET is_style_compatible = ? WHERE code = ?", (val, icon_code))
            print(f"Updated {icon_code}: is_style_compatible = {val}")

        elif action == "--substitute":
            sub = sys.argv[3] if len(sys.argv) >= 4 and sys.argv[3].lower() != "none" else None
            cursor.execute("UPDATE icons SET substitute_code = ? WHERE code = ?", (sub, icon_code))
            print(f"Updated {icon_code}: substitute_code = {sub}")

        else:
            print(f"Error: Unknown action {action}", file=sys.stderr)
            conn.close()
            sys.exit(1)

        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite transaction error: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    conn.close()

if __name__ == "__main__":
    main()
