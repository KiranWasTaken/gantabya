
login:
	docker login

dbuild:
	docker  build --platform linux/amd64 -t sugamdocker35/gantabya:v4 .

push:
	docker push sugamdocker35/gantabya:v4

ssh:
	ssh root@64.227.135.50
	ssh -i gantabya.pem ubuntu@13.61.22.70

postgres:
	docker run --name gantabya --network gantabya -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_DB=gantabya -e POSTGRES_PASSWORD=secret -d postgres:alpine

ssh-pwd:
	

create-network:
	docker network create app
venv:
	python3 -m venv venv

activate:
	source venv/bin/activate

build: requirements.txt
	pip3 install -r requirements.txt
	@touch build

run:
	python3 manage.py runserver

migratefile:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

lint:
	pylint apps

network:
	docker network create app

docker-run:
	docker run --name gantabya --network gantabya -d -p 80:8000  sugamdocker35/gantabya:v4

log:
	docker logs gantabya -f
list:
	docker ps

mssql:
	docker run --name mysql-gantabya --network app -e MYSQL_ROOT_PASSWORD=root_password -e MYSQL_USER=gantabya_user  -e MYSQL_PASSWORD=gantabya_password  -e MYSQL_DATABASE=gantabya -p 3306:3306 -d mysql:latest

