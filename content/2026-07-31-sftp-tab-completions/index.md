+++
title = "Fixing sftp Tab Completions on macOS"
date = 2026-07-31
+++

GUIs are good for FTP too, but lately I've just been using the [`sftp`](https://man7.org/linux/man-pages/man1/sftp.1.html) command as a way to really quickly just make one or two transfers.

```bash
sftp user@host
Connected to host.
sftp> put ~/stuff.zip
```

I've been copy and pasting my file paths the whole time, until I just found out there's a way to get tab complete in the prompt. The built in `sftp` command to macOS doesn't have tab complete support built in, so you have to download the `openssl` version.

```bash
brew install openssh
```

You'll also need to update your PATH to prioritize the `openssh` version of the command over Apple's.

```bash
export PATH="/opt/homebrew/opt/openssh/bin:$PATH"
```
