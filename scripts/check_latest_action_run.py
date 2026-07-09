#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from typing import Any
from urllib.parse import urlencode


GITHUB_API = "https://api.github.com"


def git_output(*args: str) -> str:
    return subprocess.check_output(("git", *args), text=True).strip()


def resolve_repo() -> tuple[str, str]:
    remote_url = git_output("remote", "get-url", "origin")
    https_match = re.match(r"https://github\.com/([^/]+)/([^/.]+)(?:\.git)?$", remote_url)
    ssh_match = re.match(r"git@github\.com:([^/]+)/([^/.]+)(?:\.git)?$", remote_url)
    match = https_match or ssh_match
    if not match:
        raise SystemExit(f"Unsupported GitHub remote URL: {remote_url}")
    return match.group(1), match.group(2)


def resolve_sha(value: str | None) -> str:
    if value is None or value == "HEAD":
        return git_output("rev-parse", "HEAD")
    return value


def github_json(path: str, params: dict[str, str] | None = None) -> Any:
    query = f"?{urlencode(params)}" if params else ""
    url = f"{GITHUB_API}{path}{query}"
    try:
        output = subprocess.check_output(
            (
                "curl",
                "-fsSL",
                "-H",
                "Accept: application/vnd.github+json",
                "-H",
                "User-Agent: portfolio-local-actions-check",
                url,
            ),
            text=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as error:
        raise SystemExit(f"GitHub API request failed:\n{error.output}") from error
    return json.loads(output)


def find_run(owner: str, repo: str, branch: str, sha: str) -> dict[str, Any] | None:
    payload = github_json(
        f"/repos/{owner}/{repo}/actions/runs",
        {"branch": branch, "per_page": "20"},
    )
    for run in payload.get("workflow_runs", []):
        if run.get("head_sha") == sha:
            return run
    return None


def print_failed_jobs(owner: str, repo: str, run_id: int) -> None:
    jobs = github_json(
        f"/repos/{owner}/{repo}/actions/runs/{run_id}/jobs",
        {"per_page": "100"},
    ).get("jobs", [])

    for job in jobs:
        conclusion = job.get("conclusion")
        if conclusion in (None, "success", "skipped"):
            continue

        print(f"- job `{job.get('name')}`: {conclusion} ({job.get('html_url')})")
        steps = job.get("steps") or []
        if steps:
            for step in steps:
                step_conclusion = step.get("conclusion")
                if step_conclusion not in (None, "success", "skipped"):
                    print(f"  - step `{step.get('name')}`: {step_conclusion}")
            continue

        check_run_url = job.get("check_run_url", "")
        check_run_id = check_run_url.rstrip("/").split("/")[-1]
        if not check_run_id:
            continue

        annotations = github_json(
            f"/repos/{owner}/{repo}/check-runs/{check_run_id}/annotations"
        )
        for annotation in annotations:
            message = annotation.get("message")
            if message:
                print(f"  - annotation: {message}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check the latest GitHub Actions run for the current commit."
    )
    parser.add_argument("--branch", default="main")
    parser.add_argument("--sha", default="HEAD")
    parser.add_argument("--wait", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--poll-seconds", type=int, default=15)
    args = parser.parse_args()

    owner, repo = resolve_repo()
    sha = resolve_sha(args.sha)
    deadline = time.monotonic() + args.timeout_seconds

    while True:
        run = find_run(owner, repo, args.branch, sha)
        if run is None:
            if not args.wait or time.monotonic() >= deadline:
                print(f"No GitHub Actions run found for {sha} on {args.branch}.")
                return 1
            time.sleep(args.poll_seconds)
            continue

        status = run.get("status")
        conclusion = run.get("conclusion")
        url = run.get("html_url")
        print(f"GitHub Actions run: {status}/{conclusion} {url}")

        if status != "completed":
            if not args.wait or time.monotonic() >= deadline:
                return 1
            time.sleep(args.poll_seconds)
            continue

        if conclusion == "success":
            return 0

        print_failed_jobs(owner, repo, int(run["id"]))
        return 1


if __name__ == "__main__":
    sys.exit(main())
