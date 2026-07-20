+++
title = "Git History When Moving Files"
date = 2026-07-20
+++

I looked up today if there was any way to preserve git history when trying to change the folder structure of a large codebase. To my surprise I learned git was already doing this by default!

I had [Codex make me a demo](https://github.com/B0sh/investigations/tree/main/gitmove) that shows how it works. Creating a move file commit and then a new line will preserve the history with `git log --follow`. Even if there are a few changes it can also still keep history, but to be 100% sure of keeping history (especially over hundreds of files) I think making a restructing commit just with moves is the best approach.

In particular I was worried about the git blame feature of my editor for line-by-line history, which I've come to rely on a lot as a way to navigate older codebases, so I opened these demo repos myself to examine in editor. It works totally fine after moves!
