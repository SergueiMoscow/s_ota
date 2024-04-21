FROM python:3.12
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN apt-get update && apt-get install -y libgl1-mesa-glx && \
    python -m pip install --upgrade pip && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-root --no-cache --no-interaction

CMD ["sh", "./entrypoint.sh"]
