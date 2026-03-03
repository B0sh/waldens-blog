+++
title = "Benji Smith: Marcus Marcus Marcus"
date = 2026-03-02
[extra]
link = "https://machinecreativity.substack.com/p/marcus-marcus-marcus-ai-randomness"

[taxonomies]
tags = ["ai"]
+++
Super interesting article about randomness with LLMs about picking names, humorously titled [Marcus, Marcus, Marcus](https://machinecreativity.substack.com/p/marcus-marcus-marcus-ai-randomness). As you can imagine they found that LLMs were disproportionally picking Marcus as a "random" name (perhaps *the* random name). 23.6% of responses were Marcus to be exact. The whole article was interesting, but the experimenting of trying improve the "randomness" of the name generation was of note to me:

> Can you make a language model more random by injecting randomness into its input?
> 
> We tested this by prepending a random “seed” to the user message. We tried several different kinds. First, “noise seeds” — random characters at three different lengths:
> 
> > 16 chars: RANDOM(<N9W_SXK/c>”R7Tq)
> > 
> > 32 chars: RANDOM(YnNOd,Snb[s{{i#\cIqo#i3]e+xmgm+&)
> >
> > 64 chars: RANDOM(L=9~$GCl+6zc*%?3NSpm#klRk#-c<v0%4|.bh<\46]ZOAH_U&pb;CPy8sH#”1D~4)
> 
> And then “word seeds,” randomly drawn from a list of 800 common English words (omitting any gendered or name-like words, e.g, “queen,” “king,” “autumn,” “forest”), in groups of four or eight:
> 
> > 4 words: RANDOM(year fire jacket suppose)
> >
> > 8 words: RANDOM(loud north great water choice face dead sure)

> Seeds work. Any kind of seed — noise or words — dramatically increases diversity compared to no seed at all. The no-seed condition produced only 288 unique names; the best seed conditions produced nearly 800.


In my own work with my [language trainer](https://github.com/B0sh/language-trainer) app, the main concept was to use AI to generate example sentences to practice listening comprehension. I ran into this creative wall quickly where I was getting very similar sentences and I actually implemented a similar approach. 

My idea was to ask the model to write the passage about `$RANDOM_WORD`, which was taken from a list of words based on the users set language level. Still, on longer passages I do find the stories to be quite repetitive. I'm definitely going to give this word seed approach a try soon as I resume work on the language trainer project.
