build-docker:
	docker buildx build --platform=linux/amd64 -t openai-web-service .

run-docker:
	docker run --platform=linux/amd64 -p 9000:8080 openai-web-service