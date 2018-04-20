up:
	docker-compose -f docker-compose.yml -f local.yml up $(filter-out $@,$(MAKECMDGOALS))

build:
	docker-compose -f docker-compose.yml -f local.yml build $(filter-out $@,$(MAKECMDGOALS))

shell:
	docker-compose -f docker-compose.yml -f local.yml exec django /entrypoint.sh ./manage.py shell_plus

test:
	docker-compose -f docker-compose.yml -f local.yml exec django /entrypoint.sh ./manage.py test

bash:
	docker-compose -f docker-compose.yml -f local.yml exec django /entrypoint.sh bash

makemigrations:
	docker-compose -f docker-compose.yml -f local.yml run --rm django ./manage.py makemigrations $(filter-out $@,$(MAKECMDGOALS))

migrate:
	docker-compose -f docker-compose.yml -f local.yml run --rm django ./manage.py migrate $(filter-out $@,$(MAKECMDGOALS))

debug:
	docker-compose -f docker-compose.yml -f local.yml run --service-ports --rm $(filter-out $@,$(MAKECMDGOALS))
