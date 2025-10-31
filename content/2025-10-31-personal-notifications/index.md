+++
title = "Setting Up Personal Notifications With Pushover"
date = 2025-10-31
+++

I've had a pretty good personal notification system going on for like eight years now with SendGrid. I have a gmail alt account that is only for these notification emails, and I use the Sendgrid free API plan to send me notifications from my [websites](https://waldens.world). Or well, I should say *used to*, because this month I discovered that [my free plan was taken from me](https://www.twilio.com/en-us/changelog/sendgrid-free-plan). How rude. I've been a (non-paying) customer for 8 years! Well no matter what, I had to find a new solution, and preferably one that didn't involve email.

The first thing I found was [this blog post](https://blog.alexsguardian.net/posts/2023/09/12/selfhosting-ntfy/) on selfhosting the [ntfy service](https://docs.ntfy.sh/), which I did manage to get working with Docker in a few hours. You can download their client app, and configure it to look at your domain if you host their server. Then you get push notifications. But right at the end I got hit with the self hosting gotcha: [iOS backgrounding](https://docs.ntfy.sh/config/#ios-instant-notifications). Ok so the docs say it won't be *instant* but I can wait a few minutes or so, right? But my notifications never came hours later... Something about [APNS](https://en.wikipedia.org/wiki/Apple_Push_Notification_service)? They have a solution where you relayed the messages their server, but at this point if I had to sign up for their service anyway then what was the point of self hosting? So I reverted my branch and tried again.

Then I took another look around and found [Pushover](https://pushover.net/). I was only looking for self hosted at first so I passed over it initially, but it seemed to have a good reputation. It's similar in where you download their client app for push notifications, but they host the API side as well. For a $5 one time fee you get an individual license with a measly 10,000 notifications a month (I will never hit this). And I get a bit more peace of mind that with some money on the line maybe I won't have to redo this system for another 8 years.

My site is in the beloved PHP language, so the code looks like this:

```PHP
$pushover_api_key = getenv('PUSHOVER_API_KEY');
$pushover_user_key = getenv('PUSHOVER_USER_KEY');

$ch = curl_init();
curl_setopt_array($ch, [
    CURLOPT_URL => "https://api.pushover.net/1/messages.json",
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => [
        'token' => $pushover_api_key,
        'user' => $pushover_user_key,
        'title' => $subject,
        'message' => $body
    ],
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_SSL_VERIFYPEER => true,
    CURLOPT_TIMEOUT => 30
]);

$result = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curl_error = curl_error($ch);
curl_close($ch);
```

It couldn't be more dead simple. It's just an HTTPS call, and their website walks you through making the tokens. I was done the entire change even through deploying in like 20 minutes. And something tells me long term this is going to be more stable then that ntfy Docker container self hosted solution. Let's go!
