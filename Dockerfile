FROM python:3.9
WORKDIR /football_db
COPY ./Pipfile Pipfile
RUN pip install pipenv
RUN pipenv install
COPY ./scripts scripts
CMD ["pipenv","run","python","scripts/app.py"]