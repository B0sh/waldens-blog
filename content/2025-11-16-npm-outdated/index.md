+++
title = "TIL: npm outdated"
date = 2025-11-16

[extra]
link = "https://docs.npmjs.com/cli/v8/commands/npm-outdated"
+++

Today I stumbled across [`npm outdated`](https://docs.npmjs.com/cli/v8/commands/npm-outdated).

> This command will check the registry to see if any (or, specific) installed packages are currently outdated.
> 
> In the output:
> 
> - `wanted` is the maximum version of the package that satisfies the semver range specified in `package.json`.
> - `latest` is the version of the package tagged as latest in the registry.

I'm suprised I've never thought to check if something like this existed before. Until now I always manually reviewed each package to see if there's a newer version.


```
b0sh@MacBook-Air-4 language-trainer % npm outdated
Package                           Current   Wanted  Latest  Location                                       Depended by
@google/generative-ai              0.21.0   0.21.0  0.24.1  node_modules/@google/generative-ai             language-trainer
@typescript-eslint/eslint-plugin   5.62.0   5.62.0  8.46.4  node_modules/@typescript-eslint/eslint-plugin  language-trainer
@typescript-eslint/parser          5.62.0   5.62.0  8.46.4  node_modules/@typescript-eslint/parser         language-trainer
@vitejs/plugin-react                4.7.0    4.7.0   5.1.1  node_modules/@vitejs/plugin-react              language-trainer
eslint                             8.57.1   8.57.1  9.39.1  node_modules/eslint                            language-trainer
eslint-plugin-react-hooks           5.2.0    5.2.0   7.0.1  node_modules/eslint-plugin-react-hooks         language-trainer
ollama                             0.5.18   0.5.18   0.6.3  node_modules/ollama                            language-trainer
openai                            4.104.0  4.104.0   6.9.0  node_modules/openai                            language-trainer
react-error-boundary                5.0.0    5.0.0   6.0.0  node_modules/react-error-boundary              language-trainer
typescript                          4.5.5    4.5.5   5.9.3  node_modules/typescript                        language-trainer
vite                               5.4.21   5.4.21   7.2.2  node_modules/vite                              language-trainer
```
