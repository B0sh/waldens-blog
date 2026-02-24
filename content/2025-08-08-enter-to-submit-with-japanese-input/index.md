+++
title = "The Problem with 'Enter to Submit' and Japanese Input"
date = 2025-08-08
+++


A common UI pattern these days is to have an "Enter to Submit" text box. Good implementations might even give you `Shift + Enter` to add a new line if you want to. There's an issue, though, that often gets overlooked for Japanese and many other languages that use an IME (Input Method Editor) to assist in typing languages with complex character sets.

![Example of Japanese IME input](https://static.waldenperry.com/2025/japanese-ime-example.png)

*Example of Japanese IME input*


The problem lies in the overloading of the Enter key. To make a selection from this list of words the IME uses the Enter key. So, the desired behavior is to submit the form when the Enter key is pressed *and* the IME is not in use.

A typical implementation without considering IME might look like this:

```javascript
const textarea = document.getElementById("input-textarea");

textarea.addEventListener("keydown", function (e) {
    // Shift + Enter should trigger a new line
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault(); // prevent new line on submit
        submit();
    }
});
```


IME completions *do* use the Enter key, so the event's `key` value is `Enter`. We need an additional check for IME input. Thankfully, the browser actually provides a flag for just this purpose on the keypress events: `isComposing`, which we can simply add into the submit check.


Unfortunately, this is the web, so [due to an issue in Safari](https://bugs.webkit.org/show_bug.cgi?id=165004) we can't rely on the `isComposing` flag completely. The recommended workaround is to check for `e.keyCode === 229`.

From the W3 UI Events [spec](https://www.w3.org/TR/uievents/#legacy-key-models):

> 7.3.1. How to determine keyCode for keydown and keyup events
> The keyCode for keydown or keyup events is calculated as follows:
>
> ...
> 
> If an Input Method Editor is processing key input and the event is keydown, return 229.

I think the purpose of this was to mask IME key presses from typical website functionality like this problem, but from a modern development perspective it's a bit arbitrary to be hiding what key was pressed. Technically, `keyCode` is a deprecated property, so I hope `isComposing` gets better WebKit support in the future.

Factoring in `isComposing` and the `e.keyCode === 229` Safari workaround would look like this:

```javascript
const textarea = document.getElementById("input-textarea");

textarea.addEventListener("keydown", function (e) {
    // Check for IME input
    const isComposing = e.isComposing || e.keyCode === 229;
    // Shift + Enter should trigger a new line
    if (e.key === "Enter" && !e.shiftKey && !isComposing) {
        e.preventDefault(); // prevent new line on submit
        submit();
    }
});
```


For websites that have this problem, I can at least write my text in TextEdit or another app first, then copy and paste it into the form as a workaround.