FROM python:3.7-alpine

ENV BRANCH master

RUN apk --update add \
    curl \
    bash \
    gcc \
    git \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    python3-dev \
    libjpeg \
    sudo \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev tcl-dev \
    openssl \
 && cd \
 && git clone -b $BRANCH https://github.com/raspberry-jam-jar/english-blabber-server.git \
 && cd english-blabber-server \
 && pip3 install --upgrade pip setuptools \
 && pip3 install -r requirements.txt \
 && curl -O https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
 && chmod +x wait-for-it.sh \
 # Cleanup
 && apk del \
    curl \
    gcc \
    git \
 && rm -rf /var/cache/apk/*

COPY ./docker-entrypoint.sh /usr/bin/docker-entrypoint.sh
COPY ./django_create_superuser.py /usr/bin/django_create_superuser.py

RUN chmod +x /usr/bin/docker-entrypoint.sh \
&& chmod +x /usr/bin/django_create_superuser.py

WORKDIR /root/english-blabber-server/

ENTRYPOINT ["docker-entrypoint.sh"]
