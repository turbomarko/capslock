#!/bin/sh

# Arguments
c1=$1  # Environment
c2=$2  # Command
c3=$3  # Command argument (optional)


# Help command
help() {
  echo "Usage: <environment> <command> [<command argument>]"
  echo "environment:"
  echo "* local"
  echo "* production"
  echo ""
  echo "command:"
  echo "* build -- build the docker image"
  echo "* init -- build, generate_ssl_certificates, git init, pre-commit install"
  echo "* up -- start the docker container"
  echo "* down -- stop the docker container"
  echo "* shell -- open Django shell"
  echo "* showmigrations -- show all migrations of the project"
  echo "* makemigrations -- create migration files based on model changes"
  echo "* migrate -- migrate the migration file changes into the database"
  echo "* backup_db -- create a database backup locally"
  echo "* list_backup_db -- list the local database backups"
  echo "* restore_db [BACKUP_FILE] -- restore the local database from a backup"
  echo "* upload_backup_db_s3 -- upload a database backup file to S3"
  echo "* download_backup_db_s3 [BACKUP_FILE] -- download a specific database backup from S3"
  echo "* ruff -- test ruff formatting"
  echo "* format -- format code with ruff"
  echo "* pytest -- run all tests"
  echo "* coverage -- run all tests and print coverage information"
  echo "* mypy -- check python typings"
  echo "* check_all -- check tests, types and formatting"
}


# App commands
build() {
  docker compose -f docker-compose."$c1".yml build
}

init() {
  echo "Do you confirm that the following are installed: docker, docker compose, git, openssl and pre-commit (y/n)? "
  read -r answer
  if [ "$answer" = "y" ]
  then
    build
    generate_ssl_certificates
    git init
    pre-commit install
  else
    echo "Operation aborted. Please install docker, docker compose, git, openssl and pre-commit."
  fi
}

up() {
  docker compose -f docker-compose."$c1".yml up
}

down() {
  docker compose -f docker-compose."$c1".yml down
}


# Django commands
shell() {
  docker compose -f docker-compose."$c1".yml run --rm analytics python manage.py shell
}

showmigrations() {
  docker compose -f docker-compose."$c1".yml run --rm analytics python manage.py showmigrations
}

makemigrations() {
  docker compose -f docker-compose."$c1".yml run --rm analytics python manage.py makemigrations
}

migrate() {
  docker compose -f docker-compose."$c1".yml run --rm analytics python manage.py migrate
}

load_data() {
  docker compose -f docker-compose."$c1".yml run --rm analytics python manage.py loaddata marketing_data.json
}

setup() {
  build && migrate && load_data && up
}


# Code check commands
ruff() {
  echo "RUFF" && docker compose -f docker-compose."$c1".yml run --rm analytics ruff check
}

format() {
  echo "RUFF" && docker compose -f docker-compose."$c1".yml run --rm analytics ruff format
}

mypy() {
  echo "MYPY" && docker compose -f docker-compose.local.yml run --rm analytics mypy analytics
}

pytest() {
  echo "PYTEST" && docker compose -f docker-compose."$c1".yml run --rm analytics pytest
}

coverage() {
  docker compose -f docker-compose.local.yml run --rm analytics coverage run -m pytest
  docker compose -f docker-compose.local.yml run --rm analytics coverage report
  docker compose -f docker-compose.local.yml run --rm analytics coverage html
}

check_all() {
  ruff && echo "ruff - No issue found"
  mypy && echo "mypy - No issue found"
  pytest && echo "pytest - No issue found"
}

case "$c1" in
  "local"|"production")
    $c2;;
  *)
    help;;
esac
