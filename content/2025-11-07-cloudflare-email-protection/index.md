+++
title = "TIL: Cloudflare email protection"
date = 2025-11-07

[extra]
link = "https://developers.cloudflare.com/waf/tools/scrape-shield/email-address-obfuscation/"
+++

I've been doing a bit of web scraping lately and ran across `[email protected]` in the HTML of the site I was downloading. Not that I had any use for their email, but I was curious what was doing the "protecting" so I dug into it. It turns out it's a [program by Cloudflare](https://developers.cloudflare.com/waf/tools/scrape-shield/email-address-obfuscation/) to combat scrapers. If Cloudflare thinks a request is a scraping, it looks for email like strings in the response and "protects" the email by removing it from being directly in the response. I checked my domain that I have on Cloudflare and it was on for me, so I guess its a default setting. 

I put the below JavaScript on my website years ago. The vast majority of visitors (99.9%+? my access log files are huge and simply there's no way that many people know me) to Walden's World and this blog is bots, and this email link has been on my [contact page](https://waldens.world/contact) for 10 years so you'd think I'd be on a bunch of spam email lists by now. I get remarkably little spam which makes me think that there's a decent effectiveness to js execution.

```javascript
<script type="text/javascript" >
//Is this even effective at stopping spam?
var walden = 'walden';
var world = 's.world';

document.getElementById("email").innerHTML = walden+"@"+walden+world;
document.getElementById("email").href = 'mailto:'+walden+"@"+walden+world;
</script>
```

Cloudflare's implementation is basically just this with extra steps. They have to ship the full email so that if it was a real user they can overwrite `[email protected]` with the actual email. So they encode the email and ship the decode function. What's I thought was cool about this approach is that Cloudflare can be a lot more aggressive with detecting bots, since even if a real user was accidentally caught up in this, they would still be able to view the email. However, any motivated scraper would be able to thwart this method by executing the JavaScript on the page. Or ever writing a special parser just for the Cloudflare email obfuscation format. I'll leave that as an exercise to the data harvesters.
