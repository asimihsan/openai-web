# openai-web

## Usage

First set up Terraform backend in the `global` environment. This is where the state for all environments is stored.

```shell
PROFILE=retail-admin
(cd terraform && aws-vault exec "$PROFILE" --region us-west-2 -- make init-global)
(cd terraform && aws-vault exec "$PROFILE" --region us-west-2 -- make apply-global) 
```

Then deploy the `dev` environment.

```shell
PROFILE=retail-admin
(cd terraform && aws-vault exec "$PROFILE" --region us-west-2 -- make init-dev)
(cd terraform && aws-vault exec "$PROFILE" --region us-west-2 -- make apply-dev) 
```

## References

- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html