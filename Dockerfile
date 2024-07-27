FROM python:3.9.19-slim-bookworm

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app/app

ENV PYTHONPATH=":/app"

ENTRYPOINT ["python", "app/main.py"]

EXPOSE ${APP_RUNNING_PORT}
