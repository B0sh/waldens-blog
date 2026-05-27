+++
title = "oklch() CSS Color Space"
date = 2026-05-27

[extra]
link = "https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl"

[taxonomies]
tags = ["web-dev", "css"]
+++

I came across the `oklch()` CSS color space value today doing while looking into the [Trees](https://trees.software/) library. The [linked post](https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl) is a great explanation of what it is and what the point is. I've been using `hsl()` color space the last few years, but it turns out there's some drawbacks:

> HSL contains 3 numbers to encode hue, saturation, and lightness, like so: hsl(210 60% 64%). The main problem with HSL is that it has a cylindrical color space. Every hue has the same amount of saturation (0—100%). But in reality, our displays and eyes have different max saturations for different hues. HSL hides this complexity by deforming the color space and extending colors to have the same max values.

On the other hand:

> OKLCH doesn’t deform the space; it shows the real color space with all its complexity. On one hand, this feature allows us to have predictable lightness values after color transformations and P3 color definition. But, on other hand, not all number combinations in OKLCH generate visible colors: some are only visible on P3 monitors. But there’s still some good here: browsers will render the closest supported color.

To me the biggest benefit would be getting relative color transformations where the color space is aware of the specific hue being used. Going to try it out on my next design project!
