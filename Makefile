up:
	docker-compose -f docker-compose.yml -f local.yml up $(filter-out $@,$(MAKECMDGOALS))

build:
	docker-compose -f docker-compose.yml -f local.yml build $(filter-out $@,$(MAKECMDGOALS))

run:
	docker-compose -f docker-compose.yml -f local.yml run $(filter-out $@,$(MAKECMDGOALS))

restart:
	docker-compose -f docker-compose.yml -f local.yml restart $(filter-out $@,$(MAKECMDGOALS))

shell:
	docker-compose -f docker-compose.yml -f local.yml exec django /entrypoint.sh ./manage.py shell_plus

bash:
	docker-compose -f docker-compose.yml -f local.yml exec django /entrypoint.sh bash

makemigrations:
	docker-compose -f docker-compose.yml -f local.yml run --rm django ./manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose -f docker-compose.yml -f local.yml run --rm django ./manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

urls:
	docker-compose -f docker-compose.yml -f local.yml run django python manage.py show_urls

logs:
	docker-compose -f docker-compose.yml -f local.yml logs -f $(filter-out $@,$(MAKECMDGOALS))

test:
	docker-compose -f docker-compose.yml -f local.yml run --service-ports --rm django ./manage.py test $(filter-out $@,$(MAKECMDGOALS))

debug:
	docker-compose -f docker-compose.yml -f local.yml run --service-ports --rm $(filter-out $@,$(MAKECMDGOALS))

rm_pyc:
	find . -name '__pycache__' -name '*.pyc' | xargs rm -rf
