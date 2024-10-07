FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./Notebooks /code/Notebooks
COPY ./recsysMicroservice /code/recsysMicroservice
COPY ./Models /code/Models

CMD ["uvicorn", "recsysMicroservice.App:app", "--reload", "--log-level", "debug"]
