# Contributing to BiT-Forum

Thank you for considering contributing to BiT-Forum! Your contributions are essential for the improvement and success of this project. Please note that this project is currently open for contributions exclusively from students of the BiT (Bahir Dar Institute of Technology). This document outlines the process for contributing and the guidelines to follow.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
   - [Submitting an Issue](#submit-issue)
   - [Issues and Bugs](#reporting-bugs)
   - [Feature Requests](#suggesting-features)
3. [Getting Started](#getting-started)
4. [Making Changes](#making-changes)
   - [Commit Message Guidelines](#commit-message-guidelines)
   - [Submit Your Changes](#submitting-changes)
5. [Community](#community)

## <a name="code-of-conduct"></a> Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [our email](mailto:gdscbahirdar@gmail.com).

## <a name="how-to-contribute"></a> How to Contribute

### <a name="submit-issue"></a> Submitting an Issue

Before you submit an issue, please search the issue tracker, maybe an issue for your problem already exists and the discussion might inform you of workarounds readily available.

### <a name="reporting-bugs"></a> Found a Bug?

If you find a bug, please report it by [opening an issue](https://github.com/gdscbahirdar/forum-backend/issues/new). Include as much detail as possible to help us diagnose and fix the issue quickly. Details might include:

- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots or logs, if applicable

### <a name="suggesting-features"></a> Missing a Feature?

You can _request_ a new feature by [submitting an issue](https://github.com/gdscbahirdar/forum-backend/issues/new) to our GitHub
Repository. If you would like to _implement_ a new feature, please submit an issue with
a proposal for your work first, to be sure that we can use it.
Please consider what kind of change it is:

- For a **Major Feature**, first open an issue and outline your proposal so that it can be
  discussed. This will also allow us to better coordinate our efforts, prevent duplication of work,
  and help you to craft the change so that it is successfully accepted into the project. For your issue name, please prefix your proposal with `[discussion]`, for example "[discussion]: your feature idea".
- **Small Features** can be crafted and directly [submitted as a Pull Request](#submitting-changes).

## <a name="getting-started"></a> Getting Started

1. **Fork the Repository**

   - Start by forking the repository to your GitHub account.

2. **Clone the Forked Repository**

   - Clone the repository to your local machine to start making changes.

3. **Set Up Your Environment**
   - Make sure you have the necessary environment set up to start contributing. This might include software, libraries, or other tools specific to this project.

## <a name="making-changes"></a> Making Changes

1. **Create a New Branch**

   - For each new feature or fix, create a new branch from `master`. Use a name that reflects your changes, for example: `feat/add-login` or `fix/remove-bug`.

2. **Make Your Changes**

   - Implement your feature or fix. Make sure to keep your changes as focused as possible. If you find multiple, unrelated issues, consider making separate branches and pull requests for each.

3. **Follow the Code Style**

   - Run `pre-commit install` to create a git hook to fix your styles before you commit.

     Alternatively, manually check your code with:

     ```
     ruff check --fix
     ```

4. **Update Documentation**
   - If your changes require it, make sure to add docstrings, comments to your code.

### <a name="commit-message-guidelines"></a> Commit Message Guidelines

To maintain a clear and consistent history, please follow these commit message guidelines:

1. **Use the Imperative Mood**: Write your commit message as if you are giving a command or instruction. For example, "Fix bug causing crash on startup" rather than "Fixed bug" or "Fixes bug."

2. **Keep it Short and Descriptive**: Aim for a concise yet descriptive commit message. The first line should be a summary (50 characters or less), followed by a blank line and then a more detailed explanation if necessary.

3. **Use Prefixes for Clarity**: Start your commit message with a relevant prefix:

   - `feat:` for new features
   - `fix:` for bug fixes
   - `chore:` for updating tasks etc; no production code change
   - `docs:` for changes to documentation
   - `style:` for formatting, white-space, etc. (does not affect code logic)
   - `refactor:` for code changes that neither fixes a bug nor adds a feature

4. **Reference Issues and Pull Requests**: If your commit addresses specific issues or pull requests, include the reference (e.g., `#123`) at the end of the commit message.

### Submitting Your Changes

1. **Pull From `master`**

   - Before submitting your pull request, pull from the `master` branch to get the latest changes. Resolve any conflicts that arise.

2. **Commit Your Changes**

   - Write clear, concise commit messages that follow any project-specific guidelines.

3. **Push to Your Fork**

   - Push your changes to your fork on GitHub.

4. **Open a Pull Request**

   - Go to the original repository, and you'll see a prompt to open a pull request. Put as much information as possible about your changes.

5. **Code Review**

   - Once your pull request is opened, maintainers will review your changes. Be open to feedback and ready to make adjustments.

     After your pull request has been merged, you might want to pull the changes from the original repository to your fork to keep it up to date.

Thank you for contributing to our project! Your efforts make a significant difference.
