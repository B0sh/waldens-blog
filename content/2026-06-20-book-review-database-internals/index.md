+++
title = "Alex Petrov: Database Internals"
date = 2026-06-20

[taxonomies]
tags = ["book-review", "database"]
+++

![Database Internals Book](https://static.waldenperry.com/2026/database-internals.jpeg)

This month I read [Database Internals](https://www.oreilly.com/library/view/database-internals/9781492040330/) by Alex Petrov.

I like to write book reviews as a little summary of the cool or interesting things I learned from my readings.

There were two parts to the book: Storage Engines and Distributed Systems.

## Storage Engines

Easily the most fascinating part about databases is the unavoidable interaction of hardware and software. It was interesting to learn of the ways that algorithm design and implementation of databases considers hardware. 

Multiple chapters of the book were dedicated to B-Trees. It's a structure that balances with the reality of computer hardware. In theory, a Binary Search Tree would be a much simpler structure for database storage. However, BST will scatter its data all over the disk. With SSDs even if you want one bit from a specific location, the entire page at that location also will be read. Taking advantage of this, B-Trees have nodes that are sized to match the page size. This has many advantageous properties like lowering the tree height (less disk reads) and high `fanout` (many similar local values being referenced in one node). Many B-Tree variations were mentioned, which each have different tradeoffs and affect performance. For example, database implementations have to consider the access of the data as well, like operating system page caching. 

[Bloom filters](https://en.wikipedia.org/wiki/Bloom_filter) were also really cool to learn about. It's a hash based algorithm that can quickly tell if a record "*might be in the table or definitely not in the table*". It's a quick check you can make before going through a relatively expensive search operation.


The success of writing data is of the upmost importance as well, and there were many algorithms discussed to ensure this. A typically employed approach is the Write Ahead Log. All database operations are written to a sequential log to disk, and updates to the internal B-Tree are batched together to improve performance. In the case of a failure, the last on disk state can be loaded and then the logged changes can be replayed.

This is also the first time that database isolation levels really clicked for me. There's 4 levels.

* Read Uncommitted
* Read Committed
* Repeatable Read
* Serializable

I don't know why but when in my head I had treated these as like binary blobs to memorize, but the names actually explain themselves once you get it. `Read Uncommitted` allows you to read values while a transaction is in progress - before they are committed. `Read Committed` solves for in progress transactions - reading only committed values, but does not address multiple values. `Repeatable Read` guarantees that once a transaction starts, the read will always be repeatable - even if transactions complete during execution. And finally, `Serializable` requires transactions be equivalent to a specific ordering.

The book mentions that each time you go up in isolation level that there's a performance cost due to more and more loss of concurrent execution. 

As data is added and deleted, data becomes more and more fragmented naturally. Eventually a type of defragmentation happens called the `vacuum` where pages are optimized and rewritten to disk. Now empty pages can then become available to the database to be reused!



## Distributed Systems

If I took away anything from Part 2 it was this: Distributed Computing is Impossible.

At least theoretically anyway. [FLP Impossibility](https://en.wikipedia.org/wiki/Consensus_(computer_science)#Solvability_results_for_some_agreement_problems) and the [Two Generals Problem](https://en.wikipedia.org/wiki/Two_Generals'_Problem) tell us that there is no safe algorithm to get consensus in a system where message transfer is unreliable. In practice, though we can design algorithms if we add constraints to the system, like timeouts.

When you really stop to consider it, the number of ways things can fail is enormous. Failures were discussed significantly in the Storage Engine part too but once messages are distributed it compounds further. Consensus algorithms have to take into account the fact that at any point messages can vanish, processes can crash, networks disconnect, etc. Some algorithms even consider Byzantine failures where an attacker actively sends bad data too. It made my head spin - in a good way. Even detecting a failure is not reliable. When a process doesn't respond to you, it's impossible to tell if the message was deleted (network issues), or the process crashed. 

The book covers in detail widely used algorithms in distributed computing for failure detection, leader election, consensus, transactions, and data querying. There's way too many to list even briefly. Seeing the wide variety of algorithms in use today by different databases goes to show that every approach has its tradeoffs. 

I have to call out Conflict-Free Replicated Data Types (CRDTs) though. Seriously who comes up with this. The idea is that updates should be represented as events. The events can be batched up and applied in any order that they arrive to the server. This leads to a system with eventual consistency. It's not the first time I've heard of CRDTs, but after reading through the book it finally clicked how cool these are.

Overall, my big takeaway is the amount of overhead required for running distributed databases is immense. Messages passing around all over the place, heartbeat pings, ack messages, etc. One should consider their situation extremely carefully before going down this road.

## This is my Conclusion

I'm not going to be a database engineer or anything like that, (but a part of me wants to give it a shot now) so I read this book as a way to casually deepen my understanding of how databases work and give me more tools to reason about why I'm seeing certain behavior as I work with databases on a daily basis. I did resort to a *tiny bit* of skimming when it came down to the deep implementation discussion, but that wasn't what I wanted from the book anyway. It was a quicker read than I thought too. 

I do think I've picked the low hanging fruit in my distributed systems knowledge with the last [few](https://waldenperry.com/designing-data-intensive-applications/) [books](https://waldenperry.com/book-review-system-design-interview/) I've read, so my next [read](https://gchandbook.org/) will be looking at memory. (I'm hyped!)
