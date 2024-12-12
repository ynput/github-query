# Github-Query

[![CI-Status](https://github.com/ynput/github-query/actions/workflows/action-ci.yml/badge.svg)](https://github.com/ynput/github-query/actions/workflows/action-ci.yml)

**This is a customized query action for Ayon-related repo-workflows.**

## Purpose

This action mainly queries pull request related information.
It got a bunch of conversion going on to prepare the data for further usage. This includes

* Filtering PR labels
* Suggest version increment based on found labels
* Preparing data structure for release information
* Prepare a markdown formatted changelog based on PR information

## Usage

For details see [action.yml](https://github.com/ynput/github-query/blob/main/action.yml) file

```yaml
- name: Query PR data
  uses: ynput/github-query@main
  with:
    # Repository name with owner. For example, actions/checkout
    repo: ""
    # Date-Time-Stamp as a starting point for the query, will only process merged PRs newer then that date
    # format: "2024-08-20T12:03:23Z"
    date: ""
    # JSON keys to query for in a gh query command
    # gh pr list --state merged --search f'merged:>=<date>' --json "body,labels,title,id,number,url" --repo <repo_name>
    query_parameters: ""
    # Define change log content and order by this comma separated value string
    # example: "enhancement,bugfix,docs"
    changelog_labels: ""
```

## Outputs

* raw-output - Full output json dictionary from github api
* label-list - List of unique labels found in PRs
* bump-increment - Increment for version bumping - either 'patch', 'minor' or 'major'
* changelog-markdown - String containing markdown formatted release changelog

## Testing

Unit-test are included in `tests/` and will run on every pr targeting main and very push to main.
These tests can be run local by changing into the `tests/` directory and running `pytest`

## Developer-Docs

The python file `github_query.py` calls all the main logic and provides it's function to `action.yml` through click-parameters.
This makes the python function calls convenient to use from terminal while keeping them easy to test. For more detailed documentation check the [docs directory](https://github.com/ynput/github-query/tree/main/docs).
