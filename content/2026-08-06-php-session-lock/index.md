+++
title = "PHP Sessions Locks Concurrent Requests"
date = 2026-08-06

[taxonomies]
tags = ["php", "web-dev", "performance"]
+++

I've known that PHP Sessions can cause long waits times for years, yet I was very surprised to find this out. Let me explain.

Let's say you run a PHP script with a really long query, where the execution is expected to take 10s+. If you try to visit another page on that same website with a different tab, your request will get stuck in loading. Until, suddenly, once the long running script completes that secondary request will go through. Other users of the website aren't getting blocked though, only your browser.

---

I've observed that behavior for years but I've never thought to consider how that happens until now. Why are other users not getting blocked on a long running request? How does PHP know that my other tab is also still me?

The answer is the PHP Session. When a session is created with [`session_start();`](https://www.php.net/manual/en/function.session-start.php) it opens a session's data file and places a lock on it. A new PHP request with that session will get caught on the lock, blocking concurrent PHP session initializations with the same session. In our example above, this explains how that long running query isn't blocking users with a different session.

This is a very helpful default as you could get nasty race conditions from parallel script execution. However, knowing this fact can unlock optimizations when you don't need this safety net. [`session_write_close();`](https://www.php.net/manual/en/function.session-write-close.php) will close the sessions's file lock and continue executing the rest of the script. Any updates to `$_SESSION` after won't be saved after execution completes.

```php
<?php
session_start();
// perform session writes and reads
session_write_close();
// may still read session contents
```

This example from the [`session_start()`](https://www.php.net/manual/en/function.session-start.php) docs is also viable. If you know your script will not be doing any `$_SESSION` writes, then you can close it right away:

```php
<?php
// If we know we don't need to change anything in the
// session, we can just read and close rightaway to avoid
// locking the session file and blocking other pages
session_start([
    'read_and_close'  => true,
]);
```

Unfortunately for me though, my project's code is really old, and has a lot of `$_SESSION` writes even at the end of scripts, so this optimization isn't helping me out. (yet!) Still I'm sure this will come in handy in the  future, so I'm glad to know it and make this blog post.
