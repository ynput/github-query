import logging
import re

from typing import NamedTuple, List, Set

logger: logging.Logger = logging.getLogger(__name__)


class Changelog(NamedTuple):
    labels: List[str]
    title: str
    number: int
    url: str
    id: int
    body: str


def filter_unique_labels(pr_data: List[dict[str, str]]) -> List[str]:
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


def csv_string_to_list(input: str) -> List[str]:
    """Convert string to list.

    Args:
        input (str): Expected csv string.

    Returns:
        list: List of strings.
    """

    if input:
        return re.split(r',\s*', input.strip())

    return []


def get_version_increment(pr_label_list: List[str], patch_bump_list: List[str]=[], minor_bump_list: List[str]=[], major_bump_list: List[str]=[]):
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


def filter_changes_per_label(pr_data: List[dict[str, str]], changelog_label_list: List[str]) -> List[Changelog]:
    """Convert list of PR dictionaries to Changelog list

    Args:
        pr_data (list[dict[str, str]]): PR information and metadata
        changelog_label_list (list[str]): Changelog labels

    Returns:
        list[Changelog]: List of changelog objects
    """

    changes_list: List[Changelog] = []

    for pull_request in pr_data:
        if pull_request.get("labels"):
            changes_list.append(Changelog(labels=[label["name"] for label in pull_request["labels"]],
                                           title=pull_request["title"],
                                           number=pull_request["number"],
                                           url=pull_request["url"],
                                           id=pull_request["id"],
                                           body=pull_request["body"],
                                           )
                                        )

    return changes_list


def get_changelog(pr_body: str, changelog_desc: str ="## Changelog Description", heading: str ="##") -> List[str]:
    """Get list of changes from a PRs changelog.

    Args:
        pr_body list(str): PR body content
        changelog_desc (str, optional): Indicates markdown changelog section. Defaults to "## Changes"
        heading (str, optional): Markdown heading. Defaults to "##"

    Returns:
        list(str): List of changes found.
    """

    lines: list[str] = pr_body.splitlines()
    changelog_section = None
    description_lines: list[str] = []

    for line in lines:
        if line.startswith(changelog_desc):
            changelog_section = True
            continue

        if changelog_section and line.startswith(heading):
            break

        if changelog_section:
            description_lines.append(line.strip())

    return description_lines


def format_changelog_markdown(changes: List[Changelog], changelog_label_list: List[str]) -> str:
    """Create markdown formatted changelog.

    Args:
        changes (list[Changelog]): Changelogs in a list
        changelog_label_list (list[str]): Label list to control order and filtering

    Returns:
        str: Markdown formatted string
    """

    changelog = "# Changelog\n"
    change_label_list: set[str] = {label for change in changes for label in change.labels}

    for label in changelog_label_list:
        if label not in change_label_list:
            continue

        formatted_label: str = label.removeprefix("type: ").capitalize()
        changelog += f"\n### **{formatted_label}**\n\n"

        for change in changes:
            if label in change.labels:
                changelog_desc: List[str] = get_changelog(change.body, changelog_desc="## Changelog Description", heading="##")

                changelog += f"<details>\n"
                changelog += f"<summary>{change.title} - [#{change.number}]({change.url})</summary>\n\n"
                
                for desc_line in changelog_desc:
                    changelog += f"{desc_line}\n"

                changelog += f"___\n\n"
                changelog += f"</details>\n"

    return changelog