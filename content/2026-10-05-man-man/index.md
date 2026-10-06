+++
title = "man man"
date = 2026-10-05

[taxonomies]
tags = ["linux"]
+++

Did you know you can do read the `man`ual of `man`?

From `man man`:

```
DESCRIPTION
    The man utility finds and displays online manual 
    documentation pages.  If mansect is provided, man 
    restricts the search to the specific section of 
    the manual.
    
    The sections of the manual are:
        1.   General Commands Manual
        2.   System Calls Manual
        3.   Library Functions Manual
        4.   Kernel Interfaces Manual
        5.   File Formats Manual
        6.   Games Manual
        7.   Miscellaneous Information Manual
        8.   System Manager's Manual
        9.   Kernel Developer's Manual
```

For example you read about `open`, the cli tool with `man 1 open`, and separately `open()` the syscall with `man 2 open`.

I came across this while researching how people program in C. It was quite surprising to learn that there's 9 different sections to `man` you can access, when I've only ever used it to look up about commands.

```
b0sh@MacBook-Air-5 ~ % man 1 open
OPEN(1)       General Commands Manual         OPEN(1)

NAME
     open – open files and directories
```


```
b0sh@MacBook-Air-5 ~ % man 2 open
OPEN(2)          System Calls Manual          OPEN(2)

NAME
     open, openat – open or create a file for reading
or writing
```
