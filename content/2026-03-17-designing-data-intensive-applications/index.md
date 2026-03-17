+++
title = "Martin Kleppmann: Designing Data-Intensive Applications"
date = 2026-03-17

[taxonomies]
tags = ["book-review", "web-dev"]
+++

![Designing Data-Intensive Applications](https://static.waldenperry.com/2026/ddia.jpeg)

[Designing Data-Intensive Applications](https://dataintensive.net/) came highly recommended online as a great place to start for getting introduced to distributed systems. 

This book answered so many of the questions I've been having about how scaling actually works. To out myself, I've not had an experience doing so-called *distributed systems* in my career so far. Backup processes, queues, data warehouse, etc, sure, but I've never needed to have service availability in multiple datacenters or shard a database for example.

So a lot of the fundamentals talked about here were brand new concepts to me, which probably explains why I loved it so much. Clearly I'm not a subject matter expert here, so the rest of this post is going to be talking about the various ways I had my mind blown by DDIA. I'm going to be thinking about the concepts in here for a long time.

Unfortunately, I picked the worst time to start this book as the [2nd edition](https://learning.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/) was released the same month I got my copy of the first edition. 

---

### NoSQL Databases

In my career, I've never given much thought to using anything other than a relational database. I didn't realize the extent to which different databases had differing design philosophies and how that manifests in their usage patterns and data storage.

Chapter 2, specifically changed my mind on the idea of "JSON in databases". I've always written this off as a bad idea because "No fixed schema? How can you reason about anything?". But when the document model was introduced as a concept it finally clicked for me. In an application where you really don't have a lot of relationship between documents, a NoSQL database can simply store the document as is with the fields and properties that it needs right with itself. Therefore you can have extremely fast access to the entire document all at once, for example like on a details page.

Schema migration is another thing that I naively thought was impossible with NoSQL databases. You'd have to loop and update in place all of your documents to add new fields or change field naming in the database, and take out the server in the mean time. They discussed a way to avoid this by create a temporary new table, and migrate all the documents in there, while using the old table to serve old requests schema format and the new table for new code. Eventually you can retire the old schema when its no longer required by any active code. This type of really clever thinking about working with data was genuinely world view changing.

### Distributed Databases

I've never been forced to consider what happens if your database actually is so big that it physically can't fit on a single server. The biggest table I've ever worked with is on the order of hundreds of millions of records, and I thought that was pretty big. 

In Chapter 5 & 6, database replication and sharding are discussed respectively. I had always thought that fundamentally you can't simply split a database up all over the world and have queries process concurrently correctly. I'm relieved to know that my assumption was correct. Sharding - splitting your data across multiple servers, and replication - having the same data being available across multiple servers, both have concurrency flaws that can only be mitigated. Even time is not reliable as a source of truth between machines! (see Chapter 8)

Correctness, however, is achievable through careful consideration of tradeoffs. The concurrency problem needs a lot of buy in all the way down to the application development level. The book discusses many different algorithms you can use depending on your tolerance for data loss and slowdowns. Correctness comes at the cost of performance, so if you can design your application around handling data inconsistency errors when they appear, the performance savings can be massive. 

### Event Processing

Chapters 10 & 11 were about batch and stream processing respectively. At the scale of data being discussed here, the way that eventing is approached has massive effects. Super computer level batch processing was discussed, and it was interesting how error recovery works there when you do not need to quickly show a result to a user.

Protocol Buffers also blew my mind. That's another technology I've heard thrown around over the years but never came up in my work directly. They allow much greater bit efficiency than JSON as text does, allowing processes to more quickly communicate between each other. Events are the name of the game in distributed systems world as its a shared language that different teams can use to communicate between each other even they use completely different implementations.

### Extra Notes

- I [generated a list of technologies](https://gist.github.com/B0sh/d2b1f7de082b5036f275c8e4a25cfb5f) found in the book. Pleasantly surprised how much of the distributed systems technology is open source! Apache is responsible for Kafka, Hadoop, ZooKeeper, and many more.
- There's very little code or practical examples here. I have a desire to *practice* distributed systems, but as of yet I'm not entirely sure where to start.
