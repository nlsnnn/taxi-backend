FROM python:3.12-slim

RUN pip install poetry==2.0.1

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/
WORKDIR /app

RUN poetry install --no-interaction
RUN poetry add gunicorn
RUN poetry add uvloop

COPY start.sh /app/start.sh
COPY . /app/

CMD ["sh", "/app/start.sh"]