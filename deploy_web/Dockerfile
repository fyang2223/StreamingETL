FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

EXPOSE 9696

COPY ["predict.py", "pipe.bin", "./"]
ENTRYPOINT [ "python", "predict.py" ]