+++
title = "The advice I took from loggingsucks.com"
date = 2026-04-25

[extra]
link = "https://loggingsucks.com/"

[taxonomies]
tags = ["web-dev", "performance"]
+++

[Logging Sucks](https://loggingsucks.com/) was a great actionable read on a better approach for application logging. The main idea is to log a *wide event* per request, instead of a typical approach of spamming dozens of individual log statements.

> The fundamental problem: logs are optimized for writing, not for querying.

Lately, I've been going through a bit of a performance kick after getting complaints for years on [my games](https://waldens.world/projects). I stumbled across the article looking for approaches on observability, and for some reason this one clicked for me.

So I put Boris's advice into practice. Since I'm going from essentially zero logs in this app, I wanted to start with logging all requests to my server. With some help from Codex, I created a custom nginx log format to start logging requests from my PHP app. Then I set up [axiom.co](https://axiom.co/) (on the free plan btw) to ingest the log stream in real time with [vector](https://vector.dev/). I genuinely got this working in under an hour. Following the wide event philosophy, I stuffed all the data nginx would give me about the request in the logs, including some app data like user account.

For the first time I became able to *query* my logs. Within minutes I already had surprising and actionable results. 

- Sort by average request time -> Wait that page is slow?
- Sort by request count -> Why is there so many requests for that script?

etc...

When I had worked on performance in the past I had more of a mindset of addressing a specific issue, so I'd do things like write code to find the runtime for a specific request and optimize on that. Having greater observability though can show you the part you thought was the bottle neck might not actually the be the problem at all.

The article goes a lot further than I'm able to do in my app for now. Here's some other useful data that they recommend collecting and questions you can answer:

- Enabled feature flags for the request -> Is the new feature improving performance?
- Deployment ID -> Which deployment caused a performance regression?
- Lifetime Customer Value -> Are high value customers having a good experience?
- Error Type/Message -> Not just "status code 500", but what caused the error

---

This post is the first part of a series I'll be doing on learnings of working on performance. The [last few months](/tags/book-review/) I've been in study-mode, and I've been itching to try out all of the new concepts I've been learning about. I'm thankful I have a real project with real users as well where this work has meaning. People have already been telling me they feel the performance uplift of the changes I've been making the last few weeks which has been awesome! Like I said this post is just about the observability part, and the next posts will be about changes I made after finding out my problem areas.
