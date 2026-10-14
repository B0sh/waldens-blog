+++
title = "Deleting Fake Google"
date = 2026-10-13

[taxonomies]
tags = ["mac", "malware", "self-repair"]

[extra]
pangram = ""
+++

I was doing a few checks after replacing my friend's [MacBook's battery](/macbook-pro-2015-battery-replacement), and was concerned about searching in Chrome. 

Every search I did in the Chrome address bar had this oddly long delay before getting redirected to Bing of all things (he said he doesn't remember picking Bing - another clue). At first I thought maybe this 2015 Macbook really is that slow, but I tried some other websites and they worked much faster.

My next hypothesis was there was some malware extension that's harvesting searches. I wasn't too far off, because I found this in the search engine settings screen:

![Chrome's settings screen with showing "google", not "google.com"](https://static.waldenperry.com/2026/chrome-fake-google-1.png)

Yep, that's very suspicious. 

![Editing the suspicious "google" search engine reveals a different URL](https://static.waldenperry.com/2026/chrome-fake-google-2.png)

And of course clicking into to edit "google" reveals that it's actually going to some data harvesting platform. I didn't see any strange apps in Mac login items and there's no extensions installed, so perhaps he downloaded something a while ago and ended up deleting it. Replacing the entry with google.com is the fix here.

It feels like this shouldn't be possible... but at the same time I use the [Kagi Chrome extension](https://help.kagi.com/kagi/getting-started/setting-default/chromium-desktop.html) and the job I want it to is literally replace my search.
