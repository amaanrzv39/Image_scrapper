install:
	pip install -r requirements.txt

test:
	python -m pytest -vv test_app.py

lint:
	pylint --disable=R,C app.py

run:
	python app.py