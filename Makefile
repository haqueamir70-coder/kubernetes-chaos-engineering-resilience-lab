.PHONY: install test lint run docker-build validate deploy-local destroy-local

install:
	python -m pip install -r app/requirements.txt -r app/requirements-dev.txt

test:
	pytest -q app/tests

lint:
	ruff check app

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080

docker-build:
	docker build -t resilience-api:local .

validate:
	./scripts/validate.sh

deploy-local:
	kubectl apply -k platform/kubernetes/overlays/local

destroy-local:
	kubectl delete namespace resilience-lab --ignore-not-found
