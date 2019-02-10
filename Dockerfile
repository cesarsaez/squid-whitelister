FROM python:3.6.6

ENV PYTHONPATH /opt/myapp/
WORKDIR $PYTHONPATH
EXPOSE 3000:3000

RUN pip install pipenv

COPY Pipfile* $PYTHONPATH
RUN pipenv install --dev

COPY . .

CMD ["pipenv", "run", "python", "ops/run.py"]
