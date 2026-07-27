# ABR

The whole framework is rule-oriented. What a software engineer actually
produces today isn't code — it's the rules that let an agent produce code.
It's the same relationship as a high-level language instructing a compiler
to emit machine code: the rules you write are the new high-level language,
just one level of abstraction further up.

I call these files **ABR — Agent Behavior Rules**. The `AGENTS.md`,
`CLAUDE.md`, and similar files you already know are all ABR.

# Plato and ABR

Plato is a framework built around ABR files. When you develop a project
with Plato, the most important thing produced isn't the project's code —
it's the ABR files that gradually accumulate while you maintain that code.
These files both maintain the project going forward and serve as a
distilled record of your experience working with the agent.

Plato maintains ABR in two places:

## project context

Path: `plato-workspace/project-context`

- `SETTINGS.md`: Plato-related project settings, e.g. the unit-test and
  e2e-test paths.
- `INDEX.md`: to keep the agent's startup context from getting too long,
  put only the **smallest possible** set of essential project knowledge in
  `Must Know`. Everything more detailed goes in the `references`
  subdirectory instead, indexed under `On-Demand References`.
- `references`: where the project's detailed knowledge actually lives.

## role rules

Path: `plato-workspace/role-rules`

Each role's rule files live under their own subdirectory: `designer/`,
`planner/`, `coder/`, `fixer/`.

# How ABR is produced

ABR grows in two ways:

1. You edit and maintain these ABR files by hand.
2. Every commit lock has a **New Rules** section. When you approve a
   commit lock, the agent takes whatever's new in **New Rules** and files
   it under the named file. For example, `COD.md: Don't repeat yourself`
   gets appended to `COD.md`.

# How ABR is used

ABR is **automatically** added as a prompt file to the command line the
guide session generates for you. For example:
`claude -p --session-id "...." --append-system-prompt-file ".plato/coder/CODER.md" ...`.
