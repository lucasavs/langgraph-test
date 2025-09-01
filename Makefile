run: 
	uv run fastapi dev app/main.py 

lint:
	uv run ruff check

format: 
	uv run ruff format