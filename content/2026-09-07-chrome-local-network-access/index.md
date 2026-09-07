+++
title = "Chrome vs. Apple's Standoff"
date = 2026-09-07

[extra]
link = "https://issues.chromium.org/issues/376742636"
+++

From [Chromium #376742636](https://issues.chromium.org/issues/376742636) - Multiple Chrome application items in macOS > Privacy&Security > Local Network

> The issue is an issue with macOS; we have filed FB15681423 with Apple. It’s likely related to updates.
> 
> Chrome does not “request new permissions”; macOS loses track of the permissions that were granted; that is filed with Apple as FB15683070. The statement that Chrome doesn’t “revoke permissions” is incorrect; it is the OS’s responsibility to track the permissions, and Chrome neither has the ability nor the responsibility to revoke permissions.

Sure, that sounds its Apple's fault, but I've also not seen any other app do this? I was hoping to find an easy way to clean the [hundreds of Chrome's](https://static.waldenperry.com/2026/chrome-local-network.png) out of my settings screen, but you have to [boot into safe mode](https://support.google.com/chrome/thread/438484479). And either way it'd just fill up again with new entries. Please end the standoff! The bug's been open since 2024.
