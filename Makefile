mysql:
	docker run -d \
	--name finance_tracker_mysql \
	-e MYSQL_ROOT_PASSWORD=finance-secret-pw \
	-e MYSQL_DATABASE=finance_tracker \
	-e MYSQL_USER=finance_user \
	-e MYSQL_PASSWORD=finance_pass \
	-v finance_tracker_data_mysql:/var/lib/mysql \
	-p 3307:3306 \
	mysql:8.0
venv:
	python -m venv .venv
activate:
	source .venv/bin/activate
deactivate:
	deactivate
rmdb:
	docker rm -f finance_tracker_mysql
startdb:
	docker start finance_tracker_mysql
stopdb:
	docker stop finance_tracker_mysql
createdb:
	docker exec -it finance_tracker_mysql createdb --username=finance_user --owner=finance_user finance_tracker
dropdb:
	docker exec -it finance_tracker_mysql dropdb finance_tracker
initdb:
	flask db init
	flask db migrate -m "Initial migration"
	flask db upgrade
run:
	python run.py
seed:
	python -m app.seed
test:
	python -m pytest -v -s

start:
	make startdb
	make activate
	make run

stop:
	make deactivate
	make stopdb

.PHONY: mysql activate deactivate rmdb startdb stopdb createdb dropdb initdb run seed start stop
