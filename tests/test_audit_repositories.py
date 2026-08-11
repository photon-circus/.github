import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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
            "Domain": domains if domains is not None else ["Libraries"],
        },
        "paths": paths
        if paths is not None
        else [
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

    def test_paginated_command_remains_get_only(self):
        command = audit.build_gh_get("/orgs/photon-circus/repos", paginate=True)
        self.assertEqual(
            command,
            ["gh", "api", "/orgs/photon-circus/repos", "--paginate", "--slurp"],
        )
        self.assertEqual(audit.flatten_paginated_list([[1, 2], [3]]), [1, 2, 3])

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

    def test_truncated_tree_never_turns_missing_paths_into_findings(self):
        candidate = snapshot(paths=[])
        candidate["tree_truncated"] = True
        result = audit.evaluate_repository(candidate, self.policy)
        checks = self.by_id(result)
        for check_id in ("readme", "license", "changelog", "local_ci", "hosted_ci"):
            self.assertEqual(checks[check_id]["status"], audit.MANUAL_REVIEW)

    def test_deterministic_non_applicability_precedes_incomplete_tree(self):
        candidate = snapshot(
            lifecycle="Experimental",
            domains=["Experience"],
            paths=[],
            protected=False,
        )
        candidate["repository"]["visibility"] = "private"
        candidate["tree_truncated"] = True
        result = audit.evaluate_repository(candidate, self.policy)
        checks = self.by_id(result)
        for check_id in (
            "local_ci",
            "contributing",
            "security",
            "releasing",
            "agent_guidance",
            "hosted_ci",
            "public_ci_hardening",
        ):
            self.assertEqual(checks[check_id]["status"], audit.NOT_APPLICABLE)

    def test_license_prefixes_do_not_count_as_license_files(self):
        candidate = snapshot(paths=["README.md", "LICENSES", "LICENSE.old", "COPYING-NOTES.md"])
        result = audit.evaluate_repository(candidate, self.policy)
        self.assertEqual(self.by_id(result)["license"]["status"], audit.FAIL)

    def test_unknown_lifecycle_propagates_to_gated_checks(self):
        candidate = snapshot(lifecycle=None, paths=["README.md", "LICENSE"])
        result = audit.evaluate_repository(candidate, self.policy)
        checks = self.by_id(result)
        for check_id in ("changelog", "local_ci", "contributing", "security", "branch_protection"):
            self.assertEqual(checks[check_id]["status"], audit.MANUAL_REVIEW)

    def test_public_hosted_ci_without_required_ci_check_warns(self):
        candidate = snapshot()
        candidate["protection"]["required_checks"] = []
        result = audit.evaluate_repository(candidate, self.policy)
        self.assertEqual(self.by_id(result)["branch_protection"]["status"], audit.WARN)

    def test_unknown_workflow_inventory_prevents_protection_pass(self):
        candidate = snapshot(paths=[])
        candidate["tree_truncated"] = True
        candidate["protection"]["required_checks"] = []
        result = audit.evaluate_repository(candidate, self.policy)
        self.assertEqual(
            self.by_id(result)["branch_protection"]["status"],
            audit.MANUAL_REVIEW,
        )

    @patch.object(audit, "gh_get")
    def test_empty_repository_is_a_repository_level_manual_review(self, gh_get):
        gh_get.return_value = []
        repository = {
            "name": "ph-empty",
            "default_branch": None,
            "description": None,
            "visibility": "private",
            "topics": [],
            "html_url": "https://github.com/photon-circus/ph-empty",
        }
        collected = audit.collect_snapshot("photon-circus", repository)
        self.assertEqual(collected["tree_unavailable"], "repository has no default branch")
        self.assertEqual(gh_get.call_count, 1)

    @patch.object(audit, "gh_get")
    def test_ruleset_only_protection_is_collected(self, gh_get):
        gh_get.side_effect = [
            [],
            {"tree": [], "truncated": False},
            None,
            [
                {"type": "deletion"},
                {"type": "non_fast_forward"},
                {
                    "type": "pull_request",
                    "parameters": {"required_review_thread_resolution": True},
                },
                {
                    "type": "required_status_checks",
                    "parameters": {"required_status_checks": [{"context": "ci"}]},
                },
            ],
        ]
        repository = {
            "name": "ph-example",
            "default_branch": "main",
            "description": "example",
            "visibility": "public",
            "topics": [],
            "html_url": "https://github.com/photon-circus/ph-example",
        }
        collected = audit.collect_snapshot("photon-circus", repository)
        self.assertEqual(collected["protection"]["source"], "ruleset")
        self.assertEqual(collected["protection"]["required_checks"], ["ci"])
        self.assertFalse(collected["protection"]["allow_force_pushes"])
        self.assertFalse(collected["protection"]["allow_deletions"])
        self.assertTrue(gh_get.call_args_list[3].kwargs["paginate"])

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
