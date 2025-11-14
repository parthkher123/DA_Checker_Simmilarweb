# Makefile for DA/PA Checker API setup

.PHONY: help env install run clean

help:
	@echo "Available targets:"
	@echo "  env      Create Python virtual environment in ./env"
	@echo "  install  Install requirements into ./env"
	@echo "  run      Run the FastAPI app with Uvicorn"
	@echo "  clean    Remove the virtual environment"

env:
	python3 -m venv env

install: env
	. ./env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	. ./env/bin/activate && uvicorn app.main:app --reload

clean:
	rm -rf env __pycache__
