+++
title = "TIL: less"
date = 2026-03-08

[extra]
link = "https://www.man7.org/linux/man-pages/man1/less.1.html"

[taxonomies]
tags = ["til"]
+++

The `less` command can display the contents of a file like `less access.log`, but it can also display the content piped in.

```bash
cat access.log | less
```

You can use that fact to quickly examine intermediate output too. Like this multi-stage command to count IPs in an access log:

```bash
cat access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head
```

You could add `less` to examine the `awk` command's output.

```bash
cat access.log | awk '{print $1}' | less
```

I found this really helpful for debugging today!
