+++
title = "About those numbers on commands"
date = 2026-10-08

[taxonomies]
tags = ["linux"]

[extra]
pangram = ""
+++

After writing my [last post](/man-man) on the different sections of the `man` command, it finally dawned on me what the number in commands written like `cat(1)` is: the section number.

Just as an example I'll quote a part from the book I'm currently working through, [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) where I had my revelation.

> For example, the **vmstat(8)** utility prints a system-wide summary of virtual memory statistics
> and more, based on kernel counters in the /proc file system. This example **vmstat(8)** output is
> from a 48-CPU production API server:

The (8) stands for the man section 8 or the *System administration commands*.
