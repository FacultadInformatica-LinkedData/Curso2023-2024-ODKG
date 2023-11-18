FROM python:3.10-slim
ENV APP_HOME /code
WORKDIR $APP_HOME
COPY . ${APP_HOME}
RUN apt-get update \
    && apt-get install -y libpq-dev build-essential
RUN pip install --upgrade pip wheel setuptools
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
CMD exec gunicorn --config ./gunicorn.conf.py
