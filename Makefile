SUBDIRS := terraform

setup:
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir setup; \
	done