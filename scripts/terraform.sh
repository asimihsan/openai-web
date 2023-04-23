#!/usr/bin/env bash

set -euo pipefail

# terrafrom.sh is a wrapper around Terraform that passes in tfvars like 'ecr_repository_url' and 'image_tag'.
# It also handles the fact that Terraform state files are stored in different directories for dev and prod.
#
# Usage:
#   ./scripts/terraform.sh --env dev --tag 0.2 apply
#   ./scripts/terraform.sh --env prod --tag 0.2 apply

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "${SCRIPT_DIR}/.." && pwd )"
TERRAFORM_DIR="${ROOT_DIR}/terraform"

TAG=
ENV=
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --tag)
      TAG="$2"
      shift
      shift
      ;;
    --env)
      ENV="$2"
      shift
      shift
      ;;
    *)
      # Pass through all other arguments to Terraform.
      break
      ;;
  esac
done

# tag is only needed if this is not an init command.
if [[ "${1}" != "init" ]]; then
  if [[ -z "${TAG}" ]]; then
    echo "Missing --tag argument"
    exit 1
  fi
fi

if [[ -z "${ENV}" ]]; then
  echo "Missing --env argument"
  exit 1
fi

if [[ "${ENV}" != "dev" && "${ENV}" != "prod" ]]; then
  echo "Invalid --env argument. Must be 'dev' or 'prod'"
  exit 1
fi

# This is the only Terraform command that needs to be run in the global directory.
# All other Terraform commands are run in the env directory.
ECR_REPOSITORY_URL=$(cd "${TERRAFORM_DIR}/env/global" && terraform output -raw ecr_repository_url)

# Run the Terraform command in the env directory.
pushd "${TERRAFORM_DIR}/env/${ENV}" > /dev/null
trap "popd > /dev/null" EXIT

# Run the Terraform command.
terraform "$@" -var "ecr_repository_url=${ECR_REPOSITORY_URL}" -var "image_tag=${TAG}"
