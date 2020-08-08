FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install pipenv

ENV PROJECT_DIR /app
WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy --ignore-pipfile

COPY ./app /app/${PROJECT_DIR}