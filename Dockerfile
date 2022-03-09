FROM python:3.8-alpine
MAINTAINER Joshua Coales <joshua@coales.co.uk>

RUN apk add --update curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:$HOME/.local/bin

RUN poetry install

COPY . .
EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
# HEALTHCHECK --timeout=10s CMD wget --no-verbose --tries=1 --spider http://localhost:8080/
