from typing import Any, Literal, List
import json
import pytest

from src import conversion_logic

@pytest.fixture
def pr_api_output() -> List[dict[str, Any]]:
    return [
        {
            "body": "# Bug Fix PR Template\r\n\r\n[ x] Feature/Enhancement<br>\r\n[ ] Bugfix<br>\r\n[ ] Documentation update<br>\r\n\r\n## Summary\r\n\r\n<!--Provide a concise description of your changes and implementation.-->\r\n\r\n## Root Cause Analysis\r\n\r\n[Issue Link](https://github.com/ynput/ci-testing/blob/develop/.github/ISSUE_TEMPLATE/bug_report.yml)<br>\r\n<!--Detail the reason for your change and which benefits result from it.-->\r\n\r\n## Changes\r\n\r\n<!--Outline the changes made in a list.-->\r\n* Add more test\r\n* Was very important\r\n* Needed to add this here\r\n\r\n## Testing Strategy\r\n\r\n<!--Explain how the fix has been tested to ensure the bug is resolved without introducing new issues.-->\r\n\r\n## Checklist\r\n\r\n* [ x] The fix has been locally tested\r\n* [ x] New unit tests have been added to prevent future regressions\r\n* [ x] The documentation has been updated if necessary\r\n\r\n## Additional Notes\r\n\r\n<!--Any further information needed to understand the fix or its impact.-->",
            "labels": [
            {
                "id": "LA_kwDOMje8_88AAAABtOJ1Ig",
                "name": "enhancement",
                "description": "New feature or request",
                "color": "b9f29d"
            }
            ],
            "title": "Add more data"
        },
        {
            "body": "# Date file added\r\n\r\n## Summary\r\n\r\nSome awesome summary going on right here.\r\n\r\n## Root Cause Analysis\r\n\r\n[Issue Link](https://github.com/ynput/ci-testing/blob/develop/.github/ISSUE_TEMPLATE/bug_report.yml)<br>\r\nDate file so absolutely needed.\r\n\r\n## Changes\r\n\r\n<!--Outline the changes made in a list.-->\r\n* Run a command\r\n* Pipe its output to a text file\r\n* Commit dem stuff\r\n\r\n## Testing Strategy\r\n\r\nnahhhhh\r\n\r\n## Checklist\r\n\r\n* [x] The fix has been locally tested\r\n* [x] New unit tests have been added to prevent future regressions\r\n* [x] The documentation has been updated if necessary\r\n\r\n## Additional Notes\r\n\r\nNop",
            "labels": [
            {
                "id": "LA_kwDOMje8_88AAAABtOJ1Gw",
                "name": "bugfix",
                "description": "Something got fixed",
                "color": "ff9195"
            }
            ],
            "title": "Add date file"
        }
        ]

@pytest.fixture
def pr_api_output_missing_label():
    return [
        {
            "body": "# Bug Fix PR Template\r\n\r\n[ x] Feature/Enhancement<br>\r\n[ ] Bugfix<br>\r\n[ ] Documentation update<br>\r\n\r\n## Summary\r\n\r\n<!--Provide a concise description of your changes and implementation.-->\r\n\r\n## Root Cause Analysis\r\n\r\n[Issue Link](https://github.com/ynput/ci-testing/blob/develop/.github/ISSUE_TEMPLATE/bug_report.yml)<br>\r\n<!--Detail the reason for your change and which benefits result from it.-->\r\n\r\n## Changes\r\n\r\n<!--Outline the changes made in a list.-->\r\n* Add more test\r\n* Was very important\r\n* Needed to add this here\r\n\r\n## Testing Strategy\r\n\r\n<!--Explain how the fix has been tested to ensure the bug is resolved without introducing new issues.-->\r\n\r\n## Checklist\r\n\r\n* [ x] The fix has been locally tested\r\n* [ x] New unit tests have been added to prevent future regressions\r\n* [ x] The documentation has been updated if necessary\r\n\r\n## Additional Notes\r\n\r\n<!--Any further information needed to understand the fix or its impact.-->",
            "title": "Add more data"
        },
        {
            "body": "# Date file added\r\n\r\n## Summary\r\n\r\nSome awesome summary going on right here.\r\n\r\n## Root Cause Analysis\r\n\r\n[Issue Link](https://github.com/ynput/ci-testing/blob/develop/.github/ISSUE_TEMPLATE/bug_report.yml)<br>\r\nDate file so absolutely needed.\r\n\r\n## Changes\r\n\r\n<!--Outline the changes made in a list.-->\r\n* Run a command\r\n* Pipe its output to a text file\r\n* Commit dem stuff\r\n\r\n## Testing Strategy\r\n\r\nnahhhhh\r\n\r\n## Checklist\r\n\r\n* [x] The fix has been locally tested\r\n* [x] New unit tests have been added to prevent future regressions\r\n* [x] The documentation has been updated if necessary\r\n\r\n## Additional Notes\r\n\r\nNop",
            "labels": [
            {
                "id": "LA_kwDOMje8_88AAAABtOJ1Gw",
                "name": "bug",
                "description": "Something isn't working",
                "color": "ff9195"
            }
            ],
            "title": "Add date file"
        }
        ]

