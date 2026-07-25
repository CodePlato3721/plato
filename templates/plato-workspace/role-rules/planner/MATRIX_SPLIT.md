## Task Splitting: Matrix Splitting Method

Use the matrix splitting method. Draw a matrix of the changes this task touches, using the tech stack as columns and the business domains as rows — the tech stack is the horizontal split, and the business domains are the vertical split.

Example: a requirement adds a VIP membership badge to the system. The badge must appear on 3 pages — Dashboard, Account Settings, and Billing. These are 3 business domains. The badge needs to read the `user` table, going through the DAO layer, the Service layer, and the View layer. These are 3 tech stack layers.

Based on tech stack and business domain, draw a matrix:

```
              | Dashboard        | Account Settings        | Billing
--------------------------------------------------------------------------
View layer    | Dashboard view   | Account Settings view   | Billing view
--------------------------------------------------------------------------
Service layer | Dashboard service| Account Settings service| Billing service
--------------------------------------------------------------------------
DAO layer     | Dashboard dao    | Account Settings dao    | Billing dao
```

Because the first business domain is the first to touch every tech stack layer, it can be split into 3 tasks (one per layer). The 2nd and 3rd business domains build on what the 1st already established, so each of them only needs 1 task (not split by layer).

### Principles

- First split the matrix along tech stack (columns) and business domain (rows).
- Split the 1st business domain's tasks by tech stack layer into independent tasks.
- For subsequent business domains, do not split by tech stack layer — each business domain's remaining work is a single task.
