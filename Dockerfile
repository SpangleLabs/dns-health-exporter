FROM python:3.8-alpine
MAINTAINER Joshua Coales <joshua@coales.co.uk>

RUN adduser -D dns_check
USER dns_check

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

COPY . /app
EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
# HEALTHCHECK --timeout=10s CMD wget --no-verbose --tries=1 --spider http://localhost:8080/