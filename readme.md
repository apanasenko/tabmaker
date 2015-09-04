# Tabmaker

*TODO: Add text about project*

## Installation

#### Step 1. Environment

Install [Git](http://git-scm.com/) and [Python 3.3](https://www.python.org/downloads/) or higher. Also, You need install [pip](https://pip.pypa.io/en/latest/installing.html) and [setuptools](https://pypi.python.org/pypi/setuptools#downloads). Add paths to environment of your machine and check in terminal:

    >>> git --version
    git version 2.5.0.windows.1

    >>> python --version
    Python 3.4.3

    >>> pip -V
    pip 7.1.2 from <path to Python>\lib\site-packages (python 3.4)

    >>> easy_install --version
    setuptools 18.2

#### Step 2. Database

Note: If you are not will developing the database and migration, or you would like to use SQLite, safely skip this step.

Install your favorite database system and adapter of this database for the Python. For example, [PostgreSQL](http://www.postgresql.org/download/) and [psycopg2](http://initd.org/psycopg/docs/install.html). Create DATABASE and USER for our project.

For PostgreSQL:

    CREATE DATABASE <database_name>;
    CREATE USER <user_name> WITH PASSWORD <password>;
    GRANT ALL privileges ON DATABASE <database_name> TO <user_name>;

#### Step 3. Deploy the project

Firstly, run a clone:

	git clone https://<your name in bitbucket>@bitbucket.org/apanasenko_aa/debatestournament.git

This will download the latest sources into a directory `DebatesTournament`.

Secondly, switch to the `DebatesTournament` directory and install all the necessary dependencies

    pip install -r requirements.txt

Thirdly, copy all settings files from `DebatesTournament\settings\default` to `DebatesTournament\settings`

*   `database.py` -- Configure your database. Read info for your database in [djbook](https://docs.djangoproject.com/en/1.8/ref/settings/#databases).   Templates for SQLite and PostgreSQL already in file, remove unnecessary and set all `<params>`.

*   `security.py` -- Set `SECRET_KEY` as random line and set `DEBUG` and `TEMPLATE_DEBUG` as `True`.

*	`smtp_email.py` -- Set `EMAIL_HOST_USER` as your email and `EMAIL_HOST_PASSWORD` as password for this.

Finaly, initiation database:

    python manage.py migrate

and check your system:

    >>> python manage.py check
    System check identified no issues (0 silenced).

That's all, enjoy =)) But if you have any problem, read this [help](http://lmgtfy.com/?q=fix+any+problem+in+django)

## Start server

To run server change directory to repository root and execute:

    >>> python manage.py runserver
    Performing system checks...

    System check identified no issues (0 silenced).
    September 01, 2000 - 00:00:00
    Django version 1.8.4, using settings 'DebatesTournament.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.

And open [localhost](http://127.0.0.1:8000/) in your browser.
