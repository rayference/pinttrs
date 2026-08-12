# AI Usage Policy

The **pintext** project has the following rules for AI usage:

- **All AI usage in any form must be disclosed.** You must state the model you
  used along with the extent that the work was AI-assisted. Example:
  *Claude Opus 4.8 for initial code generation*.

- **The human-in-the-loop must fully understand all code.** If you can't explain
  what your changes do and how they interact with the greater system without the
  aid of AI tools, please do not contribute to this project.

- **Issues and discussions can use AI assistance but must have a
  human-in-the-loop.** This means that any content generated with AI must have
  been reviewed *and edited* by a human before submission. AI is very good at
  being overly verbose and including noise that distracts from the main point.
  Humans must do their research and trim this down.

- **No AI-generated media is allowed (art, images, videos, audio, etc.).** Text
  and code are the only acceptable AI-generated content, per the other rules in
  this policy.

These rules apply strictly to external contributions to **pintext**.
Maintainers are trusted to apply good judgment when using AI tools and are not
strictly subject to these rules, although they are encouraged to follow them.

## There are humans here

Please remember that **pintext** is maintained by humans.

Every discussion, issue, and pull request is read and reviewed by humans
(sometimes with the assistance of machines). They should be approached with the
understanding that a contribution is made valuable by the amount of human work
that has been put in it — with or without AI assistance. Vibe coding rarely
produces results that meet the quality requirements of this project: LLM output
has to be worked on significantly to reach a state where a merge with the
codebase can be considered. That work should come upstream of opening a PR, and
not be offloaded to maintainers by putting them in a conversation with an LLM
with the PR's author as an intermediary.

## We are not anti-AI, but...

This codebase is written with AI assistance, applied with judgment, at a
magnitude that allows maintainers to keep an understanding of the entire
codebase. Inconsiderate usage of AI tools not only increases the burden on
maintainers and degrades the understanding they have of their codebase, but also
is an environmental threat and promotes cognitive atrophy.

While we understand that using AI tools is compelling in a highly competitive
economy, we do not want to encourage contributors to use them — they are already
pushed by their competitors and AI tool providers.

## Working with coding agents

Agent-specific guidance for this repository — layout, commands, conventions and
the gotchas that trip agents up — lives in [`AGENTS.md`](AGENTS.md).
`CLAUDE.md` is a symlink to it, so a single file serves every tool.

## Are you willing to contribute?

Then head on to our [developer's guide](https://pintext.readthedocs.io/en/latest/dev/index.html).
