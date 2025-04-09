runserver:
	@pdm run python manage.py runserver

makemigrations:
	@pdm run python manage.py makemigrations

migrate:
	@pdm run python manage.py migrate

precommit:
	@pdm run pre-commit run -a

test:
	@pdm run pytest