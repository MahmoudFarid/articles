FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN groupadd -r django && useradd -r -g django django

# Install postgis requirements
RUN apt-get update -y && \
    apt-get install -y binutils libproj-dev gdal-bin python-gdal && \
    rm -rf /var/lib/apt/lists/*

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/django/gunicorn.sh ./compose/django/entrypoint.sh /

RUN sed -i 's/\r//' /entrypoint.sh && \
    sed -i 's/\r//' /gunicorn.sh && \
    chmod +x /entrypoint.sh && chown django /entrypoint.sh && \
    chmod +x /gunicorn.sh && chown django /gunicorn.sh

COPY . /app
RUN chown -R django /app

ENV DJANGO_SETTINGS_MODULE=config.settings.production


WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
