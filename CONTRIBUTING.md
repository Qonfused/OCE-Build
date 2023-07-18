# Contributing Guide

Welcome! Thank you for your interest in contributing to this project. There are many ways to contribute, including submitting bug reports, improving documentation, submitting feature requests, reviewing new submissions, or contributing code that can be incorporated into the project.

This document describes this project's development process. Following these guidelines shows that you respect the time and effort of those managing this project. In return, you will be shown respect in addressing your issue, reviewing your changes, and incorporating your contributions.

> **Note** Please, don't use the issue tracker for support questions. Instead use: [Github Discussions](https://github.com/Qonfused/OCE-Build/discussions).

**Table of Contents:**

1. [Important Resources](#important-resources)
2. [Finding an Issue](#finding-an-issue)
3. [Reporting Bugs](#reporting-bugs)
4. [Feature Requests](#feature-requests)
5. [Improving Documentation](#improving-documentation)
6. [Development Process](#development-process)
7. [Contributing Code](#contributing-code)
    1. [General Guidelines and Philosophy](#general-guidelines-and-philosophy)
    2. [Getting Started](#getting-started)
    3. [Setting up your development environment](#setting-up-your-development-environment)
    4. [Project Structure](#project-structure)
    5. [Project Scripts](#project-scripts)
    6. [Coding Style](#coding-style)
    7. [Building the Project](#building-the-project)
    8. [Testing](#testing)
    9. [License](#license)
8. [Pull Request Process](#pull-request-process)
    1. [Review Process](#review-process)
    2. [Addressing Feedback](#addressing-feedback)

## Important Resources

> TODO

## Finding an Issue

The list of outstanding feature requests and bugs can be found on our on our [GitHub issue tracker](https://github.com/Qonfused/OCE-Build/issues). Pick an unassigned issue that you think you can accomplish and add a comment that you are attempting to do it.

Regarding issue labels:

* `good first issue` labeled issues are deemed to be good low-hanging fruit for newcomers to the project.
* `help-wanted` labeled issues may be more difficult and may include new feature development.
* `type:documentation` labeled issues must only touch content in the `docs` folder.

## Reporting Bugs

> **Note** If you find a security vulnerability, do NOT open an issue. Please refer to our [Security Policy](https://github.com/Qonfused/OCE-Build/security/policy) for reporting security vulnerabilities.

Before you submit your issue, please [search the issue archive](https://github.com/Qonfused/OCE-Build/issues) - maybe your question or issue has already been identified or addressed.

If you find a bug in the source code, you can help us by [submitting an issue to our GitHub issue tracker](https://github.com/Qonfused/OCE-Build/issues/new/choose). This project provides a bug issue template to help you kickstart your issue.

Even better, you can submit a new Pull Request with a fix.

## Feature Requests

Please create a new GitHub issue for any major changes and enhancements that you wish to make. Please provide the feature you would like to see, why you need it, and how it will work. Discuss your ideas transparently and get community feedback before proceeding.

Major Changes that you wish to contribute to the project should be discussed first in an GitHub issue that clearly outlines the changes and benefits of the feature.

Small Changes can directly be crafted and submitted to the GitHub Repository as a Pull Request. See the section about Pull Request Submission Guidelines, and for detailed information the core development documentation.

## Improving Documentation

Should you have a suggestion for the documentation, you can open an issue and outline the problem or improvement you have - however, creating the doc fix yourself is much better!

If you want to help improve the docs, it's a good idea to let others know what you're working on to minimize duplication of effort. Create a new issue (or comment on a related existing one) to let others know what you're working on. If you're making a small change (typo, phrasing) don't worry about filing an issue first.

For large fixes, please build and test the documentation before submitting the PR to be sure you haven't accidentally introduced any layout or formatting issues.

> TODO: Instructions on building and viewing documentation

## Development Process

This project follows the [git flow](http://nvie.com/posts/a-successful-git-branching-model/) branching model of development.

The `origin/main` branch should always reflect a *production-ready* state, while the `origin/development` branch is an *integration branch* reflecting the latest development changes.

A *topic branch* is a short-lived branch that you create and use for a single particular feature or related work. It is recommended that you create a new topic branch for every new feature you work on.

When you have finished working on a topic branch, you can merge your changes back into the `origin/development` branch. This is done by creating a pull request. Pull requests are the preferred way to contribute code-changes to this project.

## Contributing Code

### General Guidelines and Philosophy

* Include unit tests when you contribute new features or fix a bug, this:
  * proves that your code works correctly
  * guards against breaking changes
  * lowers the maintenance cost

* Keep compatibility and cohesiveness mind when contributing a change that
  will impact the public API.

* Create issues for any major changes and enhancements that you wish to make.

* Create a pull request for your changes and coordinate with the project
  maintainers to get it merged to main.

### Getting Started

To begin contributing, you will need to fork the main repository to work on your changes. Simply navigate to our GitHub page and click the "Fork" button at the top. Once you've forked the repository, you can clone your new repository and start making edits.

In git, it is best to isolate each topic or feature into a “topic branch”. While individual commits allow you control over how small individual changes are made to the code, branches are a great way to group a set of commits all related to one feature together, or to isolate different efforts when you might be working on multiple topics at the same time.

While it takes some experience to get the right feel about how to break up commits, a topic branch should be limited in scope to a single issue.

To create a new branch and start working on it, run the following commands:

```sh
# Checkout the main branch - you want your new branch to come from main
git checkout main

# Create a new branch named newfeature (give your branch its own simple informative name)
git branch newfeature

# Switch to your new branch
git checkout newfeature
```

For more information on the GitHub fork and pull-request processes, [please see this helpful guide](https://gist.github.com/Chaser324/ce0505fbed06b947d962).

### Setting up your development environment

Development of this project requires the following tools:

* [Python](https://www.python.org/downloads/) (version 3.8 or higher)
* [Poetry](https://python-poetry.org/docs/#installation)

#### Poetry

Poetry is a Python package manager that provides a virtual environment for managing dependencies and project configuration. Poetry is required to be installed on your system to develop and build this project.

It's recommended to use at least version `1.5.0` of Poetry to ensure compatibility with this project.

To install Poetry, you can either use the [official installation instructions](https://python-poetry.org/docs/#installation) or use the provided script to install Poetry in your home directory:

```sh
bash scripts/install-poetry.sh
```

To upgrade Poetry from a previous version, you can run `poetry self update` to fetch the latest version, or run `poetry self update 1.5.0` to update to the project's recommended version.

To setup the poetry environment and install project dependencies, run the below command:

```sh
bash scripts/setup-poetry.sh
```

### Project Structure

> TODO

### Project Scripts

This project uses a custom set of scripts to help manage the development and build process. These scripts are located in the **ci/scripts** directory. These scripts are intended to be run through the [**poethepoet**](https://github.com/nat-n/poethepoet) plugin, which is installed as part of the `setup-poetry.sh` script.

To list all available scripts, run `poetry run poe`. Run a script using `poetry <script>` or `poetry run poe <script>`.

Note that scripts listed in the **ci/scripts** directory must be prefixed with `poetry run poe <command>`, while scripts listed in the [**pyproject.toml**](/pyproject.toml) file can also be run through `poetry <command>`.

For example, to run the **test** script, simply run `poetry test` or `poetry run poe test`. Only the latter option is available for CI scripts to avoid namespace pollution of Poetry commands.

It's recommended to run the **resolve-modules** and **sort-imports** CI scripts before commiting; these scripts will ensure that all module namespaces can properly be resolved and that all imports are sorted correctly. These scripts will run automatically on the pre-commit git hook, but can be run manually by running `poetry run poe resolve-modules` and `poetry run poe sort-imports`.

### Coding Style

When contributing code to this project, it is important to keep the code style consistent with the rest of the project. This makes it easier for other developers to read the code and understand it. Should the need arise, the project maintainers may ask you to make changes to your code to keep it consistent with the project's style.

For Python code, it's recommended to adhere to the
  [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html).

#### Lint your changes

Code linting is a type of static analysis that is frequently used to find problematic patterns or code that doesn't adhere to certain style guidelines. By running a linting tool on your code, you can ensure that your code follows the project's style guidelines and that it adheres to the project's quality standards.

For Python code, it's recommended to use [pylint](https://www.pylint.org/) to lint your code. Below are some examples of how to lint your code using pylint:

* Lint unstaged changes to Python files.

  ```shell
  git diff --name-only | sed '/.*\.py/!d' | xargs pylint
  ```

### Building the Project

> TODO

### Testing

> TODO

### License

When contributing code to this project, you must agree to license your contribution under the same license that covers the project. In this case, the project is licensed under the [BSD 3-Clause License](/LICENSE). This license is a permissive open source license that allows for free use of the code for both commercial and non-commercial purposes.

When adding a new file to the project, you must include the license header at the top of the file. This can be done by copying the license header from an existing file in the project and updating the year and author information. Below are some examples of license headers for different programming languages:

* [Python license example](https://github.com/Qonfused/OCE-Build/blob/python-rewrite/ocebuild/__init__.py#L1-L4)

## Pull Request Process

This project doesn't enforce any labeling conventions for pull requests, but it's desired to use a short and concise title that addresses the big picture of your changes.

When you are ready to generate a pull request, either for preliminary review, or for consideration of merging into the project you must first push your local topic branch back up to GitHub:

```sh
git push origin newfeature
```

Once you've committed and pushed all of your changes to GitHub, go to the page for your fork on GitHub, select your development branch, and click the pull request button. If you need to make any adjustments to your pull request, just push the updates to your branch. Your pull request will automatically track the changes on your development branch and update.

1. Ensure any install or build dependencies are removed before the end of the layer when doing a
   build.
2. Update the README.md with details of changes to the interface, this includes new environment
   variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you
   do not have permission to do that, you may request the second reviewer to merge it for you.

### Review Process

Except for critical, urgent or very small fixes, we try to leave pull requests open for most of the day or overnight if something comes in late in the day, so that multiple people have the chance to review/comment.  Anyone who reviews a pull request should leave a note to let others know that someone has looked at it.

For larger commits, we like to have a +1 from someone else and/or from other contributor(s) before proceeding.  Please note if you reviewed the code or tested locally -- a +1 by itself will typically be interpreted as thinking its a good idea, but not having reviewed in detail.

### Addressing Feedback

Once a PR has been submitted, your changes will be reviewed and constructive feedback may be provided. Feedback isn't meant as an attack, but to help make sure the highest-quality code makes it into our project. Changes will be approved once required feedback has been addressed.

If a maintainer asks you to "rebase" your PR, they're saying that a lot of code has changed, and that you need to update your fork so it's easier to merge.

To update your forked repository, follow these steps:

```sh
# Fetch upstream main and merge with your repo's main branch
git fetch upstream
git checkout main
git merge upstream/main

# If there were any new commits, rebase your development branch
git checkout newfeature
git rebase main
```

If too much code has changed for git to automatically apply your branches changes to the new main, you will need to manually resolve the merge conflicts yourself.

Once your new branch has no conflicts and works correctly, you can override your old branch using this command:

```sh
git push -f
```

Note that this will overwrite the old branch on the server, so make sure you are happy with your changes first!
