SUBDIRS := terraform

build-service:
	cd service && $(MAKE) build-docker

run-service:
	cd service && $(MAKE) run-docker

run-service-local:
	cd service && poetry run uvicorn http-serve:app --host 127.0.0.1 --reload