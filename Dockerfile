FROM python:3.12
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -yq update \
    && apt-get -yq install build-essential libffi-dev python-dev-is-python3 \
    && apt-get purge -y --auto-remove

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/"

# Install uv
RUN pip install uv

WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./

# Install dependencie
RUN uv sync --frozen

COPY . .
