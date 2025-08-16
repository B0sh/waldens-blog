+++
title = "Switching Node Versions without Admin Privileges"
date = 2025-08-15
+++

I've been using [NVM Windows](https://github.com/coreybutler/nvm-windows) for a long time to easily switch Node versions for working with different apps. With NVM Windows it requires admin access to adjust the Windows environment for Node. However, my new corporate laptop policies got stricter with admin rights, and so I'm not able to just quickly elevate to admin to switch my node version anymore.

The solution I ended up using involved [NVM sh](https://github.com/nvm-sh/nvm) and the Git Bash shell. I was able to install [Git for Windows](https://git-scm.com/downloads) without admin, so that's what I went with. WSL also should work if you have that installed.

The [Installing and Updating](https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating) steps were quite simpler. Here's what I had to do:

1. Run the install script in Git Bash:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

2. Add this command to `~/.bashrc`:

```bash
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
```

3. Reload your terminal or run `source ~/.bashrc` and `nvm` commands should be accessible now:

```bash
nvm install 20
nvm use 20
```

The main limitation is that you'll need to continue using Git Bash for all your `node` or `npm` commands going forward. 
