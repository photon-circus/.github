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

    def test_conventional_cargo_xtask_shape_requires_semantic_review(self):
        candidate = snapshot()
        candidate["paths"].remove("scripts/ci.sh")
        candidate["paths"].extend([".cargo/config.toml", "xtask/Cargo.toml"])
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "conventional cargo xtask paths present; inspect the Cargo alias, "
            "documented command, and gate semantics",
        )

    def test_shell_and_cargo_xtask_entry_points_require_review(self):
        candidate = snapshot()
        candidate["paths"].extend([".cargo/config.toml", "xtask/Cargo.toml"])
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "multiple apparent entry points; verify all but one are thin launchers: "
            "scripts/ci.sh, conventional cargo xtask paths",
        )

    def test_shell_and_partial_cargo_xtask_shape_require_review(self):
        candidate = snapshot()
        candidate["paths"].append("xtask/Cargo.toml")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "multiple apparent entry points; verify all but one are thin launchers: "
            "scripts/ci.sh, xtask/Cargo.toml",
        )

    def test_cargo_config_without_xtask_manifest_still_passes(self):
        candidate = snapshot()
        candidate["paths"].append(".cargo/config.toml")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.PASS)
        self.assertEqual(local_ci["evidence"], "scripts/ci.sh")

    def test_cargo_config_alone_is_not_an_xtask_signal(self):
        candidate = snapshot()
        candidate["paths"].remove("scripts/ci.sh")
        candidate["paths"].append(".cargo/config.toml")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertIn("not machine-inferable", local_ci["evidence"])

    def test_multiple_shell_entry_points_require_review(self):
        candidate = snapshot()
        candidate["paths"].append("scripts/check.sh")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "multiple apparent entry points; verify all but one are thin launchers: "
            "scripts/ci.sh, scripts/check.sh",
        )

    def test_shell_and_powershell_entry_points_do_not_shadow_a_second_shell(self):
        candidate = snapshot()
        candidate["paths"].extend(["tools/check.ps1", "tools/check.sh"])
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "multiple apparent entry points; verify all but one are thin launchers: "
            "scripts/ci.sh, tools/check.sh, tools/check.ps1",
        )

    def test_powershell_only_entry_point_requires_review_not_warning(self):
        candidate = snapshot()
        candidate["paths"].remove("scripts/ci.sh")
        candidate["paths"].append("scripts/local-ci.ps1")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "one possible entry point: scripts/local-ci.ps1; inspect repository documentation",
        )

    def test_absent_entry_point_is_distinguishable_from_an_unrecognized_one(self):
        candidate = snapshot()
        candidate["paths"].remove("scripts/ci.sh")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "no candidate local entry point is present in the tree; a documented gate "
            "may still be a bare tool invocation, so absence is not machine-inferable",
        )

    def test_local_ci_never_reports_warn_or_fail(self):
        shapes = [
            [],
            ["scripts/ci.sh"],
            ["scripts/local-ci.ps1"],
            ["tools/check.sh"],
            ["Makefile"],
            ["xtask/Cargo.toml", ".cargo/config.toml"],
            ["scripts/ci.sh", "tools/check.ps1", "tools/check.sh"],
        ]
        for entry_points in shapes:
            for lifecycle in ("Incubating", "Active", "Maintenance"):
                with self.subTest(entry_points=entry_points, lifecycle=lifecycle):
                    candidate = snapshot(lifecycle=lifecycle)
                    candidate["paths"].remove("scripts/ci.sh")
                    candidate["paths"].extend(entry_points)
                    result = audit.evaluate_repository(candidate, self.policy)
                    local_ci = self.by_id(result)["local_ci"]
                    self.assertNotIn(local_ci["status"], (audit.WARN, audit.FAIL))

    def test_truncated_tree_prevents_local_ci_pass(self):
        candidate = snapshot()
        candidate["tree_truncated"] = True
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertIn("cannot determine", local_ci["evidence"])

    def test_partial_cargo_xtask_shape_requires_review(self):
        candidate = snapshot()
        candidate["paths"].remove("scripts/ci.sh")
        candidate["paths"].append("xtask/Cargo.toml")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "one possible entry point: xtask/Cargo.toml; inspect repository documentation",
        )

    def test_unrecognized_entry_point_is_not_treated_as_missing(self):
        candidate = snapshot()
        candidate["paths"].remove("scripts/ci.sh")
        candidate["paths"].append("Justfile")
        result = audit.evaluate_repository(candidate, self.policy)
        local_ci = self.by_id(result)["local_ci"]
        self.assertEqual(local_ci["status"], audit.MANUAL_REVIEW)
        self.assertEqual(
            local_ci["evidence"],
            "one possible entry point: Justfile; inspect repository documentation",
        )

    def test_experimental_missing_release_documents_require_manual_review(self):
        result = audit.evaluate_repository(
            snapshot(
                lifecycle="Experimental",
                paths=["README.md"],
                protected=False,
            ),
            self.policy,
        )
        checks = self.by_id(result)
        for check_id in ("changelog", "releasing"):
            self.assertEqual(checks[check_id]["status"], audit.MANUAL_REVIEW)
            self.assertEqual(
                checks[check_id]["evidence"],
                "publication/versioned-deliverable status is not machine-inferable",
            )
        self.assertEqual(checks["license"]["status"], audit.FAIL)

    def test_experimental_present_release_documents_pass(self):
        result = audit.evaluate_repository(
            snapshot(
                lifecycle="Experimental",
                paths=["README.md", "CHANGELOG.md", "RELEASING.md"],
                protected=False,
            ),
            self.policy,
        )
        checks = self.by_id(result)
        for check_id in ("changelog", "releasing"):
            self.assertEqual(checks[check_id]["status"], audit.PASS)
            self.assertEqual(checks[check_id]["evidence"], "present")

    def test_archived_missing_release_guidance_requires_manual_review(self):
        result = audit.evaluate_repository(
            snapshot(
                lifecycle="Archived",
                paths=["README.md", "LICENSE", "CHANGELOG.md"],
                protected=False,
            ),
            self.policy,
        )
        self.assertEqual(
            self.by_id(result)["releasing"]["status"],
            audit.MANUAL_REVIEW,
        )

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
            "agent_guidance",
            "hosted_ci",
            "public_ci_hardening",
        ):
            self.assertEqual(checks[check_id]["status"], audit.NOT_APPLICABLE)
        for check_id in ("changelog", "releasing"):
            self.assertEqual(checks[check_id]["status"], audit.MANUAL_REVIEW)
            self.assertEqual(
                checks[check_id]["evidence"],
                "cannot determine (GitHub truncated the recursive tree)",
            )

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

    def test_observed_workflow_preserves_missing_ci_warning_on_truncated_tree(self):
        candidate = snapshot(paths=[".github/workflows/ci.yml"])
        candidate["tree_truncated"] = True
        candidate["protection"]["required_checks"] = []
        result = audit.evaluate_repository(candidate, self.policy)
        self.assertEqual(
            self.by_id(result)["branch_protection"]["status"],
            audit.WARN,
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
