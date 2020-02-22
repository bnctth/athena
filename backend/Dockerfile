###########
# BUILDER #
###########

FROM python:3.7.6-alpine as builder

# set work directory
WORKDIR /usr/src/athena

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update && apk add libressl-dev postgresql-dev libffi-dev gcc musl-dev python3-dev 
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/athena/wheels -r requirements.txt


#########
# FINAL #
#########

FROM python:3.7.6-alpine

# create directory for the app user
RUN mkdir -p /home/athena

# create the app user
RUN addgroup -S athena && adduser -S athena -G athena

# create the appropriate directories
ENV HOME=/home/athena
ENV ATHENA_HOME=/home/athena/web
RUN mkdir $ATHENA_HOME
RUN mkdir $ATHENA_HOME/static
WORKDIR $ATHENA_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/athena/wheels /wheels
COPY --from=builder /usr/src/athena/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $ATHENA_HOME

# copy project
COPY . $ATHENA_HOME

# chown all the files to the user athena
RUN chown -R athena:athena $ATHENA_HOME

# change to user athena
USER athena

# run entrypoint.sh
ENTRYPOINT ["/home/athena/web/entrypoint.sh"]
