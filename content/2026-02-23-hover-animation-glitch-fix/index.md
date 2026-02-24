+++
title = "Fixing Animation Glitching with a CSS Hover"
date = 2026-02-23
+++

Animation issues are quite tricky to give a name to...

Just take a look at this video of my [website](https://waldens.world/):

{{ video(src="https://static.waldenperry.com/2026/waldens-world-index-issue.mp4") }}

The effect is when you hover over the rotated text, it *turns* into a link by removing the rotation and `text-decoration: underline` style. I also apply a bit of scaling `transform: scale(1.05)` to make it pop. However, the problem is if you hover at a specific spot, the text jumps around back and forth between the start and end positions of the animation. Yet most positions run the animation completely fine?

## Why is that?

It turns out the culprit lies in bounding boxes. If you consider the bounding boxes of the start and end of the animations respectively, they do not overlap completely. After the `transform: rotate()` applies, the bounding box sticks out on the edges a bit. Hovering over one of those spots will of course be detected by CSS `:hover`, but once the animation begins to apply, your cursor no longer is inside the bounding box of the element, and it removes the `:hover` state.

You can see this clearer in my video when I add a border to show the bounding box of the links.

## How to fix it?

My solution was to move the rotation animation to a child element. The parent element with some added padding now becomes a hitbox for the hover animation. With the selector `.parent:hover .child` you can trigger the rotate animation on hover of the parent element. Since the parent element fully covers both the start and end bounding boxes, the animation never resets itself. Take a look at the two bounding boxes in the fixed version below:

{{ video(src="https://static.waldenperry.com/2026/waldens-world-index-fix.mp4") }}

Here's a simplified version of the CSS I used. I had to manually adjust the padding until it was just right. 

```css
.splash-link {
    padding: 10px; /* adjust to fill rotated hitbox */
    transform: scale(1.0);
    transition: transform 0.2s;
    .text {
        transition: transform 0.2s;
        transform: rotate(-5deg);
    }
}

.splash-link:hover {
    transform: scale(1.05);
    .text {
        transform: rotate(0);
    }
}
```

```html
<a href="/videos" class="splash-link">
    <div class="text">Videos</div>
</a>
```

[Try it out!](https://waldens.world/)

As an aside, trying to have LLMs do this visual fix was totally worthless! I tried GPT 5.2 Codex and Claude Opus 4.5. Neither one could do it.
