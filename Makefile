install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

pull:
	python scripts/pull_data.py --start 2019 --end 2024 --team SEA

features:
	python scripts/build_features.py

figures:
	python scripts/make_figures.py

test:
	pytest -q
