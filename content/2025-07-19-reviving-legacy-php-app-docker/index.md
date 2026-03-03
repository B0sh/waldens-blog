+++
title = "How I revived my 15 year old PHP 5.x game with Docker"
date = 2025-07-19

[taxonomies]
tags = ["docker", "highlights"]
+++

While cleaning out the hard drives I stumbled upon a zip archive of my first major project, Nebula Wars. It's a PHP/MySQL web game from late 2010.

![Screenshot of Nebula Wars from January 5th, 2011](https://static.waldenperry.com/2025/Nebula_Wars_1-5-11.png)

The story behind this game is kinda wild. I got the source code to a Pokémon RPG, and without knowing much at all about programming set out to convert it into a Space-themed RPG when I was 13 years old. I didn't know JavaScript yet, so the actual gameplay can be boiled down to clicking around on this website. It's certainly of its era.

I thought it'd be a fun challenge to see how difficult it'd be to get this thing running in 2025.

### Let's go with Docker

Starting out, I realized this would be the perfect situation for Docker containers. Docker is difficult to explain, but it acts as a sort of virtual environment, so when I go to install an old PHP version, it won't be able to interact with the rest of the modern environment that's either on my Mac or potentially on a server somewhere. Since it's so old I figured it'd be difficult to setup the environment natively on my modern Mac.

As the screenshot peekers already noticed, I didn't actually do any local development in 2011. It was all FTP development in the browser with cPanel.[^1] As such there's no git history or really documentation of any kind with my code. I just have a zip file of the PHP source and a dump of the MySQL database.

The first step was figuring out what environment I was running. I checked [PHP's version history](https://en.wikipedia.org/wiki/PHP#Release_history) and it seems most likely I would've been running PHP 5.3 as I worked on the project late 2010 and into 2011. My MySQL dumps show me I was using 
`Server version 5.1.56`. Now we have something to work with.

I opted for a `docker-compose.yml` file. This lets me define both the PHP server and MySQL database in one file. First, the MySQL installation:

```yml
services:
  mysql:
    image: mysql/mysql-server:5.5
    environment:
      MYSQL_DATABASE: nw_nebulawars
      MYSQL_USER: nebulawars
      MYSQL_PASSWORD: testpass
    volumes:
      - mysql_data:/var/lib/mysql
      - ./sql:/docker-entrypoint-initdb.d:ro

volumes:
  mysql_data: {}
```

In 2025, the oldest MySQL that Docker is currently supporting is 5.5, so I couldn't match the 5.1 that I used. Thankfully, it worked out just fine. I have some experience with doing legacy MySQL migrations, and I know if I was going to go up to latest that I'd start running into a bunch of issues, so best to keep it as close as possible. 

A few things to note about the container config:

* `./sql:/docker-entrypoint-initdb.d:ro` is a magic folder that executes sql scripts. I moved my database create scripts into `./sql`, and let the container take care of the rest.
* Adding the `mysql_data` volume causes the database to be stored persistently, so when you stop & start the container it keeps the database.
* And of course `testpass` just to keep things moving.

You wouldn't do any of this for a production database, but the goal here is to get the app functional!


### PHP Container Setup

I added 2 more services for the web server:

```yml
services:
  php:
    build:
      context: .
      dockerfile: PHP.Dockerfile
    volumes:
      - ./app:/app
    depends_on:
      - mysql
  
  nginx:
    image: nginx:latest
    volumes:
      - ./app:/app
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    ports:
      - 80:80
    depends_on:
      - mysql
```

Like with MySQL, PHP 5.3 is too old to be supported by official Docker images any longer. The code in my app is so bad however, PHP 5.3 was pretty much a requirement. I found a community image [`helder/php-5.3`](https://hub.docker.com/r/helder/php-5.3) and just used that as the starting image for my Dockerfile. `./app` is where I stuck all of the PHP code and assets.

I added a `depends_on` to wait to start the web server until MySQL is finished loading. This would stop users from being able to make any web requests when the database is still initializing.

Finally, I setup a modern nginx image to handle the web server. I know I was using apache at the time, but considering I didn't even have an `.htaccess` file in my code, I wasn't actually taking advantage of any apache features. Might as well go with nginx here. Here is my `nginx.conf`:

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name _;
    server_tokens off;
    access_log off;

    root /app;
    index index.php;

    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass php:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;  
    }

    location / {
        try_files $uri $uri/ =404;
    }
}
```

You'll notice I skipped HTTPS setup. I wasn't using HTTPS in 2011, so it's more *authentic* this way. The `docker-compose.yml` file also has to explicitly expose port 80.



### Testing The App

Now it's time to turn it on.

```
docker compose up --build
```

Everything starts up, but quickly it's apparent there's a few issues to still be resolved.

At first I couldn't connect to the database. 

```
Warning: mysql_connect() [function.mysql-connect]: Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2) in /app/dbconf.php on line 8
```

*And, yes it's using the legendarily insecure `mysql_*` series of functions*

It turns out you need to update the database hostname from `localhost` to `mysql` for Docker. `localhost` is now pointing to a container that only has PHP installed, and since we separated out the database into a separate container, this needed to be adjusted in the code.

It was looking really good then, until I hit my captcha. It turns out I used the `Securimage` PHP library to generate captchas for the game, and it was relying on the `gd` PHP module to generate images. This provides various functions for creating images and rendering text.

```
Fatal error: Call to undefined function imagecreatetruecolor() in /app/cap55/securimage.php on line 478
```

I had to dig through old posts about getting the `gd` to work in PHP 5 to come up with this Dockerfile, but eventually I did get it working. Also, since the version of debian used in the image is no longer supported, I had to pull in the linux releases file from the archives. So I ended up at the end with this Dockerfile:

```Dockerfile
FROM helder/php-5.3

RUN echo "deb [trusted=yes] http://archive.debian.org/debian stretch main" > /etc/apt/sources.list

RUN apt-get update
RUN apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev
RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ 
RUN docker-php-ext-install gd    
```

### And now it works!

I was impressed I managed to get it running in just a few hours. I know I'm working on a toy project, but I demonstrated that it's still possible to revive a 15 year old PHP 5.3 application with Docker.

If this were a real production legacy application, getting to this point would be an excellent first step. From here, the next steps would involve:

* Setting up a production-ready MySQL server 
* Adding HTTPS support
* Implementing proper secrets management
* Most importantly, gradually bumping the PHP & MySQL versions. What would it take to get to PHP 7+?

In my case, I think I'm going to put this one back on the shelf for another decade.

[^1]: My maintenance strategy was to go in the chatroom and tell everyone not to use X page while I was working on it.