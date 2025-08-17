# Python FastAPI PostgreSQL

A Python FastAPI application connecting to PostgreSQL

![ci workflow](https://github.com/MatthewCYLau/python-fastapi-postgresql/actions/workflows/ci.yaml/badge.svg)

API URL here: [`https://python-fastapi-postgresql-620656388728.europe-west1.run.app/`](https://python-fastapi-postgresql-620656388728.europe-west1.run.app/)

## Run/build app locally

- Run app on host machine:

```bash
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 manage.py
uvicorn api.main:app --reload # or this
deactivate
```

- Run app as container:

```bash
docker compose up --build
```

### Install new packages

```bash
pip3 install boto
pip3 freeze > requirements.txt
```

## Connect to Cloud SQL

- Connect to Cloud SQL using `psql`:

```bash
psql postgresql://db_user:password@<cloud-sql-public-ip>:5432/python_fastapi
psql postgresql://db_user:password@<cloud-sql-public-ip>:5432/python_fastapi -f sql/access.sql # grant access to service account
```

- Connect to Cloud SQL using [Cloud SQL Auth proxy](https://cloud.google.com/sql/docs/mysql/connect-instance-auth-proxy):

```bash
# cd <location-to-cloud-sql-proxy>
./cloud-sql-proxy <INSTANCE_CONNECTION_NAME>
psql -h localhost -d python_fastapi -U db_user
```

- Connect to Cloud SQL using Cloud SQL Auth proxy _and_ IAM database authentication:

```bash
gcloud auth activate-service-account fastapi-db-iam-user@open-source-apps-001.iam.gserviceaccount.com --key-file <service-account-json-file.json>
gcloud config set auth/impersonate_service_account fastapi-db-iam-user@open-source-apps-001.iam.gserviceaccount.com
gcloud sql generate-login-token

# cd <location-to-cloud-sql-proxy>
./cloud-sql-proxy <INSTANCE_CONNECTION_NAME>
psql "dbname=python_fastapi host=127.0.0.1 user=fastapi-db-iam-user@open-source-apps-001.iam password=<sql-access-token>"
```

or this

```bash
gcloud auth application-default login --impersonate-service-account fastapi-db-iam-user@open-source-apps-001.iam.gserviceaccount.com

# cd <location-to-cloud-sql-proxy>
./cloud-sql-proxy --auto-iam-authn <INSTANCE_CONNECTION_NAME>
psql "dbname=python_fastapi host=127.0.0.1 user=fastapi-db-iam-user@open-source-apps-001.iam"
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
