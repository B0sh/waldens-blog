+++
title = "This Web Dev Guy Vibes With SwiftUI"
date = 2025-10-28
+++

As a web guy, [my attempts](https://github.com/B0sh/language-trainer) to make apps have always been confined to Electron. I always looked up to native apps very highly, but had never given it a true shot. So I when had an idea for an personal audio player app thing, I decided to ditch what I know and give SwiftUI a shot. Just to be sure we're all clear: I don't know how to do this. I make websites. However, in 2025, surely coding agents have 10x productivity right? With my Github Copilot subscription I can run Claude 4 or GPT-5-Codex agents, so I've got the top of the line LLM access. Easy.

Well, here I am after a week of hacking and prompting with agents in my downtime and I do have a quite functional app now with 7 screens and almost all of my long shot wish list features in already. Considering I started from downloading Xcode, I'm confident there's no way I would have had something this feature complete this quickly without LLMs. Bototm line, this app works for me.

What I *loved* about this development journey though is how I got progressively exposed to SwiftUI concepts as I needed them. Or to put it another way, I did the terrible thing of ignoring all the code I didn't understand until I realized it was a problem. That was the time I dug in deeper. Obviously that's something I can get away with here because I'm the only user for this project. But at the same time I can feel the code getting further and further away from me as more and more code I don't understand is creeping in this project. And as I said it works *for me*. I went in from the start knowing I'd never have another user. I feel very far from a hypothetical production app. So I thought I'd do a bit of a postmorterm on what I learned and didn't learn with agent first development.

---

### What I learned

- **`View`**: I got the best handle on creating and using `View`s. I really enjoyed thinking about UI problems in terms of `HStack`/`VStack`. With CSS and flexbox you'd have to set up this pattern for yourself. Just the whole concept of `View` was great to work with.

- **Swift**: While obviously I still would have so much to learn, I do feel like I picked up Swift quite quickly. Before long I was comfortable writing my own Swift pure functions without AI assistance as needed. I'm talking about all the basics here: arrays, variables, functions, typing, error handling, etc.

- **[LazyVGrid](https://developer.apple.com/documentation/swiftui/lazyvgrid)**: This is an awesome API for doing content aware grid reflowing. I know browsers have CSS Grid and flexbox, and I know how to use them, but I really liked the API that's in SwiftUI. My app has several of these.

- **`#Preview`**: The `#Preview` block lets you write some code to live preview your component views while in Xcode. You can setup as many different inputs as you want to test various states and edge cases. The fact that it's just built right in was super helpful for my project. I can think of times in the past where I've gone and created test pages or design pages to test these things before, but this was a whole new level to that concept. Soon I want to investigate this for my typical React/Angular development. [Storybook](https://storybook.js.org/) might be a good place to start.

- **SQLite**: While not specific to Mac development, this was my first project where I used SQLite to run the data layer. This ended up being a great choice. Swift has several great community libraries for SQLite integration.

---


### What I didn't learn

- **Threading and MainActor**: My app has network calls and a SQLite database, and I tried to keep it simple and not care about blocking the main thread, but even I couldn't put up with that. I had 3 or 4 failed attempts where eventually the SQLite database would end up locked. Finally I prompted for "everything to be on the main thread except for network calls", which led to a successful program. In theory, it would've been nice to move that whole process to its own thread, but in practice it hasn't mattered for me.

- **AVFoundation**: Considering I made an app that plays audio, I very rarely had to touch the generated AVFoundation player code. Getting the *player UI* to look good was much harder, but the playing of an mp3 file part was not affected.

- **`extension`**: I ended up with 5 `extension` blocks that were LLM generated, and I never needed to learn what that is. I assumed it was like extending a prototype like in JavaScript, which makes sense just fine. But, critically, I didn't understand the LLM chose an `extension` and not just a regular function.

- **Eventing with @State, @ObservedObject**: I have a lot of state getting passed around, and every single bit of it I didn't write myself.

- **Navigation**: Speaking of not writing code, I also didn't write any of the navigation handling code. There's several issues with the Navigation still but it's good enough for me at this point.

---

### Conclusion

I don't want to say I learned absolutely nothing about these "What I didn't learn" points, because I was directing the direction of the agents and making tweaks as I went. I just know I wouldn't be able to defend the logic or reasoning behind the code in those spots because I don't understand it enough. And my main focus was on the UI design, and I think that comes across in the concepts I glossed over.

The way I've always pushed my programming skill is by doing. If the doing is getting done for me, does the value of doing side projects for learning go down? I'm still thinking through this.

---

### Bonus: Struggles

- **App Icon**: I got stuck for an hour setting up an app icon. I was completely positive I did it right dragging in icons into Xcode. Turns out I needed to do a Clean & Rebuild... Maybe one day computer use LLMs will be available enough to debug Xcode for me.

- **iOS hallucinations**: The LLMs would often try to bring in iOS only APIs that would be an instant `not available in macOS` build fail. In retrospect, I think an `AGENTS.md` file would've been helpful here to note that this was a Mac app.
