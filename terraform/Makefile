include .env
export

GLOBAL_TF_VARS := -var "backend_bucket_name=$(BACKEND_BUCKET_NAME)" \
	-var "backend_dynamodb_table_name=$(BACKEND_DYNAMODB_TABLE_NAME)"
DEV_BACKEND_CONFIG := -backend-config="bucket=$(BACKEND_BUCKET_NAME)" \
	-backend-config="dynamodb_table=$(BACKEND_DYNAMODB_TABLE_NAME)" \
	-backend-config="key=dev-terraform.tfstate" \
	-backend-config="region=$(AWS_REGION)"
PROD_BACKEND_CONFIG := -backend-config="bucket=$(BACKEND_BUCKET_NAME)" \
	-backend-config="dynamodb_table=$(BACKEND_DYNAMODB_TABLE_NAME)" \
	-backend-config="key=prod-terraform.tfstate" \
	-backend-config="region=$(AWS_REGION)"

setup:
	brew install terraform

.PHONY: fmt
fmt:
	terraform fmt -recursive

validate:
	terraform validate

init-global:
	cd env/global && terraform init

plan-global:
	cd env/global && terraform plan $(GLOBAL_TF_VARS)

apply-global:
	cd env/global && terraform apply $(GLOBAL_TF_VARS)

destroy-global:
	cd env/global && terraform destroy $(GLOBAL_TF_VARS)
