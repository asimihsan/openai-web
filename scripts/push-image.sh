#!/usr/bin/env bash

set -euo pipefail

TAG=
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --tag)
      TAG="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown argument: $key"
      exit 1
      ;;
  esac
done

if [[ -z "${TAG}" ]]; then
  echo "Missing --tag argument"
  exit 1
fi


SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "${SCRIPT_DIR}/.." && pwd )"
REGION="us-west-2"

ECR_REPOSITORY_URL="$(cd "${ROOT_DIR}" && terraform output -raw -state=terraform/env/global/terraform.tfstate ecr_repository_url)"

aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ECR_REPOSITORY_URL}"
docker tag openai-web-service:latest "${ECR_REPOSITORY_URL}:${TAG}"
docker push "${ECR_REPOSITORY_URL}:${TAG}"