@pytest.fixture
def major_bump() -> List[str]:
    return ["epic"]

@pytest.fixture
def major_bump_no_list() -> Literal['epic']:
    return "epic"

@pytest.fixture
def merged_pr_samples():
    with open("merged_pr_query.json") as file:
        return json.load(file)
    
@pytest.fixture
def changelog_markdown() -> str:
    with open("formatted_changelog.md") as file:
        return file.read()

@pytest.fixture
def minor_bump() -> list[str]:
    return ["feature", "enhancement"]

@pytest.fixture
def patch_bump() -> list[str]:
    return ["bugfix"]

@pytest.fixture
def pr_labels_bug() -> list[str]:
    return ["bugfix"]

@pytest.fixture
def pr_labels_enhancement() -> list[str]:
    return ["bugfix", "documentation", "feature", "enhancement"]

@pytest.fixture
def pr_labels_epic() -> List[str]:
    return ["bugfix", "documentation", "feature", "enhancement", "epic"]

@pytest.fixture
def pr_labels_wrong_labels() -> list[str]:
    return ["documentation", "wontfix"]

@pytest.fixture
def pr_labels_empty_list() -> list[Any]:
    return []

@pytest.fixture
def pr_labels_none() -> None:
    return None

@pytest.fixture
def csv_string_spaces() -> Literal['bugfix, enhancement, feature']:
    return "bugfix, enhancement, feature"

@pytest.fixture
def csv_string_no_spaces() -> Literal['bugfix,enhancement,feature']:
    return "bugfix,enhancement,feature"

@pytest.fixture
def csv_string_no_comma() -> Literal['bugfix']:
    return "bugfix"

@pytest.fixture
def csv_string_empty() -> Literal['']:
    return ""

@pytest.fixture
def changelog_label_list() -> list[str]:
    return ["type: enhancement", "type: bug", "type: maintenance"]

@pytest.fixture
def changelog_exclude_label_list() -> List[str]:
    return ["sponsored"]


# Get PR Label test-cases

def test_get_labels(pr_api_output: List[dict[str, Any]]) -> None:
    labels: List[str] = conversion_logic.filter_unique_labels(pr_data=pr_api_output)

    assert isinstance(labels, list)
    assert set(labels) == {"bugfix", "enhancement"}

def test_get_labels_missing_input(pr_api_output_missing_label) -> None:
    labels = conversion_logic.filter_unique_labels(pr_data=pr_api_output_missing_label)

    assert labels == []


# Convert repo label list

def test_csv_string_to_list_spaces(csv_string_spaces: Literal['bugfix, enhancement, feature']) -> None:
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_spaces)
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_spaces)

    assert string_list == ["bugfix", "enhancement", "feature"]

def test_csv_string_to_list_no_spaces(csv_string_no_spaces: Literal['bugfix,enhancement,feature']) -> None:
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_no_spaces)
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_no_spaces)

    assert string_list == ["bugfix", "enhancement", "feature"]

