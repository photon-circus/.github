import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "audit_repositories.py"
SPEC = importlib.util.spec_from_file_location("audit_repositories", MODULE_PATH)
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = audit
SPEC.loader.exec_module(audit)


def snapshot(*, lifecycle="Active", domains=None, paths=None, protected=True):
    return {
        "repository": {
            "name": "ph-example",
            "description": "A bounded example",
            "visibility": "public",
            "default_branch": "main",
            "topics": ["embedded-rust"],
            "html_url": "https://github.com/photon-circus/ph-example",
        },
        "properties": {
            "Lifecycle": lifecycle,
            "Domain": domains or ["Libraries"],
        },
        "paths": paths
        or [
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "RELEASING.md",
            "AGENTS.md",
            "scripts/ci.sh",
            ".github/workflows/ci.yml",
        ],
        "tree_truncated": False,
        "protection": {
            "required_checks": ["ci"],
            "conversation_resolution": True,
            "allow_force_pushes": False,
            "allow_deletions": False,
        }
        if protected
        else None,
    }


class ReadOnlyBoundaryTests(unittest.TestCase):
    def test_github_command_is_get_only(self):
        command = audit.build_gh_get("/repos/photon-circus/ph-example")
        self.assertEqual(command, ["gh", "api", "/repos/photon-circus/ph-example"])
        forbidden = {"--method", "-X", "POST", "PUT", "PATCH", "DELETE"}
        self.assertTrue(forbidden.isdisjoint(command))

    def test_unsafe_endpoint_is_rejected(self):
        with self.assertRaises(audit.AuditError):
            audit.build_gh_get("/repos/example value")


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = audit.Policy(("ph-example",), {})

    def by_id(self, result):
        return {item["id"]: item for item in result["checks"]}

    def test_active_reference_profile(self):
        result = audit.evaluate_repository(snapshot(), self.policy)
        checks = self.by_id(result)
        self.assertEqual(checks["license"]["status"], audit.PASS)
        self.assertEqual(checks["local_ci"]["status"], audit.PASS)
        self.assertEqual(checks["branch_protection"]["status"], audit.PASS)
        self.assertEqual(checks["public_ci_hardening"]["status"], audit.MANUAL_REVIEW)

    def test_experimental_changelog_is_not_required_but_license_is(self):
        result = audit.evaluate_repository(
            snapshot(
                lifecycle="Experimental",
                paths=["README.md"],
                protected=False,
            ),
            self.policy,
        )
        checks = self.by_id(result)
        self.assertEqual(checks["changelog"]["status"], audit.NOT_APPLICABLE)
        self.assertEqual(checks["license"]["status"], audit.FAIL)

    def test_public_documentation_repo_does_not_require_hosted_ci(self):
        paths = [
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
        ]
        result = audit.evaluate_repository(
            snapshot(domains=["Documentation"], paths=paths),
            self.policy,
        )
        checks = self.by_id(result)
        self.assertEqual(checks["hosted_ci"]["status"], audit.NOT_APPLICABLE)

    def test_findings_do_not_become_execution_failures(self):
        report = {
            "generated_at": "2026-08-11T00:00:00+00:00",
            "organization": "photon-circus",
            "scope": "test",
            "repositories": [audit.evaluate_repository(snapshot(protected=False), self.policy)],
        }
        rendered = audit.render_markdown(report)
        self.assertIn("findings authorize no changes", rendered)

    def test_unavailable_protection_data_requires_manual_review(self):
        candidate = snapshot()
        candidate["protection"] = {"unavailable": "HTTP 403"}
        result = audit.evaluate_repository(candidate, self.policy)
        checks = self.by_id(result)
        self.assertEqual(checks["branch_protection"]["status"], audit.MANUAL_REVIEW)

    def test_private_optional_workflow_requires_judgment_not_warning(self):
        candidate = snapshot(lifecycle="Incubating", protected=False)
        candidate["repository"]["visibility"] = "private"
        result = audit.evaluate_repository(candidate, self.policy)
        checks = self.by_id(result)
        self.assertEqual(checks["hosted_ci"]["status"], audit.MANUAL_REVIEW)

    def test_policy_file_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "policy.json"
            path.write_text(
                json.dumps(
                    {
                        "active_cohort": ["ph-example"],
                        "grandfathered_default_branches": {"ph-old": "master"},
                    }
                ),
                encoding="utf-8",
            )
            policy = audit.load_policy(path)
            self.assertEqual(policy.active_cohort, ("ph-example",))
            self.assertEqual(policy.grandfathered_default_branches["ph-old"], "master")


if __name__ == "__main__":
    unittest.main()
