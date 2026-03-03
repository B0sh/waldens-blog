+++
title = "Material Icon's FOUT Problem"
date = 2025-12-11

[taxonomies]
tags = ["css"]
+++
![](https://static.waldenperry.com/2025/material-icon-flash.jpg)

*This doesn't look right...*

Hey, an issue I've actually worked on before encountered in my real life! After a quick view source, sure enough, this website is using Google's [Material Icons](https://fonts.google.com/icons?selected=Material+Icons+Outlined) font. This is a web font that functionally works as an icon pack, similar to [Microsoft Wingdings](https://en.wikipedia.org/wiki/Wingdings). The way it works is if you want to render the home icon, you write the word `home` and the font itself will render that sequence of characters as a home icon.

```html
<span class="material-icons-outlined">home</span>
```

That's great and all, but what is the browser supposed to do if the font hasn't loaded yet? This is where the layout issue from the screenshot comes from. Before the material icons font is loaded, `home` is rendered with the browser's default font. You can see that in the screenshot with `notifications_off` and `search`.

This problem has a name: **Flash of Unstyled Text** (FOUT).

At my job we made extensive usage of Material Icons in our web apps so I've looked at many different proposed solutions to this problem before but everything comes up short.

### Font Loading Settings

In [Google's font best practice guide](https://web.dev/articles/font-best-practices#font_rendering) they say the following about how to think about font loading:

>  When faced with a web font that has not yet loaded, the browser is faced with a dilemma: should it hold off on rendering text until the web font has arrived? Or should it render the text in a fallback font until the web font arrives?
> 
> ...
> 
> `font-display` informs the browser how it should proceed with text rendering when the associated web font has not loaded. It's defined per font-face.
> There are five possible values for `font-display`:
> | Value    | Block period        | Swap period          |
> |----------|--------------------|--------------------|
> | Auto     | Varies by browser   | Varies by browser   |
> | Block    | 2-3 seconds        | Infinite           |
> | Swap     | 0ms                | Infinite           |
> | Fallback | 100ms              | 3 seconds          |
> | Optional | 100ms              | None               |

That screenshotted website is already using the `font-display: block` for the Material Icon font, but as demonstrated by my slow network conditions, 3 seconds wasn't enough here and I still saw the FOUT. There just isn't any way to *force* the browser to wait indefinitely until a font is downloaded before rendering. Browser authors could've done that, but it's intentionally limited to help users with slow connections see content.

Once the font is cached though, on subsequent page loads you don't see the behavior since the font is already loaded. So the FOUT on fonts is limited to first page loads typically.

### Faster Downloads

Another [optimization](https://developers.google.com/fonts/docs/material_symbols#static_font_with_google_fonts) is to attack it from the file size end and shrink your payload by only sending the icons that are actually used in your app. Like the following:

`<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght@100&icon_names=favorite,home,settings" rel="stylesheet" />`

From there you could download the font file it generates and add it to your app to self host your font. (Also generally a good idea so you won't be sending Google any extra referral data...)

While this does vastly cut down on the font's file size, thereby decreasing average load times, there's always a slower connection that could still see the flash. 


### What about code points?

If you don't like the layout-breaking long flash of a word like `home`, you can flash a &#xe5d2; instead. On the [Material Icons page](https://fonts.google.com/icons?icon.size=24&icon.color=%23e3e3e3) there's a unicode code point for each icon. Render that specific character with `&#x****;` and the chosen icon will render.

```html
<span class="material-icons-outlined">&#xe5d2;</span>
```

This mitigates the content flow issue since an entire word won't be rendered, which is good I guess, but you get this wierd box character instead. At best this idea is a sidegrade.


### JavaScript Font Loading Detection

If you can use JavaScript to detect when a font is loaded, then you would be able to programmatically add CSS rules or classes based on the state of loading.

The [FontFace API](https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/load) can load fonts and give a callback when the font is finished loading.

I'm positive this works, but it's a lot of complexity to add plus you have to juggle styling for icon loading before and after. For anyone looking for a permanent solution to FOUT, I'd spend my time here.


## Don't give yourself this problem

For our apps, we didn't have `font-display: block` enabled yet, so that was an easy win that took the flash from happening essentially every non-cached page load to only for slow connections. Unfortunetly, since we had a system where we could swap icons at runtime, I was unable to implement the static font optimizations.

What I *wanted* to do though was not use a web font at all. Google has SVG icons available for download of every material icon, and you can simply download add them to your app from there. It's annoying to manage a lot of images, sure, but so is the issues that come from font icons. I think many people are still choosing the Material Icon font without giving a lot of thought to SVGs because Google has a lot of documentation about the fonts out there already, but I hope this post will convince some people to not worry about this and use SVGs instead.
