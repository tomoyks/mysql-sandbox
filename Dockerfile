FROM mysql:8.0

WORKDIR /tmp
RUN apt-get update && apt-get install -y wget unzip
RUN wget 'http://downloads.mysql.com/docs/sakila-db.zip' && unzip sakila-db.zip && ls -la

RUN cp sakila-db/sakila-schema.sql /docker-entrypoint-initdb.d/00_sakila-schema.sql && \
    cp sakila-db/sakila-data.sql /docker-entrypoint-initdb.d/01_sakila-data.sql && \
    cp sakila-db/sakila.mwb /docker-entrypoint-initdb.d/sakila.mwb