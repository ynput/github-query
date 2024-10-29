"""
This script is supposed to be run from command line right away to be used in a github action workflow yaml file.
Additionally it's test suite relies mainly on pytest and therefore the functions need to be importable to the pytest script.
"""

import argparse
import click
import json
import logging
import re
import subprocess

from collections import namedtuple

from src import conversion_logic, queries


logger: logging.Logger = logging.getLogger(__name__)

Changelog: type[Changelog] = namedtuple("Changelog", "labels title number url id")


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

    command: str = f"gh pr list --state merged --search 'merged:>={latest_release_date}' --json {','.join(query_tags)} --repo {repo_name}"
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


def filter_changes_per_label(pr_data: list[dict[str, str]], changelog_label_list: list[str]) -> list[Changelog]:

    changes_list: list[Changelog] = []

    for pull_request in pr_data:

        # TODO refactor this to become more readable
        label_list: list[str] = [label["name"] for label in pull_request["labels"] if label["name"] in changelog_label_list]
        if label_list:
            changes_list.append(Changelog(label_list, pull_request["title"], pull_request["number"], pull_request["url"], pull_request["id"]))

    return changes_list


def sort_changes(changes_list: list[Changelog], changelog_label_list: list[str]) -> list[Changelog]:

    # TODO implement this logic in a more clever way
    sorted_changes: list[Changelog] = []

    for order_label in changelog_label_list:
        for change in changes_list:
            if any(label == order_label for label in change.labels):
                sorted_changes.append(change)

    return sorted_changes


def build_changelog_markdown(changes: list[Changelog]) -> str:
    changelog = "# Changelog"
    previous_labels: list[str] = []

    # TODO implement this logic in a more clever way, checkout `from itertools import groupby`
    for change in changes:
        current_labels: list[str] = change.labels
        
        if not any(label in previous_labels for label in current_labels):
            label: str = change.labels[0].removeprefix("type: ")
            changelog += f"\n\n## {label.capitalize()}\n\n"

        changelog += f"* {change.title} - [{change.number}]({change.url})\n"

        previous_labels = current_labels

    return changelog


def get_labels(pr_data: list[dict[str, str]]) -> list[str]:
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


def get_repo_var(repo: str, var_name: str) -> list[str]:
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


def csv_string_to_list(input: str) -> list[str]:
    if input:
        return re.split(r',\s*', input.strip())

    return []


def get_version_increment(patch_bump_list: list[str], minor_bump_list: list[str], pr_label_list: list[str]):
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


@click.group()
def cli():
    pass


@cli.command()
@click.argument('repo_name', type=click.STRING)
@click.argument('query_tags', type=click.STRING)
@click.argument('latest_release_date', type=click.STRING)
@click.argument('changelog_labels', type=click.STRING)
def generate_release_changelog(latest_release_date: str, query_tags: str, repo_name: str, changelog_labels: str) -> None:
    """Output a markdown formatted changelog.

    latest_release_date (str): datetime string\n
    query_tags (str): csv string\n
    repo_name (str): repo name as <owner><repo>\n
    """

    query_tags_list: list[str] = conversion_logic.csv_string_to_list(query_tags)
    pr_result: list[dict[str, str]] = queries.query_merged_prs(latest_release_date, query_tags_list, repo_name)
    changelog_labels_result: list[str] = conversion_logic.csv_string_to_list(changelog_labels)

    pr_filtered: list[Changelog] = filter_changes_per_label(pr_data=pr_result, changelog_label_list=changelog_labels_result)
    sorted_changes: list[Changelog] = sort_changes(changes_list=pr_filtered, changelog_label_list=changelog_labels_result)
    markdown_changelog: str = build_changelog_markdown(sorted_changes)

    click.echo(markdown_changelog)

if __name__ == "__main__":
    cli()
