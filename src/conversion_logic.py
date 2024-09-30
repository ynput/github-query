import logging
import re


logger = logging.getLogger(__name__)

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
        filtered_label = list(set(label_list).intersection(pr_label_list))[0]

        if filtered_label:
            change_list = get_changelog(pr_data=pr["body"])
            
            changelog += f"## {filtered_label.capitalize()}\n"
            changelog += "".join([f"* {change}\n" for change in change_list])
            changelog += "\n"

    return changelog


def get_labels(pr_data: dict) -> list:
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

def csv_string_to_list(input: str) -> list:
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