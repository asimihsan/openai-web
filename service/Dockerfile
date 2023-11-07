FROM --platform=${TARGETPLATFORM:-linux/arm64} ubuntu:22.04

ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH
ARG PYTHON_VERSION=3.11.6

ENV DEBIAN_FRONTEND=noninteractive
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

# Install Python and other dependencies using pyenv
RUN mount=type=cache,target=/var/lib/apt/lists && \
    mount=type=cache,target=/var/cache/apt && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        git \
        libbz2-dev \
        libffi-dev \
        liblzma-dev \
        libncurses5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libxml2-dev \
        libxmlsec1-dev \
        llvm \
        make \
        mecab-ipadic-utf8 \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev && \
        curl https://pyenv.run | bash && \
        pyenv update && \
#        PYTHON_CFLAGS=-march=native CONFIGURE_OPTS='--enable-optimizations --with-lto' \
          pyenv install $PYTHON_VERSION && \
        pyenv global $PYTHON_VERSION && \
        pyenv rehash

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright

# Install Playwright and the Firefox browser
RUN mount=type=cache,target=/var/lib/apt/lists && \
    mount=type=cache,target=/var/cache/apt && \
    pip3 install playwright && \
    python -m playwright install-deps && \
    python -m playwright install firefox

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry install

# Copy the source code
COPY --link . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "http-serve:app", "--host", "0.0.0.0"]
