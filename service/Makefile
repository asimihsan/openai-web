build-docker:
	docker buildx build --platform=linux/arm64 -t openai-web-service:latest .

build-lima:
	lima nerdctl build --platform=linux/arm64 -t openai-web-service:latest .

run-docker:
	docker run \
		--platform=linux/arm64 \
		--privileged \
		-p 8000:8000 \
		--env-file .env \
		openai-web-service:latest

run-lima:
	lima nerdctl run \
		--platform=linux/arm64 \
		--privileged \
		-p 8000:8000 \
		--env-file .env \
		openai-web-service:latest

run-local:
	poetry run uvicorn http-serve:app --host 127.0.0.1 --reload