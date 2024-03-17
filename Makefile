# create virtaulenv and install dependencies for development
init:
	virtualenv --version || pip install virtualenv \
	&& virtualenv --always-copy --python python3 venv
	&& source venv/bin/activate

# rebuild the docker image
docker_build:
	docker build -t challenge:latest .

# run already built docker image
docker_run_etl:
	docker run -i \
	  -e SQLALCHEMY_URL -e LOG_DIR=/app/logs -e CONFIG_DIR=/app/config \
		-v "$(PWD)/logs":/app/logs \
		challenge:latest run_etl

docker_run_migrations:
	docker run -i -e SQLALCHEMY_URL challenge:latest run_migrations

# run all db schema migrations
run_migrations:
	alembic upgrade head

# run etl through main.py as entrypoint
run_etl:
	python src/main.py


run_tests:
	python -m unittest
