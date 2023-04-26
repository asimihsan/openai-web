FROM --platform=${TARGETPLATFORM:-linux/arm64} ubuntu:22.04

ARG TARGETPLATFORM
ARG TARGETOS
ARG TARGETARCH

# Install Python and other dependencies
RUN mount=type=cache,target=/var/lib/apt/lists && \
    mount=type=cache,target=/var/cache/apt && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    curl \
    unzip

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

RUN poetry export > /requirements.txt && \
    pip3 install -r /requirements.txt && \
    rm -f /requirements.txt

# Copy the source code
COPY --link . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "http-serve:app", "--host", "0.0.0.0"]
