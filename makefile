start:
	uvicorn main:app --reload

sync:
	pip freeze > requirements.txt
