"""
This script is written in a certain - maybe even unconventional way - by intention.
It's supposed to be run from comamndline right away to be used in a github action workflow yaml file.
Additonally it's test suite relies mainly on putest and therefore the functions need to be importable to the pytest script.
"""

import click
import json
import logging
import re
import subprocess


logger = logging.getLogger(__name__)

def query_merged_prs(latest_release_date, query_tags, repo_name):
    """Run gh pull request query.

    Args:
        latest_release_date (str): datatime string
        query_tags (str): csv string
        repo_name (str): repo name as <owner><repo>

    Returns:
        dict: json-dictionary.
    """

    pr_list = subprocess.run(
        [
            "gh", "pr", "list", 
            "--state", "merged", 
            "--search", f'merged:>={latest_release_date}', 
            "--json", ','.join(query_tags), 
            "--repo", repo_name
        ],
        capture_output=True,
        text=True,
        check=True
    )

    return json.loads(pr_list.stdout)

# INFO not in use
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

# INFO not in use
def changelog_per_label(json_dict):
    # TODO replace with labels fetched from repo variables
    changelog_labels = ["bugfix", "enhancement", "feature"]
    labels = []
    for item in json_dict:
        labels.append(item["labels"])
        if any(item in changelog_labels for item in labels):
            pass

# INFO not in use
def prepare_changelog_markdown(pr_query, minor_bump_list, patch_bump_list):   
    # ? should version bump labels also be filter for changelog ?
    label_list = minor_bump_list + patch_bump_list
    changelog = ""

    for pr in pr_query:
        # get all label names in a list
        pr_label_list = [label["name"] for label in pr["labels"]]
        fitlered_label = list(set(label_list).intersection(pr_label_list))[0]

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
        list: Liste of unique labels strings found or `None`.
    """

    labels = set()

    for item in pr_data:
        if not item.get("labels"):
            logger.warning("No PR label data found.")
            return []
        for label in item["labels"]:
            if not label.get("name"):
                logger.warning("No PR label names found.")
                return []

            labels.add(label["name"])
            logger.debug("PR labels found.")

    return list(labels)

def get_repo_var(repo: str, var_name: str) -> list:
    """Query labels from repository variables.

    Args:
        repo (str): Repository name `owner/repo-name`
        var_name (str): Repo variable name

    Returns:
        str: csv-string.
    """
    labels = subprocess.run(
        ["gh", "variable", "get", var_name, "--repo", repo],
        capture_output=True,
        text=True,
        check=True
    )

    return labels.stdout

def csv_string_to_list(input: str) -> list:
    """Covnert string to list.

    Args:
        input (str): Expected csv string.

    Returns:
        list: List of strings.
    """

    if input:
        return re.split(r',\s*', input.strip())

    return []

def get_version_increment(patch_bump_list: list, minor_bump_list: list, pr_label_list: list):
    """Figure out version increment based on PR labels.

    Args:
        patch_bump_list ([str]): Labels for bumping patch version
        minor_bump_list ([str]): Labels for bumping minor version
        label_list ([str]): Labels found in PRs

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

    logger.warning("No relevant labels found for version increment.")
    return ""

# CLI using Click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('repo_name', type=click.STRING)
@click.argument('query_tags', type=click.STRING)
@click.argument('latest_release_date', type=click.STRING)
def pr_labels(latest_release_date, query_tags, repo_name):
    """Get a list of all version relevant PR labels.

    latest_release_date (str): datatime string\n
    query_tags (str): csv string\n
    repo_name (str): repo name as <owner><repo>\n
    """

    pr_result = query_merged_prs(latest_release_date, query_tags, repo_name)
    pr_labels = get_labels(pr_data=pr_result)

    if not pr_labels:
        click.echo("")

    click.echo(pr_labels)


@cli.command()
@click.argument('repo_name', type=click.STRING)
@click.argument('query_tags', type=click.STRING)
@click.argument('latest_release_date', type=click.STRING)
def version_increment(latest_release_date, query_tags, repo_name):
    """Output a calculated version increment suggestion.

    latest_release_date (str): datatime string\n
    query_tags (str): csv string\n
    repo_name (str): repo name as <owner><repo>\n
    """

    pr_result = query_merged_prs(latest_release_date, query_tags, repo_name)
    pr_labels = get_labels(pr_data=pr_result)
    patch_repo_var_list = csv_string_to_list(get_repo_var(repo=repo_name, var_name="PATCH_BUMP_LABEL"))
    minor_repo_var_list = csv_string_to_list(get_repo_var(repo=repo_name, var_name="MINOR_BUMP_LABEL"))
    increment = get_version_increment(patch_bump_list=patch_repo_var_list, minor_bump_list=minor_repo_var_list, pr_label_list=pr_labels)

    click.echo(increment)


if __name__ == '__main__':
    cli()