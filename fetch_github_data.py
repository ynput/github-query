"""
This script is written in a certain - maybe even unconventional way - by intention.
It's supposed to be run from comamndline right away to be used in a github action workflow yaml file.
Additonally it's test suite relies mainly on putest and therefore the functions need to be importable to the pytest script.
"""

import argparse
import json
import subprocess

parsed_args = None

def parse_arguments():
    """Parse command-line arguments and store them in a global variable."""
    global parsed_args
    if parsed_args is None:
        parser = argparse.ArgumentParser(description="A python script to convert GitHub PR information to a more simple format.")
        parser.add_argument("repo", type=str, help="Repository name consisting of 'repo-owner/repo-name'")
        parser.add_argument("query_parameters", type=str, help="Keys to query for.")
        parser.add_argument("date", type=str, default="2024-07-08T09:48:33Z", help="Latest release date.")
        parsed_args = parser.parse_args()


def get_inputs():
    """Get the parsed command-line arguments.

    Returns:
        tuple(str): Parameters as string tuple.
    """

    if parsed_args is None:
        parse_arguments()
    
    repo_name = parsed_args.repo
    query_tags = parsed_args.query_parameters.split(',')
    latest_release_date = parsed_args.date

    return repo_name, query_tags, latest_release_date

def get_raw_output(repo_name, query_tags, latest_release_date):

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

def changelog_per_label(json_dict):
    changelog_labels = ["bug", "enhancement", "feature"]
    labels = []
    for item in json_dict:
        labels.append(item["labels"])
        if any(item in changelog_labels for item in labels):
            pass

def prepare_changelog_markdown():
    repo_name, query_tags, latest_release_date = get_inputs()
    pr_query = get_raw_output(repo_name=repo_name, query_tags=query_tags, latest_release_date=latest_release_date)
   
    minor_bump_label_list = get_repo_label(repo=repo_name, label_name="MINOR_BUMP_LABEL")
    patch_bump_label_list = get_repo_label(repo=repo_name, label_name="PATCH_BUMP_LABEL")
    
    # ? should version bump labels also be filter for changelog ?
    label_list = minor_bump_label_list + patch_bump_label_list
    changelog = ""

    for pr in pr_query:
        # get all label names in a list
        pr_label_list = [label["name"] for label in pr["labels"]]
        fitlered_label = list(set(label_list).intersection(pr_label_list))[0]

        if fitlered_label:
            change_list = get_changelog(pr_data=pr["body"], changelog_start="## Changes")
            
            changelog += f"## {fitlered_label.capitalize()}\n"
            changelog += "".join([f"* {change}\n" for change in change_list])
            changelog += "\n"

    return changelog


def get_labels():
    github_data = get_raw_output(*get_inputs())
    labels = set()

    for item in github_data:
        for label in item["labels"]:
            labels.add(label["name"])

    return json.dumps(list(labels))

def get_repo_label(repo, label_name):
   
    label= subprocess.run(
        ["gh", "variable", "get", label_name, "--repo", repo],
        capture_output=True,
        text=True,
        check=True
    )

    return label.stdout.strip().split(", " or ",")

def get_version_increment():

    repo_name, _, _ = get_inputs()

    minor_bump_label_list = get_repo_label(repo=repo_name, label_name="MINOR_BUMP_LABEL")
    patch_bump_label_list = get_repo_label(repo=repo_name, label_name="PATCH_BUMP_LABEL")

    for label in json.loads(get_labels()):
        if label.lower() in minor_bump_label_list:
            return "minor"
        if label.lower() in patch_bump_label_list:
            return "patch"

if __name__ == "__main__":
    parse_arguments()