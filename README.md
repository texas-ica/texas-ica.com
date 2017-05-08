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

The backend of the app is written in Flask with MongoDB as the main database. There are many frameworks used to make handling server requests easier. The following list should give a good intuition as to how the codebase is organized.

- `ica/models`: Database object schemas for MongoDB
- `ica/static`: Static assets for the website
    - `ica/static/js`: Dynamic content - navigation dropdowns, modals, etc.
    - `ica/static/scss`: CSS stylesheets written in SCSS
    - `ica/static/img`: Images and icons
- `ica/templates`: Website templates using the Jinja2 engine
- `ica/tests`: Unit tests for different parts of the app
- `ica/views`: Views for the main website, social network, and other apps
- `forms.py`: Model and validation logic for forms
- `server.py`: Configuration for the server, database and frameworks
