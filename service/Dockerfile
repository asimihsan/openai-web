# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04 AS base

# Set the architecture to linux/amd64
ARG TARGETARCH=amd64

# Define function directory
ARG FUNCTION_DIR="/function"

# Install Python and other dependencies
RUN mount=type=cache,target=/var/lib/apt/lists && \
    mount=type=cache,target=/var/cache/apt && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    unzip \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files
WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry export > /requirements.txt && \
    pip3 install -r /requirements.txt --target "${FUNCTION_DIR}" && \
    rm -f /requirements.txt

# Install the AWS Lambda Runtime Interface Client
RUN pip install \
        --target ${FUNCTION_DIR} \
        awslambdaric

# Install Playwright and the Chromium browser
RUN pip install --target "${FUNCTION_DIR}" playwright
ENV PYTHONPATH="${FUNCTION_DIR}:${PYTHONPATH}"
RUN python -m playwright install chromium

# Copy the source code
COPY . .

# Build the final image
FROM base AS final

# Copy the virtual environment and function directory from the base image
COPY --from=base /opt/venv /opt/venv
COPY --from=base ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set the working directory
WORKDIR /app

# Add the function directory to the Python path
ENV PYTHONPATH="${FUNCTION_DIR}:${PYTHONPATH}"

# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
# See: https://aws.amazon.com/blogs/aws/new-for-aws-lambda-container-image-support/
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh

# Set the entrypoint and command
ENTRYPOINT ["/entry.sh"]
CMD ["lambda_chat.lambda_handler"]
