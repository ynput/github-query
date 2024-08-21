import argparse
import json
import subprocess

def collect_inputs():
    """Get parameters for gh command.

    Returns:
        json dict: dictionary retunred from github api.
    """

    parser = argparse.ArgumentParser(description="A python script to convert github pr information to a more simple format.")
    parser.add_argument("repo", type=str, help="Repository name consisting of 'repo-owner/repo-name'")
    parser.add_argument('query_parameters', type=str, help='Keys to query for.')
    parser.add_argument('date', type=str, default="2024-07-08T09:48:33Z", help='Latest release date.')
    args = parser.parse_args()

    repo = args.repo
    query_tags = args.query_parameters.split(',')
    latest_release_date = args.date

    command = f"gh pr list --state merged --search 'merged:>={latest_release_date}' --json {','.join(query_tags)} --repo {repo}"
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

def changelog_per_label(json_dict):
    changelog_labels = ["bug", "enhancement", "feature"]
    labels = []
    for item in json_dict:
        labels.append(item["labels"])
        if any(item in changelog_labels for item in labels):
            pass

def prepare_changelog_markdown(collect_inputs, get_changelog):
    pr_output_list = []
    pr_output = {}

    for pr_data in collect_inputs():
        labels = pr_data["labels"]
        changelog_markdown = ""

        changelog_markdown =+ f"## {labels}"
        pr_output["title"] = pr_data["title"]
        pr_output["label_name"] = [label["name"] for label in pr_data["labels"]]
        pr_output["changelog"] = get_changelog(pr_data=pr_data["body"], changelog_start="## Changes")  # TODO udpate to "changelog"

        pr_output_list.append(pr_output)

    return pr_output_list

def get_labels():
    github_data = collect_inputs()
    labels = set()

    for item in github_data:
        for label in item["labels"]:
            labels.add(label["name"])

    return json.dumps(list(labels))

def get_version_increment():
    # TODO get rpo string dynamically
    minor_bump_label= subprocess.run(
        ["gh", "variable", "get", "MINOR_BUMP_LABEL", "--repo", "ynput/ayon-addon-action-testing"],
        capture_output=True,
        text=True,
        check=True
    )
    minor_bump_label_list = minor_bump_label.stdout.strip().split(", " or ",")

    patch_bump_label= subprocess.run(
        ["gh", "variable", "get", "PATCH_BUMP_LABEL", "--repo", "ynput/ayon-addon-action-testing"],
        capture_output=True,
        text=True,
        check=True
    )
    patch_bump_label_list = patch_bump_label.stdout.strip().split(", " or ",")

    for label in json.loads(get_labels()):
        if label.lower() in minor_bump_label_list:
            return "minor"
        if label.lower() in patch_bump_label_list:
            return "patch"
