from typing import Any, Literal, List
import json
import pytest

from src import conversion_logic

@pytest.fixture
def pr_api_output() -> List[dict[str, Any]]:
    with open("pr_api_output.json") as file:
        return json.load(file)

@pytest.fixture
def pr_api_output_missing_label() -> List[dict[str, Any]]:
    with open("pr_api_output_missing_label.json") as file:
        return json.load(file)

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
def changelog_markdown_icons() -> str:
    with open("formatted_changelog_icons.md") as file:
        return file.read()
    
@pytest.fixture
def changelog_body() -> str:
    with open("changelog.md") as file:
        return file.read()

@pytest.fixture
def changelog_description() -> List[str]:
    return ['Some more information', '', '- Prototype loading of USD references into a Maya USD proxy while keeping it managed by the pipeline', '- Prototype loading of Maya references into a Maya USD proxy while keeping it managed by the pipeline']

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
def empty_string() -> str:
    return ""

@pytest.fixture
def changelog_label_list() -> list[str]:
    return ["type: enhancement", "type: bugfix", "type: maintenance"]

@pytest.fixture
def label_with_emote() -> str:
    return "type: bugfix(🐛)"

@pytest.fixture
def label_type_prefix() -> str:
    return "type: bugfix"

@pytest.fixture
def changelog_label_list_icons() -> list[str]:
    return ["feature(🎉)", "type: enhancement(💚)", "type: bugfix(🐛)", "type: maintenance"]

@pytest.fixture
def changelog_exclude_label_list() -> List[str]:
    return ["sponsored"]


# Get PR Label test-cases

def test_get_labels(pr_api_output: List[dict[str, Any]]) -> None:
    labels: List[str] = conversion_logic.filter_unique_labels(pr_data=pr_api_output)

    assert isinstance(labels, list)
    assert set(labels) == {"bugfix", "enhancement"}

def test_get_labels_missing_input(pr_api_output_missing_label: List[dict[str, Any]]) -> None:
    labels: List[str] = conversion_logic.filter_unique_labels(pr_data=pr_api_output_missing_label)

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

def test_csv_string_to_list_empty(empty_string: Literal['']) -> None:
    string_list: List[str] = conversion_logic.csv_string_to_list(empty_string)
    string_list: List[str] = conversion_logic.csv_string_to_list(empty_string)

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

def test_get_version_increment_major(minor_bump: List[str], patch_bump: List[str], major_bump: List[str], pr_labels_epic: List[str]) -> None:
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

def test_get_changelog_description(changelog_body: str, changelog_description: str) -> None:
    filtered_changelog: List[str] = conversion_logic.get_changelog_description(changelog_body)

    assert filtered_changelog == changelog_description

def test_format_changelog_markdown(merged_pr_samples: List[dict[str, str]], changelog_label_list: List[str], changelog_markdown: str) -> None:
    filtered_pr_list: List[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=merged_pr_samples, changelog_label_list=changelog_label_list)
    changelog_result: str = conversion_logic.format_changelog_markdown(changes=filtered_pr_list, changelog_label_list=changelog_label_list)

    assert changelog_result == changelog_markdown

def test_format_changelog_markdown_no_data(changelog_label_list: List[str]) -> None:
    filtered_pr_list: List[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=[], changelog_label_list=changelog_label_list)
    changelog_result: str = conversion_logic.format_changelog_markdown(changes=filtered_pr_list, changelog_label_list=changelog_label_list)

    assert changelog_result == "# Changelog\n"

def test_filter_emote(label_with_emote: str) -> None:
    filter_result: str = conversion_logic.filter_emote(text=label_with_emote)

    assert filter_result == "type: bugfix"

def test_filter_emote_no_emote(label_type_prefix: str) -> None:
    filter_result: str = conversion_logic.filter_emote(text=label_type_prefix)

    assert filter_result == "type: bugfix"

def test_filter_emote_empty(empty_string: str) -> None:
    filter_result: str = conversion_logic.filter_emote(text=empty_string)

    assert filter_result == ""

def test_format_label_emote(label_with_emote: str) -> None:
    formatted_label: str = conversion_logic.format_label(text=label_with_emote)

    assert formatted_label == "🐛 **Bugfix**"

def test_format_label_empty(empty_string: str) -> None:
    formatted_label: str = conversion_logic.format_label(text=empty_string)

    assert formatted_label == ""

def test_format_label(label_type_prefix: str) -> None:
    formatted_label: str = conversion_logic.format_label(text=label_type_prefix)

    assert formatted_label == "**Bugfix**"

def test_get_changelog_description_no_descprition():
    pr_body = "## Changelog\r\n<!-- Paragraphs contain detailed information on the changes made to the product or service, providing an in-depth description of the updates and enhancements. They can be used to explain the reasoning behind the changes, or to highlight the importance of the new features. Paragraphs can often include links to further information or support documentation. -->\r\n\r\nOn Maya scene exports only include the relevant history for the selected nodes downstream and upstream and not upstream, and also their downstream descendant children.\r\n\r\n## Additional info\r\n<!-- Paragraphs of text giving context of additional technical information or code examples. -->\r\n\r\nNote: This may affect maya scene exports, camera rig exports and layout exports. However, I do feel this is a way more sensible default behavior on exports _with_ construction history enabled.\r\n\r\nWith this change, if you have a hierarchy like:\r\n```\r\ngrp/\r\n    obj1\r\n    obj2\r\n```\r\nAnd `obj1` is inside the instance then after this PR `obj2` is not included.\r\nBefore this PR all other descendents from upstream groups would be included, regardless of whether they were \"inputs\" to the `obj1`.\r\n\r\nAfter this PR, if `obj2` is an input connection to `obj1` (e.g. there are active constraints driving `obj1` or some other connections driving it) then `obj2` **will still be included.**\r\n\r\nAs such, only objects actively contributing to members of the instance will still be included in the output.\r\n\r\n## Testing notes:\r\n\r\n1. Recreate the aforementioned hierarchy from additional info.\r\n2. Publish `obj1` - it should not include `obj2`\r\n3. Now make a connection from `obj2` to `obj1` (e.g. translate connection)\r\n4. Now `obj2` should also be included in `obj2`.\r\n5. Now disconnect the connection, and key `obj1`  transforms.\r\n6. The keys should be exported along just fine."
    changelog_desc_result: List[str] = conversion_logic.get_changelog_description(pr_body)

    assert changelog_desc_result == []

def test_format_changelog_markdown_icons(merged_pr_samples: List[dict[str, str]], changelog_label_list_icons: List[str], changelog_markdown_icons: str) -> None:
    filtered_pr_list: List[conversion_logic.Changelog] = conversion_logic.filter_changes_per_label(pr_data=merged_pr_samples, changelog_label_list=changelog_label_list_icons)
    changelog_result: str = conversion_logic.format_changelog_markdown(changes=filtered_pr_list, changelog_label_list=changelog_label_list_icons)

    assert changelog_result == changelog_markdown_icons
