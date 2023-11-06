FROM python:3.9
WORKDIR /football_db
COPY . .
RUN pip install pipenv
RUN pipenv install
# CMD ["pipenv","run","python","scripts/app.py"]