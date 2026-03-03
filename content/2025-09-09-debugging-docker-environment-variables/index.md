+++
title = "Debugging Docker Compose Environment Variables"
date = 2025-09-09

[taxonomies]
tags = ["docker"]
+++

I was having issues with my Docker compose project not picking up environment variables, with the following error: 

```
b0sh@MacBook-Air-4 % sudo docker compose up
WARN[0000] The "LOG_DIRECTORY" variable is not set. Defaulting to a blank string. 
invalid spec: :/log: empty section between colons
```

The project's `docker-compose.yml` file looked something like the following, where an environment variable was controlling the location of a volume.

```yml
b0sh@MacBook-Air-4 % cat docker-compose.yml
services:
  mysql:
    image: mariadb:latest
    env_file:
      - variables.env
    volumes:
      - ${LOG_DIRECTORY}:/log
    ports:
      - 3306:3306
  ...
```

Even though (I thought) I had that variable in my environment variables it wasn't picking up for some reason.

I then found out about the [`docker compose config`](https://docs.docker.com/reference/cli/docker/compose/config/) command which was new to me and was very helpful for debugging. It prints your Docker compose file after all flags and variables are processed, as well as expanding out short form notations so that you can debug the config as Docker is seeing it. 

After manually setting the variable with `export LOG_DIRECTORY=/app/mysql/log` I was able to see all my project's environment variables expanded out and noticed it was indeed working.

```yml
b0sh@MacBook-Air-4 % docker compose config
services:
  mysql:
    image: mariadb:latest
    environment:
      LOG_DIRECTORY: /app/mysql/log
      MYSQL_DATABASE: migrations
      MYSQL_HOST: mysql
      MYSQL_PASSWORD: ***
      MYSQL_USER: ***
      NODE_ENV: development
    volumes:
      - type: bind
        source: /app/mysql/log
        target: /log
        bind:
          create_host_path: true
    ports:
      - mode: ingress
        target: 3306
        published: "3306"
        protocol: tcp
  ...
```

That's when I was able to realize that the issue was the `LOG_DIRECTORY` environment variable was in the project's `variables.env` file, not in a `.env` file. Docker wasn't looking at the non standard env file name. The actual project has a very complicated environment variable management system which I simplified here, so I got all bent out of shape and overlooked this simple fact.

I created a new `.env` file with the `LOG_DIRECTORY` variable and everything magically started working.

The `docker compose config` command was critical to unwinding this mess and I'm really happy to have this added to my toolkit working with Docker.

Additionally, when I had tried to run an `export LOG_DIRECTORY=/app/mysql/log` to test, at first I was running the config command without sudo, but running `sudo docker compose up` was triggering the environment variable not found error. Of course, that won't set the bash variable for the root user, triggering the error. I didn't notice this for a while, so if you run your Docker with sudo, also run the config command with sudo as well to get more accurate results.
