FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir -r /code/requirements.txt

COPY ./Notebooks /code/Notebooks
COPY ./recsysMicroservice /code/recsysMicroservice
COPY ./Models /code/Models

CMD ["hypercorn", "recsysMicroservice.App:app"]
