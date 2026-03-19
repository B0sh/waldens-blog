+++
title = "Help! My Postgres 18 Docker container won't save its data"
date = 2026-03-18

[taxonomies]
tags = ["docker", "postgres"]
+++

During my latest app development I've been having an issue where my Postgres Docker container loses all of its data whenever I run `docker compose down` or delete it another way. Data was fine on a `--rebuild` or running for days, so I was stumped for a while. 

It turns out this problem is related to a change in the location data is stored by default in Postgres 18+.
I had happened to be following an older tutorial and naively bumped up the version to latest. Going forward the default data storage location is at `/var/lib/postgresql/18/docker`.
There are [docs](https://github.com/docker-library/docs/blob/master/postgres/README.md#pgdata) here on `PGDATA`, and [discussion](https://github.com/docker-library/postgres/pull/1259) on the changes. For my small personal site situation I'm not going to be going fancy version based rollbacks so I just decided to set `PGDATA` environment variable manually. Perhaps not what Postgres recommends me to do, but that's ok with me.

Just for posterity here's what I ended up with:

```yaml dockerfile
services:
  db:
    image: postgres:18.1-alpine3.23
    restart: always
    ports:
      - 5432:5432
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=${POSTGRESQL_DATABASE}
      - POSTGRES_USER=${POSTGRESQL_USERNAME}
      - POSTGRES_PASSWORD=${POSTGRESQL_PASSWORD}
      # See: https://github.com/docker-library/docs/blob/master/postgres/README.md#pgdata
      - PGDATA=/var/lib/postgresql/data
      
volumes:
  db-data:
```
