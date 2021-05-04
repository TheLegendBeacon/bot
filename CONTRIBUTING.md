## Pre-requisites:
 - [Python 3.8+](https://www.python.org/downloads/)
 - [Poetry](https://python-poetry.org/docs/)
 - Some experience with [Git](https://git-scm.com/downloads)
 - [A GitHub Account](https://github.com/join)
 - Some knowledge of [discord.py](https://discordpy.readthedocs.io/en/stable/)

## Installation Steps:
1. Head over to https://github.com/cat-dev-group/bot
2. Click on the fork option in the top right corner. This will create your copy of the repository, to which you will make your changes.
3. Create a folder where you wish to store a local copy of the project. Open your terminal/command prompt and `cd` to this directory.
4. Enter the following command to get a local copy of the repo:
`git clone https://www.github.com/YourGithubUsername/bot`.
`cd bot` to this repo.

## Contributing:
1. Run `poetry shell` to initialize the virtual environment and `poetry install` to update dependencies.
2. Create a new branch for whatever you're working on with `git checkout -b branch-name`, where `branch-name` describes what the end-goal is in 2-3 words.
3. Make your changes. You'll usually be adding new cogs in the `bot/exts` directory.
4. Run `git add .` to stage your changes.
5. Run `git commit -m "commit message"` to commit your changes. Keep the commit title short and descriptive.
6. Run `git push -u origin branch-name` to push your changes to the remote repo (on your GitHub).
7. When you're done, create a pull-request on the repo. Your code will be reviewed and when ready, it will be merged. 

## Additional Notes:
1. If you're adding dependencies, use `poetry add package-name` instead of the usual `pip install package-name`.
2. Follow PEP8. Format your code with [black](https://pypi.org/project/black/) before you commit.
3. Run `poetry lock` before you commit.

## Testing:
1. You would need your own discord bot for testing. Create one from the [Discord Developer Portal](https://discord.com/developers/applications) if you haven't already.
2. Create a test server on discord,  and add your bot there.
3. Add your bot token and prefix in the `.env` file.
4. Run the bot with `poetry run python -m bot`.
