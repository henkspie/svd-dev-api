FROM python:3.12-alpine3.19
LABEL maintainer="Henk Spierings"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /temp/requirements
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .temp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /temp/requirements/development.txt; \
    else  \
        /py/bin/pip install -r /temp/requirements/production.txt; \
    fi && \
    rm -rf /temp && \
    apk del .temp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
    # mkdir -p /vol/web/media && \
    # mkdir -p /vol/web/static && \
    # chown -R django-user:django-user /vol && \
    # chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user
