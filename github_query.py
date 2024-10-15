"""
This script is written in a certain - maybe even unconventional way - by intention.
It's supposed to be run from comamndline right away to be used in a github action workflow yaml file.
Additonally it's test suite relies mainly on putest and therefore the functions need to be importable to the pytest script.
"""

import argparse
import json
import logging
import re
import subprocess

from collections import namedtuple


logger = logging.getLogger(__name__)

def parse_args() -> dict:
    """Parse command-line arguments and store them in a global variable."""

    parser = argparse.ArgumentParser(description="A python script to convert GitHub PR information to a more simple format.")
    parser.add_argument("repo", type=str, help="Repository name consisting of 'repo-owner/repo-name'")
    parser.add_argument("query_parameters", type=str, help="Keys to query for.")
    parser.add_argument("date", type=str, default="2024-07-08T09:48:33Z", help="Latest release date.")
    parsed_args = parser.parse_args()

    repo_name = parsed_args.repo
    query_tags = parsed_args.query_parameters.split(',')
    latest_release_date = parsed_args.date

    command = f"gh pr list --state merged --search 'merged:>={latest_release_date}' --json {','.join(query_tags)} --repo {repo_name}"
    pr_json = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    return json.loads(pr_json.stdout)

def get_changelog(pr_data, changelog_start="## Changelog", heading="##"):
    """Get list of changes from a PRs changelog.

    Args:
        pr_body (list(str)): List of PR body contents.
        changelog_start (str, optional): Indicates markdown changelog section. Defaults to "## Changes".
        heading (str, optional): Markdown heading. Defaults to "##".

    Returns:
        list(str): List of changes found.
    """

    lines = pr_data.splitlines()
    changelog_section = None
    changelog_lines = []

    for line in lines:
        if line.startswith(changelog_start):
            changelog_section = True
            continue

        if changelog_section and line.startswith(heading):
            break

        if changelog_section and line.startswith("* "):
            changelog_lines.append(line.strip("* ").strip())

    return changelog_lines

def filter_changelog_per_label(pr_data, changelog_label_list):
    
    Changelog = namedtuple("Changelog", "labels title number url id")
    changes_list = []

    for pull_request in pr_data:

        label_list = [label["name"] for label in pull_request["labels"] if label["name"] in changelog_label_list]
        if label_list:
            changes_list.append(Changelog(label_list, pull_request["title"], pull_request["number"], pull_request["url"], pull_request["id"]))

    return changes_list

def changelog_per_label(json_dict):
    # TODO replace with labels fetched from repo variables
    changelog_labels = ["bugfix", "enhancement", "feature"]
    labels = []
    for item in json_dict:
        labels.append(item["labels"])
        if any(item in changelog_labels for item in labels):
            pass

def build_changelog_markdown(filtered_pr_data, changelog_label_list):
    changelog = "# Changelog"

    for pr_data in filtered_pr_data:
        
        pr_data.labels in pr_data
        if fitlered_label:
            change_list = get_changelog(pr_data=pr["body"])
            
            changelog += f"## {fitlered_label.capitalize()}\n"
            changelog += "".join([f"* {change}\n" for change in change_list])
            changelog += "\n"

    return changelog


def get_labels(pr_data: dict) -> list:
    """Filter all unique labels from dictionary.

    Args:
        pr_data (dict): Github PR query result

    Returns:
        [str]: Liste of unique labels strings found or `None`.
    """

    labels = set()

    for item in pr_data:
        if not item.get("labels"):
            return []
        for label in item["labels"]:
            if not label.get("name"):
                return []

            labels.add(label["name"])

    return list(labels)

def get_repo_var(repo: str, var_name: str) -> list:
    """Query labels from repository variables.

    Args:
        repo (str): Repository name `owner/repo-name`
        var_name (str): Repo variable name

    Returns:
        str: Comma separated value string.
    """
    labels = subprocess.run(
        ["gh", "variable", "get", var_name, "--repo", repo],
        capture_output=True,
        text=True,
        check=True
    )

    return csv_string_to_list(labels.stdout)

def csv_string_to_list(input: str) -> list:
    if input:
        return re.split(r',\s*', input.strip())

    return []

def get_version_increment(patch_bump_list: list, minor_bump_list: list, pr_label_list: list):
    """Figure out version increment based on PR labels.

    Args:
        patch_bump_list ([str]): Labels for bumping patch version
        minor_bump_list ([str]): Labels for bumping minor version
        label_list([str]): Labels found in PRs

    Returns:
        str: version increment
    """

    if not pr_label_list:
        return ""

    # TODO add major bump option
    if any(label in pr_label_list for label in minor_bump_list):
        return "minor"

    if any(label in pr_label_list for label in patch_bump_list):
        return "patch"

    return ""

if __name__ == '__main__':

    # TODO remove before merging
    command = f"gh pr list --state merged --search 'merged:>=2024-08-01T11:29:22Z' --json body,labels,title,number,url,id --repo ynput/ayon-maya"
    pr_json = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pr_data = json.loads(pr_json.stdout)

    changelog_labels = ["type: bug", "type: enhancement", "type: maintenance"]
    pr_filtered = filter_changelog_per_label(pr_data=pr_data, changelog_label_list=changelog_labels):
    changelog = build_changelog_markdown(filtered_pr_data=pr_filtered, changelog_label_list=changelog_labels)

    print(changelog)
