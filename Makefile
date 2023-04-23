SUBDIRS := terraform

setup:
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir setup; \
	done

build-service:
	cd service && $(MAKE) build-docker

run-service:
	cd service && $(MAKE) run-docker

run-service-local:
	cd service && poetry run uvicorn http-serve:app --reload