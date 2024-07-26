# python-mariadb-kafka

project book libray as producer that provide CRUD APIs, database as default connect to MariaDB then applied as asyncronous handle. The operation CREATE(POST), UPDATE(PUT), and DELETE(DELETE) will be forwarded to Apache Kafka

## Init

```text
~/python-mariadb-kafka$ python3 -m venv venv
~/python-mariadb-kafka$ source venv/bin/activate
~/python-mariadb-kafka$ pip install -r requirements.txt
```

## How To Run

As default, the project run with ASGI network brigde and can directly run with the following command

```text
~/python-mariadb-kafka$ export PYTHONPATH="$PYTHONPATH:$PWD"
~/python-mariadb-kafka$ python app/main.py
```

## API Load Test With Locust

Make sure the application is already running, then do the following command

```text
~/python-mariadb-kafka$ pip install locust
~/python-mariadb-kafka$ cd tests/
~/python-mariadb-kafka$ locust
```

Access web browser `http://0.0.0.0:8089/` then do the configuration and testing

## Code Lint

There are four linter used in this project

1. black
2. flake8
3. ishort
4. mypy

Use the following command to install the required package

```text
~/python-mariadb-kafka$ pip install black flake8 isort mypy
```

then do the linter based on needed

```text
~/python-mariadb-kafka$ ./script/lint_all.sh # to run all the linter
~/python-mariadb-kafka$ ./script/lint_black.sh # to run black linter only
~/python-mariadb-kafka$ ./script/lint_flake8.sh # to run flake8 linter only
~/python-mariadb-kafka$ ./script/lint_isort.sh # to run isort linter only
~/python-mariadb-kafka$ ./script/lint_mypy.sh # to run mypy linter only
```
