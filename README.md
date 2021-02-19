![pypi](https://img.shields.io/pypi/v/pybadges.svg)
![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)

Python flask rest api using TDD 
--------------------  


Quick Start
----------
You can frok the repository by selecting this repository. Made neccessary changes according to your project name for below comand

1. Clone the repo
```
$ git clone https://github.com/<forked_user_name>/flask-rest-accelerator.git
$ cd flask-rest-accelerator
```

2. Initialize and activate a virtualenv:
```
virtualenv venv
source .env
python -m pip install autoenv
```
3. Install the dependencies:
```
$ pip install -r requirements.txt
```

4. For linting and formatting:
```
$ pre-commit install
$ pre-commit install --hook-type commit-msg
- pre-commit installed at .git\hooks\pre-commit 
- Can I run the hooks without a commit? pre-commit run -a
```

5. Running postgres locally in ubuntu

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
sudo apt-get -y install postgresql
-----------------
# Start the service
sudo service postgresql start
# Setup initial password
sudo -u postgres psql postgres
\password postgres
---------------------
# Create database
createdb test_db
createdb postgres # if not created bydefault
```

6. Run migration
```
# Migrations is a way of propagating changes we make to our models (like adding a field, deleting a model, etc.) into the database schema. Flask-Migrate uses Alembic to autogenerate migrations for us.

python manage.py db init
python manage.py db migrate # alembic auto generate the model
python manage.py db upgrade
```

7. Run the development server:
```
export FLASK_ENV=development
flask run
```

8. Running unit test
```
source .env
python test_bloglist.py
```

9. Code coverage
```
py.test --cov=. --cov-config .coveragerc
```

