# Texas ICA

[![Build Status](https://travis-ci.org/texas-ica/texas-ica.com.svg?branch=master)](https://travis-ci.org/texas-ica/texas-ica.com)

Connect with fellow members, view upcoming events/announcements, and use other custom apps!

## Development

You need Python 3.5 or later to run the project locally. You can have multiple versions of Python (Python 2.x or Python 3.x) installed on your machine, but we use a virtual environment to keep project dependencies isolated from the global environment.

To begin, fork the repository to a folder on your machine. It's recommended to change the name of the repository for ease of navigation and usage.

```sh
$ git clone https://github.com/texas-ica/texas-ica.com.git
$ mv texas-ica.com ica
```

Change directories into `ica` and setup the virtual environment. If you already have `virtualenv` installed, the first command is unnecessary. Use `sudo` with the commands if installation fails the first time.

```sh
$ pip install virtualenv
$ virtualenv -p python3 venv
```

We work within a virtual environment, so you must activate the environment every time you would like to work on the project. Do this with `source venv/bin/activate`.

The configuration file requires a couple of environment variables required to build the project. These should be defined in the `activate` file inside `venv/bin`.

## Directory Structure

The technology stack is primarily Flask, MongoDB (main database), Redis (task queue broker), Backbone.js, and Semantic UI. There are many other frameworks used to make handling server and API requests easier. The following list should give a good intuition as to how the codebase is organized.

- `ica/models`: Database object schemas for MongoDB
- `ica/static`: Static assets for the website
    - `ica/static/js`: Dynamic content - navigation dropdowns, modals, etc. - and Backbone.js MVC
    - `ica/static/scss`: CSS stylesheets written in SCSS
    - `ica/static/img`: Images and icons
- `ica/templates`: Website templates using the Jinja2 engine
- `ica/tests`: Unit tests for different parts of the app
- `ica/views`: Views for the main website, social network, and other apps
- `forms.py`: Model and validation logic for forms
- `server.py`: Configuration for the server, database and frameworks

## Version Control

Always follow these guidelines when working with this repository:

- The `master` branch has production code, so this should *never* be untested or break. The Travis CI build should always be passing.
- The `dev` branch is used for staging and merging separate branches used for developing features or fixing bugs.
- Issues should be categorized as `feature`, `bug`, or `refactor`. They can be labelled as other things, but should fall within one or more of these three categories.

When editing the codebase, make sure the reason you're editing it is outlined as an issue in the issue tracker. This helps streamline the development process, manage edits over time, and provide evidence to the ICA executive board that work is being done. Here are some good tips to follow:

1. Create branches off of `develop` with the following convention:
- `feature`, `bug`, or `refactor` (ex: `feature/32-implement-profile-cache`, `bug/10-icons-not-found`, `refactor/23-modals-to-js-dir`)
- Forward slash
- GitHub issue number (found in issue tracker)
- Dashes, never underscores
- Meaningful and short description of the branch

2. Commit messages that reference the issue number and describe what was and why it was added/removed

3. The branch is merged into `develop` and every week, review all of the changes and when you're absolutely confident about your code, merge the branch into `master`

There shouldn't be any merge conflicts since only one person will be working on this repository at a time, but if there are, use GitHub's [merge conflict article](https://help.github.com/articles/resolving-a-merge-conflict-using-the-command-line/) to resolve it.
