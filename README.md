# openai-web

## Usage

First set up Terraform backend in the `global` environment. This is where the state for all environments is stored.

```shell
PROFILE=retail-admin
(cd terraform && aws-vault exec "$PROFILE" --region us-west-2 -- make init-global)
(cd terraform && aws-vault exec "$PROFILE" --region us-west-2 -- make apply-global) 
```

Push image:

```shell
PROFILE=retail-admin
aws-vault exec "$PROFILE" --region us-west-2 -- ./scripts/push-image.sh --tag 0.2
```

Then deploy the `dev` environment.

```shell
PROFILE=retail-admin
(aws-vault exec "$PROFILE" --region us-west-2 -- ./scripts/terraform.sh --env dev --tag 0.2 init)
(aws-vault exec "$PROFILE" --region us-west-2 -- ./scripts/terraform.sh --env dev --tag 0.2 apply)
```

## Testing

```shell
 curl -X POST \
  http://localhost:8000/completion \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello world!"}'
```

## References

- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
