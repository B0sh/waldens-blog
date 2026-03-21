+++
title = "TIL: Speculative Decoding"
date = 2026-03-20

[extra]
link = "https://research.google/blog/looking-back-at-speculative-decoding/"

[taxonomies]
tags = ["til", "ai"]
+++


Learned about the concept of **Speculative Decoding** for optimizing LLM interference. The idea is that you can use a weaker (faster) LLM to generate the next set of tokens, but then have the real model validate those tokens. If the weaker model missed, it will have to correct itself. You'd think this would add a lot of overhead, but it turns out in practice that a lot of tokens are predictable and so you can get away with this approach.

I found it interesting how similar this is to something like CPU branch prediction.

{{ video(src="https://storage.googleapis.com/gweb-research2023-media/media/SpeculativeDecoding-1-Illustration.mp4") }}

*Source: Google [https://research.google/blog/looking-back-at-speculative-decoding/](https://research.google/blog/looking-back-at-speculative-decoding/)*
