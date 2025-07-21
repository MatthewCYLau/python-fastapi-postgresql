# Python FastAPI PostgreSQL

A Python FastAPI application connecting to PostgreSQL

![ci workflow](https://github.com/MatthewCYLau/python-fastapi-postgresql/actions/workflows/ci.yaml/badge.svg)

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

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
