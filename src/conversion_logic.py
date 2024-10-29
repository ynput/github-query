import logging
import re

from collections import namedtuple


logger: logging.Logger = logging.getLogger(__name__)
Changelog: type[Changelog] = namedtuple("Changelog", "labels title number url id")


def sort_changes(changes_list: list[Changelog], changelog_label_list: list[str]) -> list[Changelog]:

    # TODO implement this logic in a more clever way
    sorted_changes: list[Changelog] = []

    for order_label in changelog_label_list:
        for change in changes_list:
            if any(label == order_label for label in change.labels):
                sorted_changes.append(change)

    return sorted_changes


# INFO currently not in use
def get_changelog(pr_data, changelog_start="## Changelog", heading="##"):
    """Get list of changes from a PRs changelog.

    Args:
        pr_body (list(str)): List of PR body contents.
        changelog_start (str, optional): Indicates markdown changelog section. Defaults to "## Changes".
        heading (str, optional): Markdown heading. Defaults to "##".

    Returns:
        list(str): List of changes found.
    """

    lines: list[str] = pr_data.splitlines()
    changelog_section = None
    changelog_lines: list[str] = []

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


def filter_unique_labels(pr_data: dict[dict[str, str]]) -> list[str]:
    """Filter all unique labels from dictionary.

    Args:
        pr_data (dict): Github PR query result

    Returns:
        list: List of unique labels strings found or `None`.
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


def csv_string_to_list(input: str) -> list[str]:
    """Convert string to list.

    Args:
        input (str): Expected csv string.

    Returns:
        list: List of strings.
    """

    if input:
        return re.split(r',\s*', input.strip())

    return []


def get_version_increment(pr_label_list: list, patch_bump_list: list=[], minor_bump_list: list=[], major_bump_list: list=[]):
    """Figure out version increment based on PR labels.

    Args:
        patch_bump_list ([str]): Labels for bumping patch version
        minor_bump_list ([str]): Labels for bumping minor version
        label_list ([str]): Labels found in PRs

    Returns:
        str: version increment
    """

    if not pr_label_list:
        logger.warning("PR label list was empty")
        return ""

    for name, param in locals().items():
        if not isinstance(param, list):
            raise ValueError(f"{name} must be a list.")

    if any(label in pr_label_list for label in major_bump_list):
        return "major"

    if any(label in pr_label_list for label in minor_bump_list):
        return "minor"

    if any(label in pr_label_list for label in patch_bump_list):
        return "patch"

    logger.warning("No relevant labels found for version increment.")
    return ""