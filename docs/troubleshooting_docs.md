# Troubleshooting

## Approach

Any faulty, missing or wrong data resulting from running this action can be troubleshooted locally using output visible within the workflow which showed the issues.

## Get the trouble data

The action.yml file in this repository contains the essential commands which are run from the terminal.

`label_list=$(python github_query.py pr-labels "${{ inputs.repo }}" "${{ inputs.base_branch }}" "${{ inputs.query_parameters }}" "${{ inputs.date }}")`

All the variables marked with `${{ X }}` are GitHub workflow variables and will be replaced with their according values at runtime.

`label_list=$(python github_query.py pr-labels "ynput/ayon-houdini" "develop" "body,labels,title,id,number,url" "2024-11-25T12:30:57Z")`

This can be used for local troubleshooting

## Troubleshoot locally

First you will need to clone down this repo and change into the repositories root directory in your terminal.
Next you need to make sure you have the [gh tool](https://cli.github.com/) available in your terminal.
Now you gonna need a PersonalAccessToken with appropriate permissions to have your [gh client authenticate](https://cli.github.com/manual/gh_auth_login) with github.

When you got that all running you should be able to just run something like this right in your terminal.
`python github_query.py pr-labels "ynput/ayon-houdini" "develop" "body,labels,title,id,number,url" "2024-11-25T12:30:57Z"`

It should show you a similar output to what the initial troubled workflow got. be aware tho - the output will have changed due the workflow being dependent on the current state of the repository.

At the time of writing (12.12.2024) I currently get this output from running this command:
`['sponsored', 'community', 'type: enhancement']`

## Debugging

When running this locally you can simply add additional debug output or code changes.
Since this only queries data and doesn't change anything you're free to test and use this state for bugfixes and development outside of any workflow right from your terminal.
