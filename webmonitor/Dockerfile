FROM public.ecr.aws/docker/library/python:3.11

WORKDIR /code

ENV PYTHONPATH=/code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org --no-cache-dir --upgrade -r /code/requirements.txt

# In order to run psql command (to check db is up) in web container
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Copy source code
COPY ./src /code/src

# Copy tests
COPY ./tests /code/tests

# We don't need this file in the container, but for demo purposes we'll keep it
# Copy .isort.cfg and .flake8
COPY ./.isort.cfg /code/.isort.cfg
COPY ./.flake8 /code/.flake8

# Copy prestart.sh and run.sh
COPY ./prestart.sh /code/prestart.sh
COPY ./run.sh /code/run.sh

# Run the application
CMD ["./run.sh"]
