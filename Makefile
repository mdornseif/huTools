# setting the PATH seems only to work in GNUmake not in BSDmake
PATH := ./pythonenv/bin:$(PATH)

default: check test examples


LINT_LINE_LENGTH= 110
FLAKE_EXCLUDES= huTools/_decorator.py,huTools/http/_httplib2/*.py,huTools/_jsonlib.py,huTools/markdown2.py,huTools/http/poster_encode.py
LINT_FLAKE8_ARGS= --max-complexity=12 --builtins=_ --exclude=$(FLAKE_EXCLUDES) --max-line-length=$(LINT_LINE_LENGTH)

check:
	flake8 $(LINT_FLAKE8_ARGS) huTools
	# -pylint --max-line-length=110 --ignore=_httplib2 huTools/

test: dependencies
	# PYTHONPATH=. ./pythonenv/bin/python huTools/aggregation.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/http/test.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/NetStringIO.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/formats.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/tools.py
	PYTHONPATH=. ./pythonenv/bin/python huTools/calendar/workdays.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/checksumming.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/humessaging.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/luids.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/obfuscation.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/postmark.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/structured.py
	# PYTHONPATH=. ./pythonenv/bin/python huTools/unicode.py

upload:
	rm -Rf build dist
	python setup.py sdist
	VERSION=`ls dist/ | perl -npe 's/.*-(\d+\..*?).tar.gz/$1/' | sort | tail -n 1`
	python setup.py sdist upload
	git tag v$(VERSION)
	git push origin --tags
	git commit -m "v$(VERSION) published on PyPi" -a
	git push origin

build:
	python setup.py build

dependencies: pythonenv

pythonenv: pythonenv/bin/activate

pythonenv/bin/activate:
	test -d pythonenv || virtualenv pythonenv
	pythonenv/bin/pip -q install -r requirements.txt

doc: examples
	paver gh_pages_build gh_pages_update -m "documentation fixup"

install: build
	sudo python setup.py install

clean:
	rm -Rf testenv pythonenv build dist html test.db pylint.out sloccount.sc pip-log.txt
	find . -name '*.pyc' -delete

.PHONY: build clean install upload check doc docs test dependencies pythonenv
