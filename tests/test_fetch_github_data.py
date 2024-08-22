
import argparse
import json
from unittest import mock
import os
import sys

from unittest.mock import patch

# Add the parent directory of 'tests' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import fetch_github_data

# Mock data to return for your tests
mock_repo_name = 'ynput/ayon-addon-action-testing'
mock_query_parameters = 'title,body,labels'
mock_date = '2024-07-08T09:48:33Z'
mock_labels_output = ['bug', 'enhancement']

# Mocking the subprocess to prevent actual GitHub CLI calls
def mock_get_raw_output(repo_name, query_tags, latest_release_date):
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
                "name": "bug",
                "description": "Something isn't working",
                "color": "ff9195"
            }
            ],
            "title": "Add date file"
        }
        ]

@patch('argparse.ArgumentParser.parse_args')
@patch('fetch_github_data.get_raw_output', side_effect=mock_get_raw_output)
def test_get_labels(mock_parse_args, mock_get_raw_output):
    # Configure the mock to return desired arguments
    mock_parse_args.return_value = argparse.Namespace(
        repo=mock_repo_name,
        query_parameters=mock_query_parameters,
        date=mock_date
    )

    fetch_github_data.parse_arguments()
    
    labels = fetch_github_data.get_labels()

    assert set(json.loads(labels)) == set(mock_labels_output)

