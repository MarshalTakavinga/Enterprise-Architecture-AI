.PHONY: install ingest ask api ui test eval up down

install:            ## local dev install
	pip install -e ".[ui,pgvector,llm,dev]"

ingest:             ## (re)build the index from data/corpus
	eaka ingest

ask:                ## make ask Q="Are we allowed to use NoSQL?"
	eaka ask "$(Q)"

api:
	uvicorn eaka.api:app --reload --port 8000

ui:
	streamlit run app/streamlit_app.py

test:
	pytest -q

eval:
	python eval/run_eval.py

up:                 ## full stack with PostgreSQL + pgvector
	docker compose up --build

down:
	docker compose down
