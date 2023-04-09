# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04 AS base

# Set the architecture to linux/arm64
ARG TARGETARCH=arm64

# Install Python and other dependencies
RUN mount=type=cache,target=/var/lib/apt/lists && \
    mount=type=cache,target=/var/cache/apt && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    unzip

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry export > /requirements.txt && \
    pip3 install -r /requirements.txt && \
    rm -f /requirements.txt

# Install the AWS Lambda Runtime Interface Client
RUN pip install awslambdaric

# Install Playwright and the Firefox browser
RUN mount=type=cache,target=/var/lib/apt/lists && \
    mount=type=cache,target=/var/cache/apt && \
    python -m playwright install-deps && \
    python -m playwright install firefox

# Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
# See: https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh

# Copy the source code
COPY --link . .

# Set the entrypoint and command
ENTRYPOINT ["/entry.sh"]
CMD ["lambda_chat.lambda_handler"]
