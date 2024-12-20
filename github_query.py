"""
This script is supposed to be run from command line right away to be used in a github action workflow yaml file.
Additionally it's test suite relies mainly on pytest and therefore the functions need to be importable to the pytest script.
"""

import click
from src import conversion_logic, queries
from typing import List


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument('repo_name', type=click.STRING)
@click.argument('base_branch', type=click.STRING)
@click.argument('query_tags', type=click.STRING)
@click.argument('latest_release_date', type=click.STRING)
def pr_labels(latest_release_date: str, query_tags: str, base_branch: str, repo_name: str) -> None:
    """Get a list of all version relevant PR labels.

    latest_release_date (str): datatime string\n
    query_tags (str): csv string\n
    repo_name (str): repo name as <owner><repo>\n
    """
    
    query_tags_list: List[str] = conversion_logic.csv_string_to_list(input=query_tags)
    pr_result: List[dict[str, str]] = queries.query_merged_prs(latest_release_date, query_tags_list, base_branch, repo_name)
    pr_labels: List[str] = conversion_logic.filter_unique_labels(pr_data=pr_result)

    if not pr_labels:
        click.echo("")
        return

    click.echo(pr_labels)


@cli.command()
@click.argument('repo_name', type=click.STRING)
@click.argument('base_branch', type=click.STRING)
@click.argument('query_tags', type=click.STRING)
@click.argument('latest_release_date', type=click.STRING)
def version_increment(latest_release_date: str, query_tags: str, base_branch: str, repo_name: str) -> None:
    """Output a calculated version increment suggestion.

    latest_release_date (str): datetime string\n
    query_tags (str): csv string\n
    repo_name (str): repo name as <owner><repo>\n
    """

    query_tags_list: list[str] = conversion_logic.csv_string_to_list(query_tags)
    pr_result: list[dict[str, str]] = queries.query_merged_prs(latest_release_date, query_tags_list, base_branch, repo_name)
    pr_labels: conversion_logic.List[str] = conversion_logic.filter_unique_labels(pr_data=pr_result)
    patch_repo_var_list: conversion_logic.List[str] = conversion_logic.csv_string_to_list(queries.get_repo_var(repo=repo_name, var_name="PATCH_BUMP_LABEL"))
    minor_repo_var_list: conversion_logic.List[str] = conversion_logic.csv_string_to_list(queries.get_repo_var(repo=repo_name, var_name="MINOR_BUMP_LABEL"))
    increment = conversion_logic.get_version_increment(patch_bump_list=patch_repo_var_list, minor_bump_list=minor_repo_var_list, pr_label_list=pr_labels)

    click.echo(increment)


@cli.command()
@click.argument('repo_name', type=click.STRING)
@click.argument('base_branch', type=click.STRING)
@click.argument('query_tags', type=click.STRING)
@click.argument('latest_release_date', type=click.STRING)
@click.argument('changelog_labels', type=click.STRING)
def generate_release_changelog(latest_release_date: str, query_tags: str, base_branch: str, repo_name: str, changelog_labels: str) -> None:
    """Output a markdown formatted changelog.

    latest_release_date (str): datetime string\n
    query_tags (str): csv string\n
    repo_name (str): repo name as <owner><repo>\n
    """

    query_tags_list: list[str] = conversion_logic.csv_string_to_list(query_tags)
    pr_result: list[dict[str, str]] = queries.query_merged_prs(latest_release_date, query_tags_list, base_branch, repo_name)
    changelog_labels_result: list[str] = conversion_logic.csv_string_to_list(changelog_labels)
    pr_filtered: list[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=pr_result, changelog_label_list=changelog_labels_result)
    markdown_changelog: str = conversion_logic.format_changelog_markdown(changes=pr_filtered, changelog_label_list=changelog_labels_result)

    click.echo(markdown_changelog)

if __name__ == "__main__":
    cli()
