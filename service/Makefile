build-docker:
	docker buildx build --platform=linux/arm64 -t openai-web-service:latest .

run-docker:
	docker run --platform=linux/arm64 --privileged -p 9000:8080 openai-web-service:latest
