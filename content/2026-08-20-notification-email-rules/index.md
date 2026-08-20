+++
title = "Can I Have Email Rules For Nofications Please"
date = 2026-08-20
+++

From time to time I need (or let's be honest, want) to have notifications for only on specific part of an app, but along with that I'm forced to get their marketing notifications too. 

Apps are supposed to have options to toggle marketing notifications off, and to be fair a lot of apps do. But this is pretty much Apple just asking nicely given the scope of the App Store. There's so [many options](https://support.apple.com/guide/iphone/change-notification-settings-iph7c3d96bab/ios) on iOS notifications, and now AI summaries too. Yet there's no simple text filter. And I can't make an app to do that either of course. I do completely understand why 3rd party apps can't have access to arbitrary notifications text, but I'm the 1st party of my own phone! 

From a technical level I think the best think I could hope for here from Apple is something similar to the [Manifest v3 filter mode](https://developer.chrome.com/blog/improvements-to-content-filtering-in-manifest-v3), where extensions can add specific filter rules but don't get to run arbitrary code against notifications. Funnily enough that'd be a breath of fresh air on iOS notifications, whereas on browser ad blocking it's a step backwards from the functionality we had before.

I tried to look up if this was possible on macOS notification center too since at least macOS is more open, and it seems like those APIs are quarantined off unless you turn off system integrity protection. Oh well, with coding agents that's a non starter now day.
