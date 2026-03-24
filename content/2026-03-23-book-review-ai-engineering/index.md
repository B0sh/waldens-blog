+++
title = "Chip Huyen: AI Engineering"
date = 2026-03-23

[taxonomies]
tags = ["book-review", "ai"]
+++

![AI engineering book](https://static.waldenperry.com/2026/ai-engineering.jpeg)

This week I read Chip Huyen's [AI Engineering](https://github.com/chiphuyen/aie-book). I came to this book as someone who had been interested in LLMs for several years now, but had never done any formal study.

I really liked how practical it was about specifically *using* foundation models.  The book reads like a comprehensive guide to the entire lifecycle of an AI feature. The early chapters cover ML basics and model selection, then prompting and system design, and finally into collecting feedback after deployment for future training data.

The publish date was Dec. 2024, so the fact that the book focuses on concepts rather than code or specific model usage was actually a plus for me. Models got *a lot* better over last year, but the teachings here are best practices that won't go away even if we get another 10x boost in model intelligence.

Hands down, the biggest practical win was Chapters 3 and 4 on evaluation. Creating an evaluation pipeline gives a cornerstone to an AI initiative. It aids development, since while iterating on model selection, prompts, context, or even the code that glues it all together, you can see whether your changes are making an objective difference. In production, you can see whether real usage is matching expectations.

My mind changed on the "AI as a judge" concept while reading this book. When it comes to directly giving test grades in school or determining court cases, the technology is clearly fraught, in my opinion. In certain constrained situations, though, I became convinced that it's a useful framework, especially when it comes to evaluation. For example, right after generating some output, you can use an AI to immediately judge that output as part of the generation pipeline for things like factual correctness or *brand values*, though of course at a cost in latency. Still, fundamentally AI can't be accountable to anything, so I continue to hold reservations here.

Huyen puts it well:

> An AI judge is not just a model - it's a system that includes both a model and a prompt. Altering the model, the prompt, or the model's sampling parameters results in a different judge.

If I had to say where I was most lost, it was in the chapter on finetuning. That chapter was quite math heavy in general, which didn't help my understanding either. I get that the main idea is that finetuning is good for shaping the output of a model more precisely, but despite a whole section being dedicated to pros and cons, I still don't feel like I understand why in practice I should choose finetuning over doing more prompt engineering. Perhaps I'll know it when I see it.

That's not to say all the math was bad. Chapter 9 on inference optimization was [very cool](/til-speculative-decoding/)! Although I don't expect much of that knowledge to be practically useful to me.

Overall, it was a informative read, packed with practical advice on AI usage. As I continue to integrate these skills into my tool belt as a software engineer, I think I'm going to be pulling this book off the shelf for reference many times in the future.
