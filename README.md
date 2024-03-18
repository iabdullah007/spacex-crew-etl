# SpaceX Crew ETL

The goal of this ETL tool written in Python is to pull data from the SpaceX Crew API and efficiently load it into a Postgres database. This pipeline facilitates the extraction and loading process, enabling users to conduct further analysis on the data stored in Postgres.



## Assumptions

- Utilization of a Python script without reliance on any designated data pipeline or orchestration tools such as Airflow or Dagster
- Implementation of a dockerized Python script
- Incorporation of schema migration and evolution
- Utilization of the SpaceX Crew API as a sample API, with acknowledgment of limitations regarding the available number of crews that can be retrieved in a single extraction
- Pagination functionality has not been integrated into the extraction module for the API data, but can be added as needed by leveraging proper query parameters to retrieve only the necessary data

## Pre-requisits
- Python version 3.8 or above
- Docker
- Make/Gmake
- Mac as development machine (Windows not supported)


## Implementation
A python project with srouce (src) and tests along with config files for the project i.e. logging configurations. Database schema migration/evolution is handled by Alembic. ETL (extract/transform/load) via plain Python to extract all the given Crews by SpaceX, validate and load them into Postgres.

### 1. Extract, transform and load the data into database

The main structure of the code is there, under `src/`, which contains extractor/transformer and loader.
Through which we can migrate the whole SpaceX Crew API data into the new system.

- `src/etl/extractor` extracts the data from API
- `src/etl/transform` transform and validate data through [Pydantic](https://docs.pydantic.dev/latest/) (a python library for data validation)
- `src/etl/loader` loads transformed data into Postgres by casting [Pydantic](https://docs.pydantic.dev/latest/) models to SQLAlchemy ORM for Postgres

### 2. Schema (migration/evolution)
Schema migration & evolution is a critical part of Data Pipelines where handing it and keeping track of revisions overtime helps team to have better understanding of lineage and changes overtime.

[Alembic](https://alembic.sqlalchemy.org/en/latest/) is used to automate schema migration and evolution. It will apply all the schema changes to build current state via `alembic upgrade head` command.

### 2. Test case

To ensure long-tem maintainability of ETL code, and to double-check that it works as it should, some unit tests are added under `tests/`. As it is just for showing what can be done, more unit tests can be added to improve the test coverage and code quality.

### 3. Use postgresql as storage & data warehouse

Postgres is used as a data storage/warehouse where data is loaded and later reports are built on top of that data through querying via Postgres.



## Run Steps

Run postgres instance either in local docker or via cloud platforms such as Aiven.
When using Aiven, create Postgres service, and export **Service URI** something like `postgresql://postgres:postgres@localhost` as done below. Don't forget to use `postgresql://` instead of `postgres://` in the Service URI.

```shell
export SQLALCHEMY_URL=<Aiven Postgres Service URI>
```

Build docker image
```shell
make docker_build
```

Run database schema migrations through below mentioned commands. It will build the current state of the database schemas i.e. CREW table, and upgrade the state in DB to reach the current version.
```shell
make docker_run_migrations
```

Run ETL to extract data from API, transform/validation and load to Postgres in **crew** table.
```shell
make docker_run_etl
```

Run **pgcli** to connect to Postgres DB and run queryies
```shell
docker run -it --rm dencold/pgcli $SQLALCHEMY_URL
```

SQL statement
```sql
select count(1) from crew
```
Output

| count   |
|---------|
| 30      |


SQL statement
```sql
select * from crew limit 5
```
Output

| id  | name | status | agency | wikipedia | launches |
| --- | ---  | ---    | ---    | ---       | ---      |
| 5fe3c5beb3467846b3242199 | Thomas Marshburn | ACTIVE   | NASA     | https://en.wikipedia.org/wiki/Thomas_Marshburn  | ['5fe3b15eb3467846b324216d'] |
| 5fe3c5f6b3467846b324219a | Matthias Maurer  | ACTIVE   | ESA      | https://en.wikipedia.org/wiki/Matthias_Maurer   | ['5fe3b15eb3467846b324216d'] |
| 607a3a5f5a906a44023e0870 | Jared Isaacman   | ACTIVE   | SpaceX   | https://en.wikipedia.org/wiki/Jared_Isaacman    | ['607a37565a906a44023e0866'] |
| 607a3ab45a906a44023e0872 | Hayley Arceneaux | ACTIVE   | SpaceX   | https://en.wikipedia.org/wiki/Hayley_Arceneaux  | ['607a37565a906a44023e0866'] |
| 5ebf1a6e23a9a60006e03a7a | Robert Behnken   | ACTIVE   | NASA     | https://en.wikipedia.org/wiki/Robert_L._Behnken | ['5eb87d46ffd86e000604b388'] |



## Frther Improvements and considerations
In order to set up production-grade pipelines to handle hundreds or thousands of pipelines, it is important to consider specific tools and orchestrators, as well as data storage layers and techniques.

- Data Storage:
  - Raw data can be stored in low-cost blob storage such as S3/GCS.
  - Utilize different approaches for transforming data, such as employing distributed data processing engines like Spark or query engines like Athena/Trino, and ingesting transformed data into Data Warehouse for querying.

- Data Pipelines:
  - Dockerizing is a viable option.
  - Current solution lacks proper orchestration capabilities. We can use cron-jobs but it is not proper solution.
  - Orchestration can be efficiently managed through specific tools like Airflow/Dagster.
  - Airflow provides a systematic approach for writing workflows/pipelines programmatically, aiding in proper abstraction, monitoring, and validation of workflows.

- Monitoring and Observability:
  - Monitor each component of the data pipeline and implement appropriate alerting systems.
  - Integrate open source or enterprise solutions like Grafana, Datadog, or AWS CloudWatch with the Data Infrastructure for effective monitoring.

- Data Quality and Schema Change/Evolution:
  - Data Consumers need to stay informed about changes made by data producers and track the evolution of data assets.
  - Utilize tools like [Alembic](https://alembic.sqlalchemy.org/en/latest/) for schema validation and evolution over time.
  - Implement data quality checks at each stage of the pipeline, track and monitor them, and set up proper alerting mechanisms.

- Knowledge Sharing and Onboarding Guidelines:
  - Make technological decisions based on business requirements, goals, team capabilities, and personas involved.
  - Develop comprehensive onboarding guidelines and hands-on labs to facilitate contributions from any team member.
  - Continuous improvement of the tech stack is crucial, along with fostering a culture of knowledge sharing.


## Links
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python
- [Pydantic](https://docs.pydantic.dev/latest/) - data validation library for Python
