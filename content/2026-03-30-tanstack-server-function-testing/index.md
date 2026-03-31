+++
title = "TanStack Start Server Function Testing"
date = 2026-03-30

[taxonomies]
tags = ["webdev", "tanstack"]
+++

I've been trying out [TanStack Start](https://tanstack.com/start/latest/docs/framework/react/overview) for the last few days. So far it's been decent to work with, but I ran into a huge roadblock when it comes to unit testing their server functions with `vitest`. Simply calling the function in a test was throwing an error.

```Error: No Start context found in AsyncLocalStorage. Make sure you are using the function within the server runtime.```

 I couldn't find anything in the official docs, but eventually I saw this [workaround](https://github.com/arackaf/repro-server-fn-in-vitest) after digging around on GitHub to see how other people were tackling this. The main issue is that you TanStack Start expects a lot of metadata (Start context) to come along with a server function invocation, and so we have to supply all of that context ourselves.

Assume you have a TanStack `createServerFn`:

```typescript
import { createServerFn } from "@tanstack/react-start";

export const getServerNumber = createServerFn({
  method: "GET",
}).handler(async () => {
  return 15;
});
````

I then added this function into my test library code to add the metadata.

```typescript
import { runWithStartContext } from "@tanstack/start-storage-context";

export function runTestServerFn<T>(fn: () => Promise<T>) {
  // Server functions require a Start context to be available in AsyncLocalStorage
  // This mimics what TanStack Start does during request handling
  return runWithStartContext(
    {
      getRouter: () => ({}) as any,
      request: new Request("http://localhost/"),
      startOptions: {},
      contextAfterGlobalMiddlewares: {},
      executedRequestMiddlewares: new Set(),
    },
    fn,
  );
}
```

Then in a `*.test.ts` file:

```typescript
it("runs ssr function", async () => {
  const result = await runTestServerFn(() => getServerNumber());
  expect(result).toEqual(15);
});
```

I hope TanStack looks at adding better support for testing when they go into 1.0 (to be fair, Start is in RC at the moment). It seems like a huge miss in the library to not at least have docs about best practices for testing SSRs.
