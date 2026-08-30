#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Automated Test Suite for jk-agy-mermaid Audit Fixes.
Validates:
1. SQLite Database (icons_cache.db) integrity and uniqueness.
2. query_icons.py relevance ranking, category prioritization unmasking, and code sanitization.
3. update_icon.py validation (rowcount, binary values, error exit codes).
4. Documentation and license consistency across README, SKILL.md, and docs.
"""

import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "skills" / "mermaid-designer" / "resources" / "databases" / "icons_cache.db"
QUERY_SCRIPT = REPO_ROOT / "skills" / "mermaid-designer" / "scripts" / "query_icons.py"
UPDATE_SCRIPT = REPO_ROOT / "skills" / "mermaid-designer" / "scripts" / "update_icon.py"

# Add scripts directory to sys.path for direct function imports
sys.path.insert(0, str(REPO_ROOT / "skills" / "mermaid-designer" / "scripts"))
import query_icons

class TestDatabaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_total_and_distinct_row_counts(self):
        self.cursor.execute("SELECT COUNT(*) FROM icons")
        total = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT COUNT(DISTINCT code) FROM icons")
        distinct = self.cursor.fetchone()[0]
        self.assertEqual(total, 2718, f"Expected exactly 2718 total rows, got {total}")
        self.assertEqual(distinct, 2718, f"Expected exactly 2718 distinct codes, got {distinct}")

    def test_no_duplicate_codes_exist(self):
        self.cursor.execute("SELECT code, COUNT(*) as cnt FROM icons GROUP BY code HAVING cnt > 1")
        dups = self.cursor.fetchall()
        self.assertEqual(len(dups), 0, f"Found unexpected duplicate codes: {dups}")

    def test_unique_index_enforced(self):
        self.cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name='idx_icons_code'")
        idx_sql = self.cursor.fetchone()
        self.assertIsNotNone(idx_sql, "Index idx_icons_code was not found")
        self.assertIn("UNIQUE", idx_sql[0].upper(), "Index idx_icons_code is not UNIQUE")

    def test_unique_constraint_rejects_duplicate_insertion(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.cursor.execute("INSERT INTO icons (code, category, name) VALUES ('logos:salesforce', 'svg', 'Duplicate Test')")

    def test_key_icons_preserved_and_intact(self):
        key_codes = ["logos:salesforce", "logos:nextjs", "logos:firebase", "logos:airtable", "fa:user", "gcp:compute-engine"]
        for code in key_codes:
            self.cursor.execute("SELECT id, name, description, search_text FROM icons WHERE code = ?", (code,))
            row = self.cursor.fetchone()
            self.assertIsNotNone(row, f"Canonical record for '{code}' is missing")
            self.assertTrue(len(row[3]) > 0, f"Search text for '{code}' is empty")


class TestQueryIconsCLI(unittest.TestCase):
    def run_query(self, args):
        cmd = [sys.executable, str(QUERY_SCRIPT)] + args
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT))
        return res

    def test_batch_query_unmasking(self):
        res = self.run_query(["--batch", "salesforce", "docker", "kubernetes", "python", "slack", "user", "load balancer", "database", "gcp:compute-engine"])
        self.assertEqual(res.returncode, 0, f"Query failed: {res.stderr}")
        data = json.loads(res.stdout)

        self.assertEqual(data["salesforce"]["code"], "logos:salesforce", "Masking bug: salesforce should return logos:salesforce")
        self.assertEqual(data["docker"]["code"], "logos:docker", "Masking bug: docker should return logos:docker")
        self.assertEqual(data["kubernetes"]["code"], "logos:kubernetes", "Masking bug: kubernetes should return logos:kubernetes")
        self.assertEqual(data["python"]["code"], "logos:python", "Masking bug: python should return logos:python")
        self.assertEqual(data["slack"]["code"], "logos:slack", "Masking bug: slack should return logos:slack")
        self.assertEqual(data["user"]["code"], "fa:user", "Masking bug: user should return fa:user")
        self.assertIn("load-balancer", data["load balancer"]["code"], "load balancer should return a load balancer icon")
        self.assertEqual(data["database"]["code"], "aws:res-database", "database should return generic aws:res-database")
        self.assertEqual(data["gcp:compute-engine"]["code"], "gcp:compute-engine", "exact code query should resolve gcp:compute-engine")

    def test_code_lookup_with_and_without_backticks(self):
        # Plain code
        res1 = self.run_query(["--code", "logos:salesforce"])
        self.assertEqual(res1.returncode, 0)
        data1 = json.loads(res1.stdout)
        self.assertEqual(data1["code"], "logos:salesforce")

        # Code enclosed in backticks
        res2 = self.run_query(["--code", "`logos:salesforce`"])
        self.assertEqual(res2.returncode, 0)
        data2 = json.loads(res2.stdout)
        self.assertEqual(data2["code"], "logos:salesforce")

    def test_code_lookup_nonexistent(self):
        res = self.run_query(["--code", "fake:does-not-exist"])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIsNone(data)


    def test_case_insensitivity_and_empty_terms(self):
        res = self.run_query(["--batch", "SalesForce", "DOCKER", "", "  "])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["SalesForce"]["code"], "logos:salesforce")
        self.assertEqual(data["DOCKER"]["code"], "logos:docker")

    def test_query_usage_on_missing_args(self):
        res = self.run_query([])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Usage:", res.stdout)

    def test_batch_punctuation_and_brackets(self):
        res = self.run_query(["--batch", "(docker)", "salesforce!", "kubernetes,", "[python]"])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertEqual(data["(docker)"]["code"], "logos:docker")
        self.assertEqual(data["salesforce!"]["code"], "logos:salesforce")
        self.assertEqual(data["kubernetes,"]["code"], "logos:kubernetes")
        self.assertEqual(data["[python]"]["code"], "logos:python")

    def test_batch_spanish_natural_language_queries(self):
        res = self.run_query(["--batch", "el balanceador de carga", "la base de datos", "el usuario", "usuario", "user"])
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertIn("load-balancer", data["el balanceador de carga"]["code"])
        self.assertTrue("database" in data["la base de datos"]["code"] or "aurora" in data["la base de datos"]["code"])
        self.assertEqual(data["el usuario"]["code"], "aws:res-user")
        self.assertEqual(data["usuario"]["code"], "aws:res-user")
        self.assertEqual(data["user"]["code"], "fa:user")

    def test_query_single_empty_list_returns_empty(self):
        conn = sqlite3.connect(str(DB_PATH))
        try:
            res = query_icons.query_single(conn, [])
            self.assertEqual(res, {'cloud': [], 'svg': [], 'font_awesome': [], 'other': []})
        finally:
            conn.close()


class TestUpdateIconCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create an isolated temporary copy of the database to guarantee production database is never mutated
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.test_db_path = Path(cls.temp_dir.name) / "test_icons_cache.db"
        shutil.copy2(DB_PATH, cls.test_db_path)
        cls.env = os.environ.copy()
        cls.env["ICONS_DB_PATH"] = str(cls.test_db_path)

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def run_update(self, args):
        cmd = [sys.executable, str(UPDATE_SCRIPT)] + args
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO_ROOT), env=self.env)
        return res

    def get_test_db_icon(self, code):
        conn = sqlite3.connect(str(self.test_db_path))
        try:
            c = conn.cursor()
            c.execute("SELECT is_blacklisted, is_style_compatible, substitute_code FROM icons WHERE code = ?", (code,))
            return c.fetchone()
        finally:
            conn.close()

    def test_update_valid_icon_succeeds(self):
        # Mutate to 1 and verify persistence in test DB
        res1 = self.run_update(["--blacklist", "logos:salesforce", "1"])
        self.assertEqual(res1.returncode, 0, f"Update failed: {res1.stderr}")
        self.assertIn("Updated logos:salesforce", res1.stdout)
        self.assertIn("1 row(s)", res1.stdout)
        row = self.get_test_db_icon("logos:salesforce")
        self.assertEqual(row[0], 1)

        # Restore to 0 and verify
        res2 = self.run_update(["--blacklist", "logos:salesforce", "0"])
        self.assertEqual(res2.returncode, 0)
        row2 = self.get_test_db_icon("logos:salesforce")
        self.assertEqual(row2[0], 0)

    def test_update_with_backticks_succeeds(self):
        res = self.run_update(["--style-compatible", "`logos:salesforce`", "1"])
        self.assertEqual(res.returncode, 0, f"Update with backticks failed: {res.stderr}")
        self.assertIn("Updated logos:salesforce", res.stdout)
        row = self.get_test_db_icon("logos:salesforce")
        self.assertEqual(row[1], 1)
        # Revert back to 0
        self.run_update(["--style-compatible", "logos:salesforce", "0"])

    def test_update_substitute_and_clear(self):
        # Set substitute
        res1 = self.run_update(["--substitute", "logos:salesforce", "`logos:clickdeploy`"])
        self.assertEqual(res1.returncode, 0)
        self.assertIn("substitute_code = logos:clickdeploy", res1.stdout)
        row1 = self.get_test_db_icon("logos:salesforce")
        self.assertEqual(row1[2], "logos:clickdeploy")

        # Clear substitute with 'none'
        res2 = self.run_update(["--substitute", "logos:salesforce", "none"])
        self.assertEqual(res2.returncode, 0)
        self.assertIn("substitute_code = None", res2.stdout)
        row2 = self.get_test_db_icon("logos:salesforce")
        self.assertIsNone(row2[2])

        # Restore original substitute
        res3 = self.run_update(["--substitute", "logos:salesforce", "logos:clickdeploy"])
        self.assertEqual(res3.returncode, 0)
        row3 = self.get_test_db_icon("logos:salesforce")
        self.assertEqual(row3[2], "logos:clickdeploy")

    def test_update_substitute_missing_args_fails(self):
        res = self.run_update(["--substitute", "logos:salesforce"])
        self.assertEqual(res.returncode, 1, "Expected exit code 1 when substitute code argument is missing")
        self.assertIn("Specify substitute icon code or 'none' to clear", res.stderr)

    def test_update_substitute_nonexistent_icon_fails(self):
        res = self.run_update(["--substitute", "logos:salesforce", "fake:does-not-exist"])
        self.assertEqual(res.returncode, 1, "Expected exit code 1 when substitute icon does not exist")
        self.assertIn("Substitute icon code 'fake:does-not-exist' was not found", res.stderr)

    def test_update_nonexistent_icon_fails_with_exit_code_1(self):
        res = self.run_update(["--blacklist", "fake:non-existent-code", "1"])
        self.assertEqual(res.returncode, 1, "Expected exit code 1 for non-existent icon")
        self.assertIn("Error:", res.stderr)
        self.assertIn("not found in the database", res.stderr)

    def test_update_invalid_binary_argument_fails(self):
        res = self.run_update(["--blacklist", "logos:salesforce", "2"])
        self.assertEqual(res.returncode, 1, "Expected exit code 1 for invalid binary argument")
        self.assertIn("Specify 0 or 1", res.stderr)

        res_str = self.run_update(["--style-compatible", "logos:salesforce", "invalid"])
        self.assertEqual(res_str.returncode, 1, "Expected exit code 1 for non-numeric value")
        self.assertIn("Specify 0 or 1", res_str.stderr)

    def test_update_usage_on_missing_args(self):
        res = self.run_update([])
        self.assertEqual(res.returncode, 1)
        self.assertIn("Usage:", res.stdout)


class TestDocumentationAndLicenseConsistency(unittest.TestCase):
    def test_readme_license_declaration(self):
        readme_path = REPO_ROOT / "README.md"
        content = readme_path.read_text(encoding="utf-8")
        self.assertNotIn("MIT License", content, "README.md still references MIT License")
        self.assertIn("CC BY 4.0", content, "README.md does not reference CC BY 4.0")

    def test_no_phantom_json_databases_in_skill_md(self):
        skill_path = REPO_ROOT / "skills" / "mermaid-designer" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        self.assertNotIn("gcp_icons.json", content, "SKILL.md still references phantom gcp_icons.json")
        self.assertNotIn("aws_icons.json", content, "SKILL.md still references phantom aws_icons.json")
        self.assertNotIn("JSON Icon Databases", content, "SKILL.md still references phantom JSON Icon Databases section")

    def test_no_phantom_json_databases_in_architecture_md(self):
        arch_path = REPO_ROOT / "docs" / "architecture_and_operations.md"
        content = arch_path.read_text(encoding="utf-8")
        self.assertNotIn("gcp_icons.json", content, "architecture_and_operations.md still references phantom gcp_icons.json")
        self.assertIn("update_icon.py", content, "architecture_and_operations.md missing update_icon.py in tree")


if __name__ == "__main__":
    unittest.main()
