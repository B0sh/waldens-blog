+++
title = "Debugging Github Actions"
date = 2026-02-24

[taxonomies]
tags = ["github-actions", "web-dev"]
+++
My Github action to deploy this blog decided to fail one day with:

```bash
Error: Process completed with exit code 1.
```

I thought "huh that's wierd". My build script essentially is just an rsync to a server. The PR was changing my blog's template a bit, so on the off chance something I changed went haywire I also tried to rerun a previous commit. Same error.

I'm used to a lot of downtime from Github so I figured I'd wait to the next day to deploy and hope it would magically go away. It did not...

![Recent github downtime graph](https://static.waldenperry.com/2026/github-downtime.png)

*It's been rough being a Github user lately...*

At first I didn't have any leads because the error was so vague. Which command is erroring? Or are my commands not even running at all? Did Github Actions have a breaking change?

For reference here's the relevant action for my deployment. 

```yaml
- name: Deploy to server
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  env:
    DEPLOY_HOST: ${{ secrets.DEPLOY_HOST }}
    DEPLOY_USER: ${{ secrets.DEPLOY_USER }}
    DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
    DEPLOY_PATH: ${{ secrets.DEPLOY_PATH }}
  run: |
    mkdir -p ~/.ssh
    echo "$DEPLOY_KEY" > ~/.ssh/deploy_key
    chmod 600 ~/.ssh/deploy_key
  
    ssh-keyscan -H "$DEPLOY_HOST" >> ~/.ssh/known_hosts
  
    # Deploy files using rsync, deleting unused files on the server
    rsync -avz --delete \
      -e "ssh -i ~/.ssh/deploy_key -o StrictHostKeyChecking=no" \
      public/ \
      "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_PATH"
  
    rm -rf ~/.ssh
```

I added [`set -x`](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) into my `run` block to start of the script to get bash to output a trace of the commands it runs. This let me see the following log:

```bash
+ mkdir -p /home/runner/.ssh
+ echo '***
***
***
'
+ chmod 600 /home/runner/.ssh/deploy_key
+ ssh-keyscan -H ***
Error: Process completed with exit code 1.
```

Now I know the error is in the ssh-keyscan command!

Then the answer immediately dawned on me. A few weeks ago I moved my site into Cloudflare, and that comes with it all of the magical Cloudflare proxying. Which is also proxying this ssh connection. (And I thought I changed nothing...)

[Cloudflare tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/) looks like the Cloudflare approved solution. With a tunnel, you could actually completely hide your server's IP address from public visibility, routing all of your traffic through cloudflare. Considering this is just my static personal site, I decided on an easier workaround. Instead, I updated my `DEPLOY_HOST` secret to use my server's IP address instead of the domain. This essentially bypasses Cloudflare's proxy and requests an SSH connection to my server directly. If I ever change hosts or have my IP rotated on me, I'll have to update the action variables again, but that is a completely acceptable tradeoff to me.

And just like that, I'm back to having the beautiful green checkmark.

![Github Actions is back to normal!](https://static.waldenperry.com/2026/github-success.png)
