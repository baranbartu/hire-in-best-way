.PHONY: bootstrap

bootstrap: _virtualenv
	venv/bin/pip install -e .
	make train

_virtualenv: 
	virtualenv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install --upgrade setuptools

train:
	sh -c '. venv/bin/activate; pnoa train'

predict:
	sh -c '. venv/bin/activate; pnoa predict'
