# Prepare workspace

This is about preparing your workspace. Whether you're working in a plain
terminal or in VSCode, you need **two windows** open at all times.

## guide session

The session you talk to Plato in. It tells you what to do next — hence
"guide." In VSCode, this is the default Claude extension panel that's
already open.

## working session

The session where the actual work happens — this is the window an agent
session runs in to do the real task. In a plain terminal, open a second
terminal window for it. In VSCode, use `` Ctrl+` `` to open an integrated
terminal and run the agent session there. This window must stay separate
from the guide window — never the same one — so the guide's context stays
clean.

# In practice

## Daily workflow

You only need to remember one command: `/plato <ticket-number>`. Keep
asking the guide with it. The guide tells you the exact command you need
next — copy that command out and run it in the working session window.
Whether you're starting a new task, or coming back after doing something
else and forgetting where you left off, just run this command again.

You can also freely switch between multiple tickets — you never need to
remember where a given ticket was left off; asking the guide always tells
you.

## Manual commit & push

The framework never commits or pushes anything for you. This is not a bug
— it's intentional. You're free to do anything you want before committing,
and you decide when to commit and push yourself. This keeps the code clean
and controllable right up until the moment it's actually committed.

---

**Previous:** [← 01. Begin](01-begin.md) · **Next:** [03. Feature →](03-feature.md)
