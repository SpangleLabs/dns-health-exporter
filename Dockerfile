FROM python:3.10.2-alpine3.15
MAINTAINER Joshua Coales <joshua@coales.co.uk>

# Poetry needs this
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
     && pip install cython \
     && apk del .build-deps gcc musl-dev

RUN adduser -D dns_check
USER dns_check

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

COPY . /app
EXPOSE 8080

ENTRYPOINT ["python", "main.py"]
# HEALTHCHECK --timeout=10s CMD wget --no-verbose --tries=1 --spider http://localhost:8080/