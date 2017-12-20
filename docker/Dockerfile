FROM python:3.6.3

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PYTHONPATH /code:$PYTHONPATH

WORKDIR /code

COPY Pipfile .
COPY Pipfile.lock .

RUN set -ex \
    && pip install pipenv --upgrade \
    && pipenv install --deploy --system \
    && pipenv install --deploy --system --dev

COPY . /code/

EXPOSE 8000

CMD manage.py runserver 0.0.0.0:8000
