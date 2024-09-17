import json
import subprocess


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
