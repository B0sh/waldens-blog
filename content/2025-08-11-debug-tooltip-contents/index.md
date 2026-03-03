+++
title = "Debugging The Contents of a Mouseover Tooltip"
date = 2025-08-11

[taxonomies]
tags = ["web-dev"]
+++

If you're working with a tooltip on mouseover, it's quite difficult to use the developer console. As soon as you go to actually interact with the dev tools with your mouse, by definition you're no longer hovering over the element you're trying to inspect! I just ran into this situation at work again, so I wanted to share the trick I picked up for this exact problem.

In Chrome DevTools, navigate to the **Sources** tab, and look at the **right side panel**. Expand **Event Listener Breakpoints** > **Keyboard** > activate the **keydown** event.

I think about this like having the ability to *freeze* the page at will with a keypress. So for tooltips, I'll first hover my mouse over the tooltip I want to debug, then press a key to trigger the breakpoint. You can then go to the HTML inspector and examine the layout & CSS at that moment. I've used this for debugging all kinds of things like mid-drag layout issues with a Kanban style card component. It's great for any temporary UI involving mouse events.
