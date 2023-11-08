# REST API APP

## Priprava okolja
- Python lokalna verzija: `pyenv local 3.9.5`
- Ustvarjanje novega virtualnega okolja: `python -m venv .venv`
- Aktivacija virtualnega okolja: `source .venv/bin/activate`
- Ustvarimo `requirements_dev.txt` in `requirements.txt`
- Namesitmo vse potrebne pakete: `pip install -r requirements_dev.txt`
- Dodamo vscode mapo
- Dodamo `.gitignore`

## Priprava strukture za aplikacijo
- Ustvarimo mape `app` in `tests`.
- Ustvarimo vse potrebne datoteke in mape.
- Dodamo osnovo in zaženemo app: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
    - Pokažemo kako na VS Code povežemo port na lokal host.

## Priprava Docker okolja
- Namestimo Docker s pomočjo skripte:
    - `chmod +x install_docker.sh`
    - `./install_docker.sh`
- Dodamo potrebne datoteke
- Povezava do baze:
    - `docker-compose exec db psql --username=firstapp --dbname=firstapp`
    - Podtakovne baze: `\l`
    - `\c firstapp`
    - `\dt`
    - `SELECT * FROM users;`

## Viri:
- [Dockerizing FastAPI with Postgres, Uvicorn, and Traefik](https://testdriven.io/blog/fastapi-docker-traefik/)
- [Developing a Single Page App with FastAPI and React](https://testdriven.io/blog/fastapi-react/)
- https://testdriven.io/blog/fastapi-crud/
- https://testdriven.io/blog/fastapi-jwt-auth/
- https://testdriven.io/blog/fastapi-graphql/
- https://testdriven.io/blog/fastapi-mongo/
- https://testdriven.io/blog/fastapi-streamlit/
- https://testdriven.io/blog/fastapi-and-celery/


- https://github.com/testdrivenio/fastapi-crud-async
- https://github.com/leon11s/python-napredni-public
- https://github.com/leon11s/plume-python-tecaj/blob/master/vsebina/napredni_tecaj/11_Creating_REST_APIs/tecaj_2020_02/src/app/api/auth.py
- https://git.ltfe.org/adahon/cyberlab-services/-/tree/master/app/api