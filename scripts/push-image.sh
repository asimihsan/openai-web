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


REGION="us-east-2"
ECR_REPOSITORY_URL="519160639284.dkr.ecr.us-east-2.amazonaws.com/my-k8s-cluster-dev-ecr-repository"

aws ecr get-login-password --region "${REGION}" | docker login --username AWS --password-stdin "${ECR_REPOSITORY_URL}"
docker tag openai-web-service:latest "${ECR_REPOSITORY_URL}:${TAG}"
docker push "${ECR_REPOSITORY_URL}:${TAG}"
