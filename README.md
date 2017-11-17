# Prorality

WIP Proposal and voting application. Prorality aims to handle proposals (internal or external) and will allow commenting and voting.

## Install

```shell
$ pipenv install
```

## Environment variables

[direnv](https://direnv.net/) is handy for managing environment variables safely:

```shell
export ALLOWED_HOSTS=*
export DEBUG=True
export SECRET_KEY='make-one-up'
```

## Running the app

```shell
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

## Contributing?

All that I ask is that you use [styleguide-git-commit-message](https://github.com/slashsBin/styleguide-git-commit-message) style.
