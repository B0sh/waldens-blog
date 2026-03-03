+++
title = "Did coding help me learn Japanese?"
date = 2025-07-16

[taxonomies]
tags = ["highlights", "japanese"]
+++
I've been learning [Japanese](https://www.youtube.com/watch?v=0L-TcW2SuLQ) since 2020. 

As a programmer, it's difficult to resist the urge to try to use computers to solve my problems. And so I made many attempts to make my life learning a second language easier with programming. I had a lot of fun with these projects, but did they actually help?

Not really... 

<!-- It turns out you don't need to use a computer to learn Japanese. -->

The [grand debate](https://xkcd.com/1205/) here is whether you save time overall by making yourself more *efficient* by building a tool compared to simply doing the actual work. It's muddy though, since I think there is real value in experimenting. So let's take a tour through my language learning experiments and see how I did.

---


### Twitch Chat Character Frequency Analyzer

My first idea was simple: I wanted to be able to watch Twitch livestreams in Japanese, so wouldn't it be good to take that specific source materialーTwitch chatーand see what words were most common? Therefore increasing my comprehension optimially by studying the maximum value item first? Well, after several hours or so I did indeed create a working Python system to extract chat history from Twitch vods, and create a frequency list out of the most common Japanese characters.

Unfortunetly, I didn't end up meaningfully incorporating any of the lists I made into my studies. I was so new to Japanese that I wasn't quite clear yet on how the Japanese writing system worked. Reflecting on the project now, a frequency list on words, not characters, would've given me some more actionable information to work with, but since Japanese does not have spaces, doing that parsing is not trivial. After looking at the results of my project at the time, realizing why my findings weren't useful to me was part of understanding how Japanese worked.

### YouTube Screenshot Tampermonkey Script ([Github](https://github.com/B0sh/japanese-tools/blob/main/youtube-screenshot.js))

This is by far the most successful script I built, as I've actually used it thousands of times. It injects a "Screenshot" button on the YouTube player, which downloads a picture of the current frame from YouTube's `<video>` element. It started out as a fork from another script, but I needed to make a lot of changes and ended up basically rewriting the entire thing. I did easily 1,000 hours of Japanese YouTube in the last several years, so I got a ton of value here.

- The main purpose is to quickly add context images to my flash cards in [Anki](https://apps.ankiweb.net/#top). If I see a new word in a YouTube video, I'd go to make a flash card for that word, and then add the screenshot from the video. When I go review that word later, it helps me remember the context that I first saw the word, which aids in the recall process.
- The filename of the screenshot includes the youtube video ID & timestamp, so I can look in the metadata of my Anki card and cross reference the context in which I saw the word originally. I've done this enough times now that I'm happy I put this data in.
- I can also open the screenshot in Preview on my Mac and get access to Live Text OCR for Japanese. Kanji are very difficult to input on a computer if you don't already know the pronunciation, so OCR is incredibly powerful for new words.

Still though, while nice it's not required to learn Japanese in any way. All it accomplishes is making me a bit faster at making flash cards with pictures compared to manual `Cmd+Shift+4` screenshots.

![7,093 flash cards selected](https://static.waldenperry.com/2025/screenshot-count.png)
*I do have 7,093 flash cards with YouTube screenshots with this extension.*

### Minecraft Flash Card Deck ([Github](https://gist.github.com/B0sh/cf2fa108e7b6fbe210bd19dc724f8deb))

I watched a ton of [Japanese Minecraft content](https://www.youtube.com/watch?v=lemQ00ju-ns) while learning, and so I had an idea to try studying Minecraft itself to improve my listening comprehension in these videos. Since I already had a good bit of experience with Minecraft mods, I knew where I could find the game's translation files. So from there it was as simpleas writing a Python script to cross reference the English & Japanese translation files, downloading the assets, and using the `genanki` Python library to create the Anki flash cards. After filtering out some repetitive content, I ended up with a deck of about 1,000 Minecraft terms of various types.

Creating the deck worked, of course. But as for the theme of this post, this once again was not much help to learning Japanese. As I started reviewing the deck, I ran into tons of cards like pictured below, way too complicated for my Japanese level *plus* not even very  common in the game. That's the definition of low value study time. 

I got a big lesson from here about how important it is to study things just outside the range of your comprehension. For me, the entirety of this deck was words that I had already learned or were too difficult.

![flash card for the Waxed Cut Copper block from Minecraft](https://static.waldenperry.com/2025/minecraft.png)

### AI Conversation Partner ([Github](https://github.com/B0sh/language-trainer/tree/svelte-eel))

{{ video(src="https://static.waldenperry.com/2025/japanese-ai-convo-demo.mp4") }}

I wanted to practice speaking but frankly at this time I was too scared to go online and try to make conversations with real Japanese people for practice, so I decided to build an *AI conversation partner*. Stop me if you've heard this one before. (side note: I did end up making real Japanese friends)

The app uses Whisper in Japanese language mode to transcribe you. Then it takes the transcription and sends it to ChatGPT for a response, and back into audio with the browser `SpeechSynthesisUtterance` API. 

Latency and transcription accuracy are big killers here. Perhaps it's worse for me as a non-native, because I imagine the vast majority of Japanese audio trained on is from native speakers. Also keep in mind that this was July 2024, so perhaps a multimodal model solution would work better now. But ignoring all that, fundatmentally after like 10 minutes this thing just wasn't fun to talk with. After I finally got it working, I closed the project and never opened it again to practice.

### AI Language Trainer ([Github](https://github.com/B0sh/language-trainer))

{{ video(src="https://static.waldenperry.com/2025/language-trainer-demo.mp4") }}

Six months later I started over again on the conversation partner prototype and this time went for a "language trainer".

The app uses LLM integration to try to generate random sentences or stories for a few different challenge games, like picking numbers and dates out of a sentence. What ended up being generated was not nearly as "random" as I wanted. Once you listen to like 10 of the sentences it all starts to sound exactly the same. I realized it was going to take some serious prompt experimentation to get better results, and that's where I left the project.

It also has the conversation mode which is what the video demos, but instead of speaking into the microphone like my previous prototype, I opted for typing responses just to avoid the transcription issues. When you finish your conversation I feed the transcript back into the LLM again to ask for feedback on your input. I think I actually came up with a great UI for this interaction. However, as expected with LLMs, it gave me really bad "corrections" too often for me to want to actually use it.

Granted, I wanted to practice building a more polished UI with React and trying out LLM APIs equally as much, but I had genuinely hoped to get some language learning value out of this project that didn't materialize.

---

In the end, if you want to learn a skill, the best bet is to just actually go out and do it for real. Thankfully for me I did that too.
