#!/usr/bin/env python3
"""Read-only evidence collector for Photon Circus repository standards.

This program has no remediation mode. Every GitHub request is an HTTP GET made
through ``gh api``. Findings are observations only and confer no authority to
change repository files, metadata, settings, visibility, or lifecycle.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote


PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"
NOT_APPLICABLE = "NOT_APPLICABLE"
MANUAL_REVIEW = "MANUAL_REVIEW"
STATUSES = (PASS, FAIL, WARN, NOT_APPLICABLE, MANUAL_REVIEW)

ALLOWED_LIFECYCLES = {
    "Experimental",
    "Incubating",
    "Active",
    "Maintenance",
    "Archived",
}
ALLOWED_DOMAINS = {
    "Firmware",
    "Hardware",
    "Libraries",
    "Tooling",
    "Experience",
    "Documentation",
}
TECHNICAL_DOMAINS = {"Firmware", "Hardware", "Libraries", "Tooling"}
MAINTAINED_LIFECYCLES = {"Incubating", "Active", "Maintenance"}

SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


class AuditError(RuntimeError):
    """Raised for execution or configuration failures, never for findings."""


@dataclass(frozen=True)
class Policy:
    active_cohort: tuple[str, ...]
    grandfathered_default_branches: dict[str, str]


def build_gh_get(endpoint: str, *, paginate: bool = False) -> list[str]:
    """Build the only permitted GitHub command: an implicit GET request."""
    if not endpoint.startswith("/") or any(char.isspace() for char in endpoint):
        raise AuditError(f"unsafe GitHub API endpoint: {endpoint!r}")
    command = ["gh", "api", endpoint]
    if paginate:
        command.extend(("--paginate", "--slurp"))
    return command


def flatten_paginated_list(payload: Any) -> list[Any]:
    if not isinstance(payload, list) or any(not isinstance(page, list) for page in payload):
        raise AuditError("paginated GitHub response was not a list of pages")
    return [item for page in payload for item in page]


def gh_get(
    endpoint: str,
    *,
    allow_not_found: bool = False,
    allow_forbidden: bool = False,
    paginate: bool = False,
) -> Any:
    command = build_gh_get(endpoint, paginate=paginate)
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        if allow_not_found and "HTTP 404" in completed.stderr:
            return None
        if allow_forbidden and "HTTP 403" in completed.stderr:
            return {"_audit_unavailable": completed.stderr.strip()}
        detail = completed.stderr.strip() or "unknown gh error"
        raise AuditError(f"GET {endpoint} failed: {detail}")
    try:
        payload = json.loads(completed.stdout)
        return flatten_paginated_list(payload) if paginate else payload
    except json.JSONDecodeError as error:
        raise AuditError(f"GET {endpoint} returned invalid JSON: {error}") from error


def validate_name(value: str, kind: str) -> str:
    if not SAFE_NAME.fullmatch(value):
        raise AuditError(f"invalid {kind}: {value!r}")
    return value


def load_policy(path: Path) -> Policy:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AuditError(f"cannot read policy {path}: {error}") from error

    cohort = tuple(validate_name(name, "repository name") for name in raw["active_cohort"])
    grandfathered = {
        validate_name(name, "repository name"): validate_name(branch, "branch name")
        for name, branch in raw.get("grandfathered_default_branches", {}).items()
    }
    return Policy(cohort, grandfathered)


def property_map(values: Any) -> dict[str, Any]:
    if not isinstance(values, list):
        raise AuditError("repository custom-property response was not a list")
    return {
        item["property_name"]: item.get("value")
        for item in values
        if isinstance(item, dict) and "property_name" in item
    }


def root_files(paths: Iterable[str]) -> set[str]:
    return {path for path in paths if "/" not in path}


def has_root(files: set[str], names: Iterable[str]) -> bool:
    folded = {name.casefold() for name in files}
    return any(name.casefold() in folded for name in names)


def check(
    check_id: str,
    status: str,
    evidence: str,
    standard: str,
) -> dict[str, str]:
    if status not in STATUSES:
        raise AuditError(f"invalid status {status!r}")
    return {
        "id": check_id,
        "status": status,
        "evidence": evidence,
        "standard": standard,
    }


def normalize_domains(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if isinstance(value, str) and value:
        return [value]
    return []


def evaluate_repository(snapshot: dict[str, Any], policy: Policy) -> dict[str, Any]:
    repo = snapshot["repository"]
    name = repo["name"]
    visibility = repo.get("visibility", "unknown")
    properties = snapshot["properties"]
    lifecycle = properties.get("Lifecycle")
    domains = normalize_domains(properties.get("Domain"))
    paths = set(snapshot["paths"])
    roots = root_files(paths)
    topics = repo.get("topics") or []
    checks: list[dict[str, str]] = []
    lifecycle_known = lifecycle in ALLOWED_LIFECYCLES
    tree_incomplete = bool(snapshot.get("tree_truncated") or snapshot.get("tree_unavailable"))
    tree_reason = snapshot.get("tree_unavailable") or "GitHub truncated the recursive tree"

    def absent_path_status(status: str) -> str:
        return MANUAL_REVIEW if tree_incomplete else status

    def absent_path_evidence(evidence: str) -> str:
        return f"cannot determine ({tree_reason})" if tree_incomplete else evidence

    checks.append(
        check(
            "description",
            PASS if str(repo.get("description") or "").strip() else FAIL,
            str(repo.get("description") or "missing"),
            "Section 3 Repository identity",
        )
    )

    lifecycle_status = PASS if lifecycle in ALLOWED_LIFECYCLES else FAIL
    checks.append(
        check(
            "lifecycle",
            lifecycle_status,
            str(lifecycle or "missing or unrecognized"),
            "Section 3.1 Lifecycle values",
        )
    )

    invalid_domains = sorted(set(domains) - ALLOWED_DOMAINS)
    domain_status = PASS if domains and not invalid_domains else FAIL
    domain_evidence = ", ".join(domains) if domains else "missing"
    if invalid_domains:
        domain_evidence += f"; unrecognized: {', '.join(invalid_domains)}"
    checks.append(check("domain", domain_status, domain_evidence, "Section 3.2 Domain values"))

    checks.append(
        check(
            "topics",
            PASS if topics else FAIL,
            ", ".join(topics) if topics else "missing",
            "Section 3 Repository identity",
        )
    )

    readme_present = has_root(roots, ("README", "README.md", "README.rst"))
    checks.append(
        check(
            "readme",
            PASS if readme_present else absent_path_status(FAIL),
            "root README present" if readme_present else absent_path_evidence("root README missing"),
            "Section 6 README contract",
        )
    )
    license_present = has_root(
        roots,
        (
            "LICENSE",
            "LICENSE.md",
            "LICENSE.txt",
            "LICENCE",
            "LICENCE.md",
            "LICENCE.txt",
            "COPYING",
            "COPYING.md",
            "COPYING.txt",
        ),
    )
    checks.append(
        check(
            "license",
            PASS if license_present else absent_path_status(FAIL),
            "root license file present" if license_present else absent_path_evidence("root license file missing"),
            "Section 9 Licensing",
        )
    )

    changelog_present = has_root(roots, ("CHANGELOG", "CHANGELOG.md"))
    if lifecycle == "Experimental":
        changelog_status = PASS if changelog_present else NOT_APPLICABLE
        changelog_evidence = "present (optional for Experimental)" if changelog_present else "optional for Experimental"
    elif lifecycle_known:
        changelog_status = PASS if changelog_present else absent_path_status(FAIL)
        changelog_evidence = "present" if changelog_present else absent_path_evidence("required but missing")
    else:
        changelog_status = MANUAL_REVIEW
        changelog_evidence = "lifecycle is unavailable, so applicability cannot be determined"
    checks.append(check("changelog", changelog_status, changelog_evidence, "Section 8 Changelog standard"))

    default_branch = repo.get("default_branch") or ""
    expected_grandfathered = policy.grandfathered_default_branches.get(name)
    if default_branch == "main":
        branch_status, branch_evidence = PASS, "main"
    elif expected_grandfathered == default_branch:
        branch_status, branch_evidence = PASS, f"{default_branch} (documented grandfathered branch)"
    else:
        branch_status, branch_evidence = MANUAL_REVIEW, f"{default_branch or 'missing'}; creation date and migration intent require review"
    checks.append(check("default_branch", branch_status, branch_evidence, "Section 15.1 Default branch"))

    technical = bool(set(domains) & TECHNICAL_DOMAINS)
    canonical_ci = "scripts/ci.sh" in paths
    shell_alternatives = sorted(
        path for path in paths if path in {"tools/check.sh", "ci.sh", "scripts/check.sh"}
    )
    powershell_alternatives = sorted(
        path for path in paths if path in {"scripts/local-ci.ps1", "scripts/ci.ps1", "tools/check.ps1"}
    )
    if not technical or (lifecycle_known and lifecycle not in MAINTAINED_LIFECYCLES):
        local_ci_status = NOT_APPLICABLE
        local_ci_evidence = "not a maintained technical repository"
    elif not lifecycle_known:
        local_ci_status = MANUAL_REVIEW
        local_ci_evidence = "lifecycle is unavailable, so applicability cannot be determined"
    elif canonical_ci and powershell_alternatives:
        local_ci_status = MANUAL_REVIEW
        local_ci_evidence = (
            "scripts/ci.sh plus a PowerShell entry point; verify PowerShell is only a thin launcher: "
            f"{', '.join(powershell_alternatives)}"
        )
    elif canonical_ci:
        local_ci_status = PASS
        local_ci_evidence = "scripts/ci.sh"
    elif tree_incomplete:
        local_ci_status = MANUAL_REVIEW
        local_ci_evidence = f"cannot determine ({tree_reason})"
    elif shell_alternatives:
        local_ci_status = WARN
        local_ci_evidence = f"noncanonical shell entry point: {', '.join(shell_alternatives)}; verify documented exception"
    elif powershell_alternatives:
        local_ci_status = WARN
        local_ci_evidence = f"PowerShell-only entry point: {', '.join(powershell_alternatives)}"
    elif lifecycle in {"Active", "Maintenance"}:
        local_ci_status = FAIL
        local_ci_evidence = "no recognized reproducible local CI entry point"
    else:
        local_ci_status = WARN
        local_ci_evidence = "no recognized local CI entry point; required before promotion to Active"
    checks.append(check("local_ci", local_ci_status, local_ci_evidence, "Section 14.1 Canonical local CI"))

    contributing_present = has_root(roots, ("CONTRIBUTING", "CONTRIBUTING.md"))
    contributing_required = visibility == "public" and lifecycle in MAINTAINED_LIFECYCLES
    if visibility != "public" or (lifecycle_known and lifecycle not in MAINTAINED_LIFECYCLES):
        contributing_status, contributing_evidence = NOT_APPLICABLE, "not required by the deterministic profile"
    elif not lifecycle_known:
        contributing_status, contributing_evidence = MANUAL_REVIEW, "lifecycle is unavailable, so applicability cannot be determined"
    elif contributing_present:
        contributing_status, contributing_evidence = PASS, "present"
    elif tree_incomplete:
        contributing_status, contributing_evidence = MANUAL_REVIEW, f"cannot determine ({tree_reason})"
    elif contributing_required:
        contributing_status, contributing_evidence = FAIL, "required for this public lifecycle"
    else:
        contributing_status, contributing_evidence = NOT_APPLICABLE, "not required by the deterministic profile"
    checks.append(
        check(
            "contributing",
            contributing_status,
            contributing_evidence,
            "Section 7 Documentation requirements",
        )
    )

    security_present = has_root(roots, ("SECURITY", "SECURITY.md"))
    security_required = visibility == "public" and lifecycle in {"Active", "Maintenance"}
    if visibility != "public" or (lifecycle_known and lifecycle not in {"Active", "Maintenance"}):
        security_status, security_evidence = NOT_APPLICABLE, "not required by the deterministic profile"
    elif not lifecycle_known:
        security_status, security_evidence = MANUAL_REVIEW, "lifecycle is unavailable, so applicability cannot be determined"
    elif security_present:
        security_status, security_evidence = PASS, "present"
    elif tree_incomplete:
        security_status, security_evidence = MANUAL_REVIEW, f"cannot determine ({tree_reason})"
    elif security_required:
        security_status, security_evidence = FAIL, "required for public Active or Maintenance repositories"
    else:
        security_status, security_evidence = NOT_APPLICABLE, "not required by the deterministic profile"
    checks.append(
        check(
            "security",
            security_status,
            security_evidence,
            "Section 7 Documentation requirements",
        )
    )

    releasing_present = has_root(roots, ("RELEASING", "RELEASING.md"))
    if lifecycle_known and lifecycle not in MAINTAINED_LIFECYCLES:
        releasing_status, releasing_evidence = NOT_APPLICABLE, "not a maintained release candidate"
    elif not lifecycle_known:
        releasing_status, releasing_evidence = MANUAL_REVIEW, "lifecycle is unavailable, so applicability cannot be determined"
    elif releasing_present:
        releasing_status, releasing_evidence = PASS, "present"
    elif lifecycle in MAINTAINED_LIFECYCLES:
        releasing_status, releasing_evidence = MANUAL_REVIEW, "publication/versioned-deliverable status is not machine-inferable"
    else:
        releasing_status, releasing_evidence = NOT_APPLICABLE, "not a maintained release candidate"
    checks.append(check("releasing", releasing_status, releasing_evidence, "Sections 7 and 17 Releases"))

    agents_present = has_root(roots, ("AGENTS.md",))
    if not technical or (lifecycle_known and lifecycle != "Active"):
        agents_status, agents_evidence = NOT_APPLICABLE, "not deterministically required"
    elif not lifecycle_known:
        agents_status, agents_evidence = MANUAL_REVIEW, "lifecycle is unavailable, so applicability cannot be determined"
    elif agents_present:
        agents_status, agents_evidence = PASS, "present"
    elif lifecycle == "Active" and technical:
        agents_status, agents_evidence = MANUAL_REVIEW, "agent use and non-obvious invariants require human classification"
    else:
        agents_status, agents_evidence = NOT_APPLICABLE, "not deterministically required"
    checks.append(check("agent_guidance", agents_status, agents_evidence, "Section 7.1 Agent documentation"))

    workflows = sorted(path for path in paths if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml")))
    hosted_required = visibility == "public" and lifecycle in {"Active", "Maintenance"} and technical
    if workflows and hosted_required:
        hosted_status = PASS
        hosted_evidence = f"{len(workflows)} workflow file(s); boundedness and pinning require content review"
    elif workflows:
        hosted_status = MANUAL_REVIEW
        hosted_evidence = f"{len(workflows)} optional workflow file(s); private cost or nontechnical value requires review"
    elif visibility != "public" or not technical or (lifecycle_known and lifecycle not in {"Active", "Maintenance"}):
        hosted_status, hosted_evidence = NOT_APPLICABLE, "hosted CI not required by visibility/lifecycle profile"
    elif not lifecycle_known:
        hosted_status, hosted_evidence = MANUAL_REVIEW, "lifecycle is unavailable, so applicability cannot be determined"
    elif tree_incomplete:
        hosted_status, hosted_evidence = MANUAL_REVIEW, f"cannot determine ({tree_reason})"
    elif hosted_required:
        hosted_status, hosted_evidence = FAIL, "bounded hosted CI required but no workflow exists"
    else:
        hosted_status, hosted_evidence = NOT_APPLICABLE, "hosted CI not required by visibility/lifecycle profile"
    checks.append(check("hosted_ci", hosted_status, hosted_evidence, "Section 14 Continuous integration"))

    protection = snapshot.get("protection")
    protection_required = lifecycle in {"Active", "Maintenance"}
    if protection is not None and protection.get("unavailable"):
        protection_status = MANUAL_REVIEW
        protection_evidence = f"GitHub did not expose protection data: {protection['unavailable']}"
    elif not lifecycle_known:
        protection_status = MANUAL_REVIEW
        protection_evidence = "lifecycle is unavailable, so applicability cannot be determined"
    elif protection is None:
        protection_status = FAIL if protection_required else NOT_APPLICABLE
        protection_evidence = "default branch is unprotected" if protection_required else "not required before Active"
    else:
        required_checks = protection.get("required_checks", [])
        conversation = protection.get("conversation_resolution")
        force_pushes = protection.get("allow_force_pushes")
        deletions = protection.get("allow_deletions")
        stable_ci_required = hosted_required and bool(workflows)
        has_stable_ci = any(
            context.casefold() == "ci" or context.casefold().endswith(" / ci")
            for context in required_checks
        )
        safety_floor = protection_required and conversation and not force_pushes and not deletions
        if not safety_floor:
            protection_status = WARN
        elif stable_ci_required and not has_stable_ci:
            protection_status = WARN
        elif hosted_required and tree_incomplete and not has_stable_ci:
            protection_status = MANUAL_REVIEW
        else:
            protection_status = PASS
        protection_evidence = (
            f"protected via {protection.get('source', 'unknown')}; checks={required_checks or 'none'}, "
            f"conversation_resolution={conversation}, allow_force_pushes={force_pushes}, "
            f"allow_deletions={deletions}"
        )
    checks.append(check("branch_protection", protection_status, protection_evidence, "Section 15.2 Protection profile"))

    if visibility != "public":
        hardening_status, hardening_evidence = NOT_APPLICABLE, "not a public workflow surface"
    elif workflows:
        hardening_status = MANUAL_REVIEW
        hardening_evidence = "inspect permissions, immutable action pins, concurrency, timeouts, duplication, and aggregate ci"
    elif tree_incomplete:
        hardening_status, hardening_evidence = MANUAL_REVIEW, f"cannot determine ({tree_reason})"
    else:
        hardening_status, hardening_evidence = NOT_APPLICABLE, "not a public workflow surface"
    checks.append(
        check(
            "public_ci_hardening",
            hardening_status,
            hardening_evidence,
            "Section 14.3 Public repositories",
        )
    )

    counts = Counter(item["status"] for item in checks)
    return {
        "name": name,
        "url": repo.get("html_url"),
        "visibility": visibility,
        "default_branch": default_branch,
        "lifecycle": lifecycle,
        "domains": domains,
        "tree_truncated": bool(snapshot.get("tree_truncated")),
        "summary": {status: counts.get(status, 0) for status in STATUSES},
        "checks": checks,
    }


def collect_snapshot(org: str, repository: dict[str, Any]) -> dict[str, Any]:
    name = validate_name(repository["name"], "repository name")
    owner = quote(org, safe="")
    repo = quote(name, safe="")
    values = gh_get(f"/repos/{owner}/{repo}/properties/values")

    branch_value = repository.get("default_branch")
    if not isinstance(branch_value, str) or not branch_value:
        return {
            "repository": repository,
            "properties": property_map(values),
            "paths": [],
            "tree_truncated": False,
            "tree_unavailable": "repository has no default branch",
            "protection": {"unavailable": "repository has no default branch"},
        }

    branch = validate_name(branch_value, "default branch")
    branch_path = quote(branch, safe="")
    tree = gh_get(f"/repos/{owner}/{repo}/git/trees/{branch_path}?recursive=1")
    classic_raw = gh_get(
        f"/repos/{owner}/{repo}/branches/{branch_path}/protection",
        allow_not_found=True,
        allow_forbidden=True,
    )
    rules_raw = gh_get(
        f"/repos/{owner}/{repo}/rules/branches/{branch_path}",
        allow_not_found=True,
        allow_forbidden=True,
        paginate=True,
    )

    classic_unavailable = isinstance(classic_raw, dict) and classic_raw.get("_audit_unavailable")
    rules_unavailable = isinstance(rules_raw, dict) and rules_raw.get("_audit_unavailable")
    if classic_unavailable and rules_unavailable:
        protection: dict[str, Any] | None = {
            "unavailable": f"classic protection: {classic_unavailable}; rulesets: {rules_unavailable}"
        }
    else:
        contexts: list[str] = []
        conversation = False
        prohibit_force_pushes = False
        prohibit_deletions = False
        sources: list[str] = []

        if isinstance(classic_raw, dict) and not classic_unavailable:
            sources.append("classic")
            status_checks = classic_raw.get("required_status_checks") or {}
            contexts.extend(status_checks.get("contexts") or [])
            contexts.extend(
                item.get("context")
                for item in status_checks.get("checks") or []
                if item.get("context")
            )
            conversation = bool((classic_raw.get("required_conversation_resolution") or {}).get("enabled"))
            prohibit_force_pushes = not bool((classic_raw.get("allow_force_pushes") or {}).get("enabled"))
            prohibit_deletions = not bool((classic_raw.get("allow_deletions") or {}).get("enabled"))

        if isinstance(rules_raw, list) and rules_raw:
            sources.append("ruleset")
            rule_types = {item.get("type") for item in rules_raw if isinstance(item, dict)}
            prohibit_force_pushes = prohibit_force_pushes or "non_fast_forward" in rule_types
            prohibit_deletions = prohibit_deletions or "deletion" in rule_types
            for rule in rules_raw:
                if not isinstance(rule, dict):
                    continue
                parameters = rule.get("parameters") or {}
                if rule.get("type") == "required_status_checks":
                    contexts.extend(
                        item.get("context")
                        for item in parameters.get("required_status_checks") or []
                        if item.get("context")
                    )
                if rule.get("type") == "pull_request":
                    conversation = conversation or bool(parameters.get("required_review_thread_resolution"))

        if sources:
            protection = {
                "source": "+".join(sources),
                "required_checks": sorted(set(contexts)),
                "conversation_resolution": conversation,
                "allow_force_pushes": not prohibit_force_pushes,
                "allow_deletions": not prohibit_deletions,
            }
        elif classic_raw is None and rules_raw == []:
            protection = None
        else:
            unavailable = []
            if classic_unavailable:
                unavailable.append(f"classic protection: {classic_unavailable}")
            if rules_unavailable:
                unavailable.append(f"rulesets: {rules_unavailable}")
            protection = {"unavailable": "; ".join(unavailable) or "protection sources were inconclusive"}

    return {
        "repository": repository,
        "properties": property_map(values),
        "paths": [item["path"] for item in tree.get("tree", [])],
        "tree_truncated": tree.get("truncated", False),
        "tree_unavailable": None,
        "protection": protection,
    }


def select_repositories(
    repositories: list[dict[str, Any]],
    requested: list[str],
    scope: str,
    policy: Policy,
) -> list[dict[str, Any]]:
    by_name = {repo["name"]: repo for repo in repositories}
    if requested:
        names = [validate_name(name, "repository name") for name in requested]
    elif scope == "active":
        names = list(policy.active_cohort)
    else:
        names = sorted(by_name)

    missing = sorted(set(names) - set(by_name))
    if missing:
        raise AuditError(f"repositories not found: {', '.join(missing)}")
    return [by_name[name] for name in names]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Photon Circus Repository Standards Audit",
        "",
        f"Generated: **{report['generated_at']}**  ",
        f"Organization: **{report['organization']}**  ",
        f"Scope: **{report['scope']}**  ",
        "Mode: **read-only evidence collection; findings authorize no changes**",
        "",
        "| Repository | Lifecycle | Visibility | Pass | Fail | Warn | Manual | N/A |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for repo in report["repositories"]:
        summary = repo["summary"]
        lines.append(
            f"| [{repo['name']}]({repo['url']}) | {repo['lifecycle'] or 'missing'} | "
            f"{repo['visibility']} | {summary[PASS]} | {summary[FAIL]} | {summary[WARN]} | "
            f"{summary[MANUAL_REVIEW]} | {summary[NOT_APPLICABLE]} |"
        )

    for repo in report["repositories"]:
        findings = [item for item in repo["checks"] if item["status"] != PASS]
        if not findings:
            continue
        lines.extend(["", f"## {repo['name']}", "", "| Status | Check | Evidence | Standard |", "| --- | --- | --- | --- |"])
        for item in findings:
            evidence = item["evidence"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {item['status']} | `{item['id']}` | {evidence} | {item['standard']} |")

    lines.extend(
        [
            "",
            "## Authority boundary",
            "",
            "This report is evidence only. It does not authorize remediation, repository writes, settings changes, visibility changes, lifecycle transitions, tagging, publishing, or release actions. Each accepted change requires a separately reviewed bound.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Read-only Photon Circus repository standards audit")
    parser.add_argument("--org", default="photon-circus", help="GitHub organization (default: photon-circus)")
    parser.add_argument("--scope", choices=("active", "all"), default="active")
    parser.add_argument("--repo", action="append", default=[], help="audit one repository; repeatable")
    parser.add_argument("--policy", type=Path, default=root / "standards" / "audit-policy.json")
    parser.add_argument("--output-dir", type=Path, default=root / "audit-output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        org = validate_name(args.org, "organization name")
        policy = load_policy(args.policy)
        repositories = gh_get(
            f"/orgs/{quote(org, safe='')}/repos?type=all&per_page=100",
            paginate=True,
        )
        if not isinstance(repositories, list):
            raise AuditError("organization repository response was not a list")
        selected = select_repositories(repositories, args.repo, args.scope, policy)
        evaluated = [evaluate_repository(collect_snapshot(org, repo), policy) for repo in selected]
        totals = Counter(
            item["status"]
            for repo in evaluated
            for item in repo["checks"]
        )
        scope_name = "explicit repositories" if args.repo else args.scope
        report = {
            "schema_version": 1,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "organization": org,
            "scope": scope_name,
            "read_only": True,
            "authority": "evidence-only; findings authorize no changes",
            "summary": {status: totals.get(status, 0) for status in STATUSES},
            "repositories": evaluated,
        }
        args.output_dir.mkdir(parents=True, exist_ok=True)
        json_path = args.output_dir / "repository-standards-audit.json"
        markdown_path = args.output_dir / "repository-standards-audit.md"
        json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        markdown_path.write_text(render_markdown(report), encoding="utf-8")
        print(f"wrote {json_path}")
        print(f"wrote {markdown_path}")
        print("read-only audit complete; findings authorize no changes")
        return 0
    except AuditError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
