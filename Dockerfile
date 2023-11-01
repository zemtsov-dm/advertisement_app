FROM python:3.11-slim


ARG YOUR_ENV

ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.6.1

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential

RUN pip install "poetry==$POETRY_VERSION"

RUN mkdir /app

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-dev\
    && rm -rf /root/.cache/pypoetry

COPY . .

RUN chmod a+x /app/docker/app.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]