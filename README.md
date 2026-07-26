<div align="center">
  <img src="assets/plato-logo-brass-transparent.png" alt="Plato logo" width="200">
</div>

# Plato

*Built for engineers who get tickets, not greenfield projects.*

> **⚠️ Warning: if you are not a professional engineer, Plato is not for
> you.** It assumes you're a software engineer with years of hands-on
> experience, comfortable with Jira, Scrum, git, and professional software
> project workflows in general. If that's not you, look at fully-automated
> tools like Superpowers or GSD instead.

Plato is an AI coding methodology framework for Claude Code. It is designed
around how real engineers on real teams actually work: you get a ticket not an
open-ended mandate to build something from scratch. 

Plato organizes the whole lifecycle of that ticket, from requirement to reviewed diff, as a
sequence of small, transparent, human-checkpointed AI sessions.

## Philosophy

### Framework, not platform

Plato is deliberately a **framework** (like Spring or React), not a
**platform** (like a low-code tool or a fully automated agent runner). It
gives you conventions, scaffolding, and best practices — it does not
generate your design for you, run agents unsupervised, or make decisions on
your behalf. Every step is visible and stays under your control.

| | GSD | Superpowers | Plato |
|---|---|---|---|
| Type | Platform | Plugin system | Framework |
| Transparency | Low (black box) | Medium | High (white box) |
| Target user | Solo developer | General developer | Team engineer |
| State management | In-memory (TodoWrite) | In-memory | File-based (persistent) |
| Session model | Long sessions | Long sessions | Short `-p` sessions |
| ABS generation | Automated | Automated | Manual (engineer writes) |

### Rule-Oriented Programming

<div align="center">
  <img src="assets/plato-rule-oriented-programming.png" alt="Rule-Oriented Programming" width="320">
</div>

ABR — **Agent Behavior Rules** — is the collective name for the markdown
files that constrain how an agent works on a project: `AGENTS.md`,
`CLAUDE.md`, `ARCHITECTURE.md`, `NEVER.md`, and the like. In this new era of
software engineering, the most valuable thing an engineer produces is no
longer the code — it's the ABR files that shape how that code gets written.
Plato refines your ABR files at every step of every ticket, so the longer
you use it, the more your project accumulates an ABR library that's
tailored specifically to it.

### Loose, Transparent, and Honest

We're software engineers. We like transparency, because we need our
projects to stay controllable. Every checkpoint in Plato's workflow can be
edited by hand, restarted, or redesigned at any time — you can change
anything. This isn't vibe coding, and you're not working inside a closed
framework; the framework is assisting *you*. You are the one driving,
reviewing, and deciding. The cost is that Plato isn't one-click — it takes
some learning to use well.

### Slow down

Working with Plato will feel slow — much slower than the one-click
frameworks out there. That's because every step requires you to step in.
It's still much faster than writing everything by hand, though. While other
tools race to make AI coding faster, Plato deliberately tries to slow it
down, because staying in control of the project matters more than raw
speed.

## Installation

This repository *is* a Claude Code Skill named `plato`. Install it with the
[skills CLI](https://github.com/anthropics/skills):

```
npx skills@latest add CodePlato3721/plato -y -g
```

This fetches the skill into your global skills directory, making `/plato`
available in Claude Code.

