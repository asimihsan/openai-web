# openai-web

## Usage

poetry setup

```shell
cd service
poetry env use $(pyenv which python3) && poetry install --no-root
```

Set up Terraform backend in the `global` environment. This is where the state for all environments is stored.

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
 ➜ wscat -c ws://127.0.0.1:8000/ws/completion
Connected (press CTRL+C to quit)
> {"prompt": "hello world!"}
< Hello
< !
<  How
<  can
<  I
<  help
<  you
<  today
< ?
```

## Push

```shell
TAG=openai-prompt-0.2
(cd service && docker buildx build . -t "${TAG}" --platform linux/arm64)
(cd scripts && ./push-image.sh --tag "${TAG}")
```

## References

- https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb