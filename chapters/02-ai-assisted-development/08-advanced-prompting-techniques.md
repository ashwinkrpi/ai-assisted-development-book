# Chapter 8 -- AI-Assisted Debugging and Code Review

> **Goal:** Learn how to use AI effectively to debug, review, and
> improve software without replacing engineering judgment.

------------------------------------------------------------------------

# Learning Outcomes

After this chapter you will be able to:

-   Debug code with AI
-   Perform AI-assisted code reviews
-   Generate useful unit tests
-   Verify AI-generated fixes

------------------------------------------------------------------------

# 1. AI Debugging Workflow

Use this four-step workflow instead of asking **"Fix my code."**

``` text
Problem
↓
Context
↓
Error Message
↓
Expected Behaviour
```

Example prompt:

``` text
Role: Senior Python Engineer

Application:
Inventory API

Problem:
Creating an order returns HTTP 500.

Error:
IntegrityError: duplicate key value

Task:
Explain the root cause, suggest a fix,
update the code, and generate regression tests.
```

![Debug Workflow](images/ch08/debug-workflow.svg)

------------------------------------------------------------------------

# 2. AI Code Review

Ask AI to review code using a checklist.

``` text
Review this module for:

- Correctness
- Security
- Performance
- Readability
- Error handling
- Test coverage

Categorise findings as Critical,
High, Medium or Low.
```

------------------------------------------------------------------------

# 3. Generate Better Tests

Prompt:

``` text
Generate pytest tests covering:

- Happy path
- Invalid input
- Boundary cases
- Exceptions
- Mock external services
```

Always execute the generated tests locally before accepting them.

------------------------------------------------------------------------

# 4. Review → Fix → Verify

``` mermaid
flowchart LR
A[Source Code]-->B[AI Review]
B-->C[Developer Review]
C-->D[Apply Fix]
D-->E[Run Tests]
E-->F[Merge]
```

AI should support---not replace---human review.

------------------------------------------------------------------------

# Hands-on Lab

A FastAPI endpoint crashes with:

``` text
ValueError: Invalid UUID
```

Create a prompt asking the AI to:

1.  Explain the exception.
2.  Identify the faulty code.
3.  Suggest multiple fixes.
4.  Update the implementation.
5.  Generate regression tests.

------------------------------------------------------------------------

# Useful Commands

``` bash
pytest

pytest -v

ruff check .

black .

git diff

git commit -m "Fix order validation"
```

------------------------------------------------------------------------

# Suggested Screenshots

Include the following screenshots from your own environment:

1.  VS Code with the error highlighted.
2.  Terminal running `pytest`.
3.  Git diff after applying the AI-generated fix.
4.  Pull Request showing the final review.

------------------------------------------------------------------------

# Best Practices

-   Include the complete error message.
-   Mention framework and language versions.
-   Ask for an explanation before requesting a fix.
-   Verify every generated change.
-   Never merge AI-generated code without review.

------------------------------------------------------------------------

# Summary

AI can significantly reduce debugging and code review time when supplied
with sufficient context. Treat AI as a collaborative engineering
assistant, verify every recommendation, and rely on automated tests
before merging changes.
