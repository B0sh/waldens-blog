+++
title = "TIL: Typescript Path Aliases"
date = 2026-11-27

[extra]
link = "https://www.typescriptlang.org/tsconfig/#paths"
+++

I was investigating an [auth library](https://www.better-auth.com/docs/integrations/next) today when I stumbled upon this syntax:

```javascript
import { auth } from "@/lib/auth";
```

Which confused me, because I couldn't tell if it was a project path or a node module. Turns out this is a [feature](https://www.typescriptlang.org/tsconfig/#paths) of TypeScript, which you can set up in your `tsconfig.json` like so:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

This solution can help with cleaning up really long relative paths like I frequenctly see in Angular or React projects. It should also help when moving files around, that would otherwise break the relative imports.

```javascript
// this:
import { SharedWidget } from '../../../../shared/widget';
// can become this:
import { SharedWidget } from '@/shared/widget';
```
