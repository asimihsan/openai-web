#!/bin/sh

export PYTHONPATH="/opt/venv/lib/python3.10/site-packages:${FUNCTION_DIR}:${PYTHONPATH}"

if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
    exec /usr/bin/aws-lambda-rie python -m awslambdaric $1
else
    exec python -m awslambdaric $1
fi
