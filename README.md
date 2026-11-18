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
uvicorn api.main:app --reload --port=8080 # or this
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
gcloud config unset auth/impersonate_service_account

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

## Workload Identity IAM policy binding

```
gcloud iam service-accounts add-iam-policy-binding \
--role="roles/iam.workloadIdentityUser" \
--member="serviceAccount:open-source-apps-001.svc.id.goog[dev/python-fastapi-postgresql-sa]" \
fastapi-db-iam-user@open-source-apps-001.iam.gserviceaccount.com
```

## Get request time via `curl` command

```
curl -s -o /dev/null -w "Total time: %{time_total} seconds\n" http://34.8.102.74
```

## Example GKE container log query

```
resource.type="k8s_container"
AND resource.labels.pod_name: "python-fastapi-postgresql"
AND resource.labels.container_name="python-fastapi-postgresql"
AND severity="INFO"
```

```
resource.type="k8s_container"
AND resource.labels.pod_name: "python-fastapi-postgresql"
AND resource.labels.container_name="python-fastapi-postgresql"
AND severity="INFO"
AND jsonPayload.user_id="usr_02453"
```

## Example Prometheus Query Language (PromQL)

```
kubernetes_io:container_memory_used_bytes{monitored_resource="k8s_container", namespace_name="dev", container_name="python-fastapi-postgresql"} / 1024 / 1024 / 1024
kubernetes_io:container_memory_request_utilization{namespace_name="dev"} * 100
sum by (path) (rate(http_request_total[5m]))
```

## Install helm chart as release into private GKE cluster

```
gcloud auth print-access-token | helm registry login europe-west1-docker.pkg.dev \
    --username oauth2accesstoken \
    --password-stdin

HTTPS_PROXY=localhost:8888 helm upgrade --install gcp-app-release \
    oci://europe-west1-docker.pkg.dev/open-source-apps-001/gcp-helm-charts/gcp-helm-chart \
    --version 2.1.0 \
    --namespace dev

HTTPS_PROXY=localhost:8888 kubectl create secret generic jwt-secret \
  --from-literal=jwt-secret='<YOUR-SECRET' \
  --dry-run=client -o yaml -n dev | HTTPS_PROXY=localhost:8888 kubectl apply -f -
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
