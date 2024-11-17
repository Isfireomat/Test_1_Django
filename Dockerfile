FROM python:3.12.5-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    procps \
    && rm -rf /var/lib/apt/lists/* 
    
RUN pip install poetry 

COPY poetry.lock pyproject.toml ./

RUN poetry install

WORKDIR /app

COPY TestedProject1 .     

EXPOSE 8000

RUN useradd -m -u 50 celeryuser

CMD poetry run gunicorn --reload -c gunicorn.conf.py core.wsgi:application
