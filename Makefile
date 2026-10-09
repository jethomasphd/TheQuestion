PYTHON ?= python3
.PHONY: research ingest verify proxies animatic rough release-check final test
research:
	$(PYTHON) scripts/build_timeline.py research
ingest:
	$(PYTHON) scripts/probe_media.py $(ARGS)
verify:
	$(PYTHON) scripts/build_timeline.py verify
proxies:
	$(PYTHON) scripts/make_proxies.py
animatic:
	$(PYTHON) scripts/render.py animatic
rough:
	$(PYTHON) scripts/render.py rough
release-check:
	$(PYTHON) scripts/validate_sources.py --release
final:
	$(PYTHON) scripts/package_release.py
test:
	$(PYTHON) -m unittest discover -s tests -v
