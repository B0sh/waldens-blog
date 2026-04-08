+++
title = "The Smallest Float"
date = 2026-04-08
+++

I was looking into how quantization in AI development works, but instead got sucked into a rabbit hole about floats. Since machine learning processes use so much floating point calculations, shrinking the number of bits required has a massive impact on the amount of calculations and memory required.

4 bits is so small you can easily make a table of all the values, there's only 16! The first bit (left) is the sign, then 2 bits are for exponent, and the last bit is the fraction.

|      | `.000` | `.001` | `.010` | `.011` | `.100` | `.101` | `.110` | `.111` |
|------|--------|--------|--------|--------|--------|--------|--------|--------|
| `0...` | `0` | `0.5` | `1` | `1.5` | `2` | `3` | `Inf` | `NaN` |
| `1...` | `-0` | `-0.5` | `-1` | `-1.5` | `-2` | `-3` | `-Inf` | `NaN` |

*Source: [Wikipedia](https://en.wikipedia.org/wiki/Minifloat#4-bit_(1.2.1))*

You can go all the way down to 2 bits, which removes the sign bit and leaves just the four values of 1, 0, Inf, and NaN. I had heard that Apple was using some 2 bit quantization for their foundation model, but I hadn't considered what that looked like in practice until now.

It's amazing that with just these values you can do anything useful.

The smallest possible 1 bit float might actually be useless though:

> Removing the mantissa would allow only two values: 0 and Inf. Removing the exponent does not work, the above formulae produce 0 and sqrt(2)/2. The exponent must be at least 1 bit or else it no longer makes sense as a float (it would just be a signed number).

*Source: [Wikipedia](https://en.wikipedia.org/wiki/Minifloat#1-bit_(0.1.0))*

---

Extra trivia: even with [more common floats](https://en.wikipedia.org/wiki/IEEE_754) like 8, 16, or 32 bits, there are different formats you can use to vary the exponent and fraction portions. Like [bfloat16](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format) which intentionally keeps the same 8 bit exponent as the standard F32 to facilitate fast conversion.
