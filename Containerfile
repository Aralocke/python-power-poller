FROM python:3.12-alpine

COPY ["requirements.txt", "cli.py", "/srv/"]
COPY ["commands/", "/srv/commands/"]
COPY ["tplink/", "/srv/tplink/"]

RUN set -ex; \
    apk update; \
    apk add --no-cache git; \
    \
    python3 -m pip install -r /srv/requirements.txt; \
    adduser --home=/srv --shell=/bin/false \
        --disabled-password --no-create-home monitor; \
    chmod 640 -R /srv/**.py /srv/*.txt; \
    chown monitor:monitor -R /srv/commands /srv/tplink /srv/cli.py; \
    \
    rm -rf /var/cache/apk/*;

USER monitor
WORKDIR /srv

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "/srv/cli.py"]
CMD ["run", "-o", "--loglevel=INFO", "/etc/monitor.conf"]
