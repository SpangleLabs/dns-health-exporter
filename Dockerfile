FROM python:3.8

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY . .
RUN poetry install
EXPOSE 8080

ENTRYPOINT ["poetry", "run", "python", "main.py"]
# HEALTHCHECK --timeout=10s CMD wget --no-verbose --tries=1 --spider http://localhost:8080/
