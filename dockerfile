### stage 1: compile
FROM python:3.11-slim as pre-build

WORKDIR /src/

RUN python -m venv /venv
ENV PATH=/venv/bin:$PATH
COPY requirements.txt .
COPY setup.py .
COPY pipelines pipelines
RUN pip install .

### stage 2: copy source
FROM python:3.11-slim

WORKDIR /src/

#copying python binaries
COPY --from=pre-build /venv /venv
ENV PATH=/venv/bin:$PATH

#Unittest
COPY pipelines pipelines
RUN python -m unittest pipelines/translate/test.py
