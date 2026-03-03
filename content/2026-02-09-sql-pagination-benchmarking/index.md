+++
title = "SQL Pagination Benchmarking"
date = 2026-02-09

[extra]
link = "https://github.com/B0sh/investigations/tree/main/sql-pagination"

[taxonomies]
tags = ["sql"]
+++
I'm trying to be better about practicing strong software engineering fundamentals. One such fundamental is benchmarking. Something I know I could do, but instead I often end up designing reactively, where I guess what the best approach is and revisit it if I have problems. I was faced recently at work with a common pagination problem, and I went along and used my typical `OFFSET` approach just to move on to the next ticket. But! I kept thinking about pagination.

You see, I've recently had to learn about DynamoDB for my current project at work (which I intend to write a post about soon), and it's requirement cursor based model for pagination. I was interested in if that method could apply to MySQL too, and it turns out it does! It turns out that `OFFSET` can perform very poorly on large offsets, since it will have to scan through all records up to the offset to find where the results start. I could go into more detail but honestly you're better off reading [this great explanation](https://mysql.rjweb.org/doc.php/pagination) from Rick James that I referenced.

It's one thing to about read it, but I want to be better about seeing reality with my own eyes and test the claims for myself. I gave Codex a prompt to create the tests for me:

```
I want to investigate the claims in this article and investigate them for myself: https://mysql.rjweb.org/doc.php/pagination  

Create a mariadb database with docker compose and a example table with a million records of random data (Use RAND())

Then write simple scripts to check the performance of the methods in the article
```

That got me most of the way there, but I had to do a bit more back and forth to get the exact queries and benchmarking harness correct. (At first it was counting the time outside of Docker too) Eventually I ended up with [this benchmark](https://github.com/B0sh/investigations/tree/main/sql-pagination):

```
b0sh@MacBook-Air-4 sql-pagination % ./scripts/bench.sh
offset	method	seconds
0	Limit Offset Method	0.019s
0	Late Lookup Method	0.018s
0	Cursor Pagination	0.019s

100000	Limit Offset Method	0.035s
100000	Late Lookup Method	0.022s
100000	Cursor Pagination	0.018s

500000	Limit Offset Method	0.086s
500000	Late Lookup Method	0.042s
500000	Cursor Pagination	0.018s

999000	Limit Offset Method	0.124s
999000	Late Lookup Method	0.086s
999000	Cursor Pagination	0.018s
```

 I was able to see the `OFFSET` query gets slower and slower as the offset increases, while Cursor Pagination is able to stay consistent, leveraging the indexes in the database. Cool!
