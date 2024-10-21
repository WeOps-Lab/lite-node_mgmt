push:
	git add . && codegpt commit . && git push

setup:
	virtualenv .venv -p python3.10
	./.venv/bin/pip install pip-tools

install:
	./.venv/bin/pip-compile ./requirements/requirements.txt ./requirements/requirements-dev.txt ./requirements/requirements-ops.txt -v --output-file ./requirements.txt
	./.venv/bin/pip-sync -v