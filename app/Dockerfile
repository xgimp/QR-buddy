# syntax=docker/dockerfile:1


ARG PYTHON_VERSION=3.12


FROM docker.io/python:${PYTHON_VERSION}-alpine as build-stage
ARG BUILD_ENVIRONMENT

COPY /app/requirements/base.txt /base.txt
COPY /app/requirements/${BUILD_ENVIRONMENT}.txt /requirements.txt

# Install deps for requirements
RUN apk add gcc musl-dev libffi-dev

# Create Python Dependency and Sub-Dependency Wheels.
RUN python -m pip wheel \
      --no-cache-dir \
      --disable-pip-version-check \
      --wheel-dir \
      /usr/src/app/wheels -r requirements.txt

FROM docker.io/python:${PYTHON_VERSION}-alpine as run-stage
# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app
WORKDIR $APP_HOME

# Install dependencies for psycopg2 and Pillow
#RUN apk add --no-cache libgcc libjpeg libwebp libpq

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=build-stage /usr/src/app/wheels /wheels/

# use wheels to install python dependencies
RUN pip install \
          --disable-pip-version-check \
          --no-index \
          --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

COPY /app $APP_HOME

# create directories for media and static files
RUN mkdir -p $APP_HOME/static/ $APP_HOME/media/

# chown all the files to the app user
RUN chown -R appuser:appuser ${APP_HOME}

# Switch to the non-privileged user to run the application.
USER appuser
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["sh", "./entrypoint.sh"]
