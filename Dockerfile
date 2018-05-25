# FROM python:3.6.5-alpine3.7 as base

# FROM base as builder
# RUN mkdir /install
# WORKDIR /install
# COPY requirements.txt /requirements.txt
# RUN pip install --install-option="--prefix=/install" -r /requirements.txt

# FROM base
# RUN apk add --no-cache  uwsgi-python3 
# COPY --from=builder /install /usr/local
# COPY . /app
# WORKDIR /app
# CMD ["ls", "/app"]

FROM  alpine:3.7 as base
RUN apk add --no-cache ca-certificates uwsgi-python3 \
        && pip3  install --upgrade --no-cache-dir pip \
        && rm -rf ~/.cache

FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr
COPY /src /app
WORKDIR /app
CMD ["uwsgi", "--http-socket", ":8080", "--manage-script-name", "--mount", "/app=run:app", "--plugin=python3", "--processes=4", "--threads=2"]



# FROM python:3.6-slim as base

# FROM base as builder
# RUN mkdir /install
# WORKDIR /install
# COPY requirements.txt /requirements.txt
# RUN pip install --install-option="--prefix=/install" -r /requirements.txt

# FROM base
# COPY --from=builder /install /usr/local
# COPY . /app
# WORKDIR /app
# CMD ["ls", "/app"]
