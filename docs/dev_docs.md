# Developer Documentation

## Code Structure

```code
📦github-query
 ┣ 📂.github
 ┃ ┗ 📂workflows
 ┃   ┗ 📜action-ci.yml
 ┣ 📂docs
 ┃ ┗ 📜dev_docs.md
 ┣ 📂src
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜conversion_logic.py
 ┃ ┗ 📜queries.py
 ┣ 📂tests
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜changelog.md
 ┃ ┣ 📜formatted_changelog.md
 ┃ ┣ 📜formatted_changelog_icons.md
 ┃ ┣ 📜merged_pr_query.json
 ┃ ┣ 📜merged_pr_query_testing.json
 ┃ ┣ 📜pr_api_output.json
 ┃ ┣ 📜pr_api_output_no_labels.json
 ┃ ┣ 📜pr_api_output_some_labels.json
 ┃ ┣ 📜test_github_query copy.py
 ┃ ┗ 📜test_github_query.py
 ┣ 📜.gitignore
 ┣ 📜README.md
 ┣ 📜action.yml
 ┗ 📜github_query.py
```

* `.github/workflows`: Github Action workflow running pytest suite and the action itself
* `docs`: THis documentation
* `src`: The query and conversion logic used by this action
* `tests`: Pytest-Suite for automated testing, including sample files
* `README.md`: User documentation to use the action.
* `action.yml`: Action entry point to call from other workflows
* `github_query`: Main execution file calling the python logic - based on click commands

## Intention

The `github_query.py` file contains the function responsible for querying and converting the data received from the github api.

* pr_labels()
* version_increment()
* generate_release_changelog

Using the clock package these function are called by the action .yml file like this:
`python github_query.py version-increment "param1" "param2" "param3" "param4"`

Afterwards the output gets piped to the actions output using `>> $GITHUB_OUTPUT`
