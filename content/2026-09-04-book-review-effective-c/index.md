+++
title = "Robert C. Seacord: Effective C"
date = 2026-09-04

[taxonomies]
tags = ["book-review", "c"]
+++

![Effective C Book](https://static.waldenperry.com/2026/EffectiveC.png)

This month I read [Effective C, 2nd edition](https://nostarch.com/effective-c-2nd-edition) by Robert C. Seacord.

It's a modern introduction to C, up to date with the latest C23 standard.

## Who is this for?

It's kind of a difficult question to answer. The pitch for Effective C is that it teaches "C programming, without dumbing it down." I found that to be an apt description in my reading.

In theory, I think Effective C could be a great fit for people who are relatively new to programming, but there will be large parts of the text, especially towards the end, that will be inaccessible without background knowledge of computer science. After all, C is a systems programming language. This book isn't going to give you a deep dive into the workings of memory or assembly code, but gives you just enough to understand how to use the language. For more experienced programmers, it reads very easily, which let me focus on the parts of C that are different from what I'm used to in my typical cohort of JavaScript, C#, or PHP.

## How I Read

I went through the book chapter by chapter and took notes on things I thought were interesting. I also kept my code editor open on the side and, from time to time, made sample programs exploring the concepts from the book. (That repo is [here](https://github.com/B0sh/c-practice/tree/3e00726726c3bc0a9756d6d3f82a56f498fdaa6a), by the way.) I also asked [Chappie](/chappie) questions about C maybe 5-10 times throughout the book, but usually the answer I was looking for was on the next page or in a later chapter anyway! Playing around with the language and going down rabbit holes makes things stick a lot more than laying back and reading a book like this.

## The Content

*or what I found interesting*

I've long known that C has this thing called "undefined behavior" but it wasn't until this book that it really clicked for me. I had in mind that undefined behavior was like mistakes in language design that were made over decades ago that we have to deal with since we can't change legacy code. It turns out (and of course this is the case) that there are good reasons for undefined behavior in language design.

Take a look at this example:

```c
int add(int x, int y) {
    return x + y;
}
```

This simple example already can invoke undefined behavior, when large values of `x` or `y` overflow the output's `int`. That was shocking to me, as you'd expect adding numbers to be completely safe in any other language. Unsigned integers have defined wraparound on the other hand, so I've found myself reaching for them more often. Out of 11 chapters, there was a whole chapter dedicated to just number types, which shows how much there is to say on this topic.

But anyway, having undefined behavior has significant benefits for compiler optimizations. As C has [many different compilers](https://en.wikipedia.org/wiki/List_of_compilers#C_compilers), each can make implementation decisions around *defined* behavior depending on their supported hardware, since they can ignore undefined behavior. Effective C doesn't go into much detail about compiler internals so that will have to be another book.

---

The preprocessor is so archaic it's hilarious. `#include` directives essentially copy and paste the header file into your source code so that function declarations can be seen. And `#define` replaces one set of text in your code with something else. It's not hard to see how that can spiral out of control quickly.

Well, since `const int` defined variables aren't actually constant (because you can take a pointer and change its values indirectly), using `#define` for project wide constants seems to make sense to me. Other than that, I'd rather not touch these if I can help it.

---

As one would expect, dynamic memory allocation is covered in detail: `malloc`, `free`, etc. I haven't attempted to write any long lived processes just yet, but *unsafe* manual memory management seems easier than I thought. You can use `sizeof` to get the byte size of structs, or even built-ins like `sizeof(int)` as part of your calculations.

It was surprising to learn that many C standard library functions do not have built-in checks for buffer overflows. They expect you to provide safe values for whatever calculation you're performing. This is awesome for performance, but it's a departure from a more defensive style of coding where you validate your inputs on the function definition side.

---

In my minimal experience so far, perhaps the most frustrating thing is the lack of support for strings in C. C++ gives you `std::string` with a ton of functionality, but here we get an array of numbers (`char str[]`). If you need UTF-8 support, it's your problem. And expect to do a lot of memory allocation with strings, as you have to make sure you have the correct amount of bytes allocated in advance of creating a string.

## Next Steps

The book doesn't go into some topics I was interested in, like multithreading and SIMD. Having read this book, I have seen enough to explore those concepts with confidence on my own. I also want to explore writing some larger-scale projects.

## Conclusion

Exploring C for a few weeks with absolutely zero intent to create anything useful has been lovely! Just fun for the fun of it all. Despite its obvious rough spots, it's a beautiful language. My goals were to try something new and peek into how professional C programmers are using this language successfully. I consider that accomplished!
