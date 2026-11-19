"""Small structural regressions for the PR review fixes; no live services required."""

import json
from pathlib import Path
import re
import unittest
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]


def text(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PluginContractTests(unittest.TestCase):
    def test_plugin_and_agent_metadata(self):
        manifest = json.loads(text(".cortex-plugin/plugin.json"))
        self.assertTrue((ROOT / manifest["skills"]).is_dir())
        for name in ("replay-verifier", "method-reviewer", "report-checker", "writing-checker"):
            with self.subTest(agent=name):
                source = text(f"agents/{name}.md")
                self.assertTrue(source.startswith("---\n"))
                metadata, body = source[4:].split("\n---\n", 1)
                self.assertIn(f"name: {name}\n", metadata + "\n")
                self.assertRegex(metadata, r'description: "[^"\n]+"')
                self.assertTrue(body.lstrip().startswith("# "))

    def test_verdicts_reach_output_and_gate(self):
        verifier = text("agents/replay-verifier.md")
        rules = dict(re.findall(r"^\| \*\*([^*]+)\*\* \|.*?\| ([^|]+) \|$",
                                verifier, re.MULTILINE))
        self.assertEqual(set(rules), {
            "MATCH", "CHECK FAILED", "MISMATCH", "MATCH (partial)",
            "NOT RUN", "NOT REPLAYABLE",
        })
        output = verifier.split("### Per step", 1)[1].splitlines()[1]
        options = {option.strip() for option in output.split(":", 1)[1].split("|")}
        self.assertEqual(set(rules), options)
        for verdict in ("CHECK FAILED", "MISMATCH", "MATCH (partial)", "NOT RUN"):
            self.assertTrue(rules[verdict].startswith("Block"), verdict)
        self.assertIn("missing files block", rules["NOT REPLAYABLE"])
        self.assertIn("| INCOMPLETE", verifier)
        for path in ("AGENTS.example.md", "skills/analysis-workflow/SKILL.md",
                     "skills/analysis-workflow/references/evidence-pack.md"):
            self.assertIn("Verdict rules", " ".join(text(path).split()))

    def test_verified_replacements_preserve_history(self):
        verifier = text("agents/replay-verifier.md")
        self.assertIn("**Gate scope:**", verifier)
        self.assertIn("### Superseded history", verifier)

    def test_failed_checks_keep_fallback_evidence(self):
        verifier = text("agents/replay-verifier.md")
        self.assertIn("Fallback evidence (whenever attempted, regardless of verdict)", verifier)
        replay = verifier.split("4. **Re-run read-only.**", 1)[1].split("5. **Compare.**", 1)[0]
        for condition in ("sql_sha256", "base_sha256", "cutoff", "CHECK FAILED", "NOT RUN"):
            self.assertIn(condition, replay)

    def test_privacy_scan_and_severity(self):
        checker = text("agents/report-checker.md")
        scan = checker.split("4. **Reader-facing content.**", 1)[1].split("5.", 1)[0]
        severity = checker.split("- **High:**", 1)[1].split("- **Medium:**", 1)[0]
        for section in (scan, severity):
            for violation in ("record-level entries", "sensitive free text"):
                self.assertIn(violation, section)
        output = checker.split("## Output", 1)[1]
        self.assertIn("redacted excerpt for privacy findings", output)

    def test_date_and_version_traceability(self):
        checker = text("agents/report-checker.md")
        severity = checker.split("## Severity", 1)[1].split("## Output", 1)[0]
        self.assertIn("a measured", severity)
        self.assertIn("design date", severity)
        self.assertIn("max(1, Profile minimum)", severity)
        self.assertIn("Results versions checked:", checker)
        self.assertNotIn("numbers against `<topic>_results.json`", checker)
        self.assertIn("exact results versions", text("skills/report-writing/references/visuals.md"))
        pack = text("skills/analysis-workflow/references/evidence-pack.md")
        report = pack.split("### executive_study.md", 1)[1].split("###", 1)[0]
        self.assertIn("Measured values", report)
        self.assertIn("design dates", report)

    def test_rerun_names_and_original_evidence(self):
        pack = text("skills/analysis-workflow/references/evidence-pack.md")
        for suffix in ("", "_<yyyy-mm-dd>", "_<yyyymmdd>", "_<yyyymmddThhmmssZ>",
                       "_<yyyymmddThhmmssZ>_<run_id>"):
            self.assertIn(f"<topic>_results{suffix}.json", pack)
        self.assertIn("Create the file exclusively", pack)
        self.assertIn("do not replace the original hash", pack)
        self.assertIn("sql_revision", pack)

    def test_no_em_dash_anywhere(self):
        dash = "\u2014"
        for path in ROOT.rglob("*"):
            if path.suffix in {".md", ".json", ".py"} and ".git" not in path.parts:
                with self.subTest(file=str(path.relative_to(ROOT))):
                    self.assertNotIn(dash, path.read_text(encoding="utf-8"))

    def test_writing_rules_and_checker(self):
        rules = text("AGENTS.example.md")
        section = rules.split("## 12. Writing style (blocking)", 1)[1]
        for rule in ("No jargon", "Explain the implication", "Counts before percentages",
                     "No em dash", "writing-checker"):
            self.assertIn(rule, section)
        checker = text("agents/writing-checker.md")
        severity = checker.split("## Severity", 1)[1].split("## Output", 1)[0]
        high = severity.split("- **Medium:**", 1)[0]
        for item in ("em dash", "jargon", "percentage", "Implication"):
            self.assertIn(item, high)
        for needle in ("Read-only", "`AGENTS.md` \u00a712", "plain-writing.md",
                       "Do not write it to a file"):
            self.assertIn(needle, checker)
        self.assertTrue((ROOT / "skills/report-writing/references/plain-writing.md").is_file())
        workflow = text("skills/analysis-workflow/SKILL.md")
        review = workflow.split("## Review", 1)[1].split("## Hand over", 1)[0]
        self.assertIn("`writing-checker`", review)
        self.assertIn("writing-checker", rules.split("## 8. Pull request gate", 1)[1])

    def test_secondary_roles_off_before_queries(self):
        rules = text("AGENTS.example.md")
        safe = rules.split("## 3. Read-only and safe", 1)[1].split("## 4.", 1)[0]
        self.assertIn("USE SECONDARY ROLES NONE", safe)
        self.assertIn("USE SECONDARY ROLES NONE", text("skills/analysis-setup/SKILL.md"))

    def test_setup_selects_role_before_any_query(self):
        setup = text("skills/analysis-setup/SKILL.md")
        check = setup.split("### 5. Snowflake", 1)[1].split("### 6.", 1)[0]
        use_role = check.index("`USE ROLE <role>`")
        roles_off = check.index("`USE SECONDARY ROLES NONE`")
        first_query = check.index("select current_role()")
        self.assertLess(use_role, roles_off)
        self.assertLess(roles_off, first_query)
        self.assertIn("current_secondary_roles()", check[first_query:first_query + 120])

    def test_checker_quotes_may_keep_source_wording(self):
        checker = text("agents/writing-checker.md")
        self.assertIn("exact quotation", checker)
        self.assertIn("Your suggested rewrite must not", checker)

    def test_review_case_rows_have_two_columns(self):
        for number, line in enumerate(text("tests/review-cases.md").splitlines(), 1):
            if line.startswith("|") and not line.startswith("|---"):
                with self.subTest(line=number):
                    cells = [c for c in re.split(r"(?<!\\)\|", line.strip()[1:-1])]
                    self.assertEqual(len(cells), 2, line[:80])

    def test_setup_skill_is_safe_and_complete(self):
        setup = text("skills/analysis-setup/SKILL.md")
        self.assertTrue(setup.startswith("---\nname: analysis-setup\n"))
        for needle in ("Never ask for a password, a token", "never commit, push or merge",
                       "ATLASSIAN_API_TOKEN", "gh auth status", "rsvg-convert",
                       "writing-checker", "Do not write a setup report to a file"):
            self.assertIn(needle, setup)
        self.assertIn("analysis-setup", text("skills/analysis-workflow/SKILL.md"))

    def test_publishing_example_and_handover(self):
        publishing = text("skills/report-writing/references/confluence-publish.md")
        example = publishing.split("```html\n", 1)[1].split("```", 1)[0]
        figure = ElementTree.fromstring(example.strip())
        self.assertEqual(figure.attrib["data-width"], "100")
        handover = publishing.split("## After publishing", 1)[1]
        for instruction in ("evidence_index.md", "Commit", "push the analysis branch",
                            "PR description", "authorization"):
            self.assertIn(instruction, handover)


if __name__ == "__main__":
    unittest.main()