def test_csv_string_to_list_no_comma(csv_string_no_comma: Literal['bugfix']) -> None:
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_no_comma)
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_no_comma)

    assert string_list == ["bugfix"]

def test_csv_string_to_list_empty(csv_string_empty: Literal['']) -> None:
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_empty)
    string_list: List[str] = conversion_logic.csv_string_to_list(csv_string_empty)

    assert string_list == []


# Version Increment test-cases

def test_get_version_increment_patch(minor_bump: List[str], patch_bump: List[str], pr_labels_bug: List[str]) -> None:
    increment = conversion_logic.get_version_increment(
        pr_label_list=pr_labels_bug,
        patch_bump_list=patch_bump,
        minor_bump_list=minor_bump,
        )

    assert increment == "patch"

def test_get_version_increment_minor(minor_bump: List[str], patch_bump: List[str], pr_labels_enhancement: List[str]) -> None:
    increment = conversion_logic.get_version_increment(
        pr_label_list=pr_labels_enhancement,
        patch_bump_list=patch_bump,
        minor_bump_list=minor_bump,
        )

    assert increment == "minor"

def test_get_version_increment_minor(minor_bump: List[str], patch_bump: List[str], major_bump: List[str], pr_labels_epic: List[str]) -> None:
    increment = conversion_logic.get_version_increment(
        pr_label_list=pr_labels_epic,
        patch_bump_list=patch_bump,
        minor_bump_list=minor_bump,
        major_bump_list=major_bump,
        )

    assert increment == "major"

def test_get_version_increment_wrong_labels(minor_bump: List[str], patch_bump: List[str], pr_labels_wrong_labels: List[str]):
    increment = conversion_logic.get_version_increment(
        pr_label_list=pr_labels_wrong_labels,
        patch_bump_list=patch_bump,
        minor_bump_list=minor_bump,
        )

    assert increment == ""

def test_get_version_increment_none(minor_bump: List[str], patch_bump: List[str], pr_labels_none: None) -> None:
    increment = conversion_logic.get_version_increment(
        pr_label_list=pr_labels_none,
        patch_bump_list=patch_bump,
        minor_bump_list=minor_bump,
        )

    assert increment == ""

def test_get_version_increment_empty_list(minor_bump: List[str], patch_bump: List[str], pr_labels_empty_list: List[Any]) -> None:
    increment = conversion_logic.get_version_increment(
        pr_label_list=pr_labels_empty_list,
        patch_bump_list=patch_bump,
        minor_bump_list=minor_bump,
        )

    assert increment == ""

def test_get_version_increment_no_list(minor_bump: List[str], patch_bump: List[str], major_bump_no_list: Literal['epic'], pr_labels_epic: List[str]) -> None:
     with pytest.raises(ValueError, match="must be a list"):
        conversion_logic.get_version_increment(
            pr_label_list=pr_labels_epic,
            patch_bump_list=patch_bump,
            minor_bump_list=minor_bump,
            major_bump_list=major_bump_no_list,
            )


# Changelog test-cases

def test_filter_changes_per_label_types(merged_pr_samples: List[dict[str, str]], changelog_label_list: List[str]) -> None:    
    filtered_pr_list: List[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=merged_pr_samples, changelog_label_list=changelog_label_list)

    assert all(isinstance(changelog, conversion_logic.Changelog) for changelog in filtered_pr_list)


def test_format_changelog_markdown(merged_pr_samples: List[dict[str, str]], changelog_label_list: List[str], changelog_markdown: str) -> None:
    filtered_pr_list: List[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=merged_pr_samples, changelog_label_list=changelog_label_list)
    changelog_result: str = conversion_logic.format_changelog_markdown(changes=filtered_pr_list, changelog_label_list=changelog_label_list)

    # print(changelog_result)

    assert changelog_result == changelog_markdown

def test_format_changelog_markdown_no_data(changelog_label_list: List[str]) -> None:
    filtered_pr_list: List[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=[], changelog_label_list=changelog_label_list)
    changelog_result: str = conversion_logic.format_changelog_markdown(changes=filtered_pr_list, changelog_label_list=changelog_label_list)

    assert changelog_result == "# Changelog\n"
