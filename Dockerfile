FROM python:3.10.6

RUN mkdir -p /code
COPY . /code/
WORKDIR /code

RUN apt update
RUN apt install -y libpq-dev build-essential
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT []
CMD pipenv run uvicorn main:app --host 0.0.0.0 --reload