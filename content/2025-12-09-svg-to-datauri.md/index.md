+++
title = "Nice tool: SVG to Data URI Converter"
date = 2025-12-09

[extra]
link = "https://www.svgviewer.dev/"
+++

Documenting this tool I found to convert SVGs to data URI `data:image/svg+xml;base64,***` called [svgviewer.dev](https://www.svgviewer.dev/). I actualy almost went to vibe coding first, but then sure enough a great tool was already out there.

And another cool thing I learned from this website is data URIs aren't limiting to base64 encoding. You can just paste the raw SVG directly into a data URI in a pinch.

```html
HTML:
<img src='data:image/svg+xml;utf8,<svg>...</svg>'>
    
CSS:
.bg {
    background: url('data:image/svg+xml;utf8,<svg>...</svg>');
}
```
