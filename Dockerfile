FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.1.13
ENV PATH="${PATH}:/root/.poetry/bin"

RUN pip install -U pip \
    && apt-get update \
    && apt install -y curl netcat \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

WORKDIR /usr/src/app
COPY . .
RUN poetry export -f requirements.txt > requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT [ "./entrypoint.sh" ]
