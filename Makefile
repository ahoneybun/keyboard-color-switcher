SHELL := /bin/bash


venv:
	if [[ ! -d .venv ]]; then \
		python3 -m venv .venv; \
	fi

install-dev: venv
	pip install -r requirements.dev.txt
