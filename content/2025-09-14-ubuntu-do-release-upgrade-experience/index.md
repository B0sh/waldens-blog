+++
title = "My Experience with Upgrading Ubuntu with do-release-upgrade"
date = 2025-09-14

[taxonomies]
tags = ["linux"]
+++

I just went through the process of upgrading one of my web servers to Ubuntu 24 with the [`do-release-upgrade`](https://manpages.ubuntu.com/manpages/jammy/man8/do-release-upgrade.8.html) Ubuntu installer script, which I've never used before. Every time in the past I went to upgrade one of my servers, I deleted it and recreated from scratch. (yes, I take a backup too)

I wasn't super confident in what would happen but I wanted to give it a shot anyway, now that Walden's World and this blog are completely Dockerized I don't have nearly as much random commands I have to run to set up that server anymore, so my current installation is essentially default with Docker installed and config.

### Preparation

`do-release-upgrade` required the server to be fully up to date on packages for Ubuntu 22, so I ran a few commands for updating:

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt dist-upgrade
```

Then it was time to run the upgrader:

```bash
sudo do-release-upgrade
```

There were a few things to confirm but the thing that scared me the most was this prompt about cutting off SSH. 

```
Continue running under SSH? 

This session appears to be running under ssh. It is not recommended 
to perform a upgrade over ssh currently because in case of failure it 
is harder to recover. 

If you continue, an additional ssh daemon will be started at port 
'1022'. 
Do you want to continue? 
```

I'm not entirely clear why port 1022 is fine when port 22 isn't, but I decided to ignore this and continue because all my servers are hosted with Linode. Linode has a feature called [Lish Console](https://techdocs.akamai.com/cloud-computing/docs/access-your-system-console-using-lish) that allows you to remotely "physically" access your server, so after thinking about it for a moment, if I did have a problem I'd be able to recover the server without using SSH on a direct connection. Plus I have a backup anyway. If you have a sudden power outage or internet loss it's good to have a recovery plan.

The installer also prompted me about needing a few gigabytes of space, but just to be safe I stopped and cleared out double what was recommended to make sure I wouldn't have any troubles with that.

### Installation Process

Once I kicked off the installation it mostly went about on its own going through upgrading all the packages one by one. I was prompted a few times on the way to confirm some upgrades and about the config changes I had made to `sshd_config` and `journald.conf`. There was a merge conflict of sorts between the default config in Ubuntu 22 and 24, which makes sense because I had made my own changes to the config. I decided to go with Ubuntu 24's new config and then manually adjust my config back after the fact according to my own new server setup documentation.

The whole process took around 20-30 minutes for me, but perhaps if I had been watching closer I could've caught the prompts I got faster.

Finally, I was prompted to restart, and it worked!

```
$ lsb_release -a
No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04.3 LTS
Release:	24.04/bak
Codename:	noble
```

That is, until I went to `sudo apt-get update` again. This is the only error I've run into so far after I upgraded the server.

```
N: Missing Signed-By in the sources.list(5) entry for 'http://mirrors.linode.com/ubuntu'
```

Since Linode is doing some special magic to mirror the Ubuntu package sources, I guess this wasn't accounted for in the official upgrade script. I followed [this advice](https://askubuntu.com/questions/1516700/missing-signed-by-in-the-sources-list5-entry-after-installing-ubuntu-24-04) from a Stack Exchange post and was quickly able to get Linode's sources key readded:

```bash
echo "Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg" >> /etc/apt/sources.list.d/third-party.sources
```