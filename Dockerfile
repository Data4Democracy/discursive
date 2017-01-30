FROM alpine:latest

RUN mkdir discursive

COPY . /discursive

RUN apk add --update \
    tini \
    python \
    py2-pip && \
    adduser -D aws

WORKDIR /home/aws

RUN mkdir aws && \
    pip install --upgrade pip && \
    pip install awscli && \
    pip install -q --upgrade pip && \
    pip install -q --upgrade setuptools && \
    pip install -q -r /discursive/requirements.txt && \
    crontab /discursive/crontab

CMD ["/sbin/tini", "--", "crond", "-f"]
