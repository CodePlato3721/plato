## Change Granularity Rules (CR Rules)

### Granularity

Keep each change small-grained. Criteria for granularity:

- **One-sentence summary check**: The Design (feature) or Solution (defect) in a CR must be summarizable in one short sentence. If it takes a list of items to describe, the change is too large and should be split.
- **Changes must be closed**: Every change must include a way to verify it, ensuring no broken code is submitted and then patched later. Verification priority:
  1. The project already has **unit tests** for the affected layer → update them alongside the change; write a test summary in the CR's Test Details.
  2. The project already has **end-to-end tests** → update them alongside the change; write a test summary in the CR's Test Details.
  3. No automated tests → describe **manual verification steps** clearly in the CR's Test Details — tell the user which command to run or what action to take to confirm the change is correct.
  4. Even manual verification is hard (e.g. the change depends on an external environment that isn't ready yet) → include **temporary scaffolding code** in this change; note "remove scaffolding in next change" in the CR; remove it in the next CR.

### CR Format

CRs come in two types: feature and defect.

**Source Tree** and **Test Tree** must use ASCII file-tree format — a single sentence is not acceptable, for example:
```
project/
├── src/
│   └── service.py    ← updated
└── tests/
    └── test_service.py    ← new
```

**feature**
- **Design**: Summary of this change's design
- **Source Details**: Core source-code detail, 1–2 lines of code, brief, excluding test changes
- **Source Tree**: ASCII tree of source files changed in this change
- **Test Details**: Summary of test changes. See **CR Testing Methods** below
- **Test Tree**: ASCII tree of test files changed in this change; see **CR Testing Methods** below
- **Test Result**: Test outcome. See **CR Testing Methods** below
- **New Rules**: Format `<rule file>: <rule text>`, one rule per line. Leave empty if there are no new rules.

**defect**
- **Root Cause**: Root cause of the defect
- **Solution**: Summary of the fix
- **Source Details**: Core source-code detail, 1–2 lines of code, brief, excluding test changes
- **Source Tree**: ASCII tree of source files changed in this change
- **Test Details**: Summary of test changes. See **CR Testing Methods** below
- **Test Tree**: ASCII tree of test files changed in this change; see **CR Testing Methods** below
- **Test Result**: Test outcome. See **CR Testing Methods** below
- **New Rules**: Format `<rule file>: <rule text>`, one rule per line. Leave empty if there are no new rules.

### CR Testing Methods

Available testing methods in a CR: unit tests, end-to-end tests, and manual testing. Each is handled differently.

**Unit tests**
The agent adds or updates unit tests in the directory given by the `unit-test-path` resolved in CODER.md's Step 1: Prepare Task, runs the tests, and writes a result summary to Test Result (pass/fail counts, failure reasons).
- **Test Details**: Summary of the test purpose and approach for this change
- **Test Tree**: ASCII tree of test files changed in this change
- **Test Result**: Unit test results

**End-to-end tests**
The agent adds or updates end-to-end tests in the directory given by the `e2e-test-path` resolved in CODER.md's Step 1: Prepare Task.
- **Test Details**: Summary of the test purpose and approach for this change
- **Test Tree**: ASCII tree of test files changed in this change
- **Test Result**: End-to-end test results

**Manual testing**
When automated tests cannot cover the change, describe clearly how to test it manually: which commands to run, or which service to start, what URL to open in the browser, and what result indicates success.
- **Test Details**: Manual testing steps (commands, or service to start + URL to open + success criteria)
- **Test Tree**: `No changes`
- **Test Result**: `Pending manual verification — see Test Details`
