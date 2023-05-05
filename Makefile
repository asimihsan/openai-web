SUBDIRS := terraform

build-service:
	cd service && $(MAKE) build-docker

run-service:
	cd service && $(MAKE) run-docker

run-service-local:
	cd service && poetry run uvicorn http-serve:app --host 0.0.0.0 --reload