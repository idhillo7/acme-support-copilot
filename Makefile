.PHONY: dev test run worker
dev:
	pip install -r requirements.txt -r requirements-dev.txt
test:
	pytest -q
run:
	uvicorn app.server:app --reload --port 8080
worker:
	python -m app.ops.draft_worker
