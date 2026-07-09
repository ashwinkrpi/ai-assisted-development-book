# Chapter 6 – Your First AI-Assisted Project

> *The best way to learn AI-assisted software development is to build a real project from idea to implementation.*

## Learning Objectives

After this chapter you will be able to:

- Break a project into manageable tasks.
- Use AI throughout the software development lifecycle.
- Review and refine AI-generated code.
- Produce tests and documentation before completion.

---

## Project Overview

In this chapter you'll build a simple command-line **Task Manager** application.

Features:

- Add a task
- List tasks
- Mark tasks as complete
- Delete tasks
- Save tasks to a local file

The application is intentionally small so that the focus remains on the workflow rather than the framework.

---

## Step 1 – Define Requirements

Before writing code, ask AI to review the requirements.

**Prompt**

```text
Review these requirements.

Identify:
- Missing requirements
- Edge cases
- Error conditions
- Suggested improvements

Do not generate code yet.
```

Refine the requirements based on the feedback before moving to implementation.

---

## Step 2 – Design the Solution

Ask AI to suggest a simple architecture.

Possible components:

- Command-line interface
- Task model
- Storage layer
- Service layer

Review the design and simplify where appropriate.

---

## Step 3 – Implement Incrementally

Instead of requesting the whole application, build it feature by feature.

Recommended order:

1. Task model
2. Storage
3. Add command
4. List command
5. Complete command
6. Delete command

Review every change before accepting it.

---

## Step 4 – Testing

Generate:

- Unit tests
- Invalid input tests
- File handling tests
- Regression tests

Run the tests locally and correct any failures before proceeding.

---

## Step 5 – Documentation

Ask AI to generate:

- README
- Installation guide
- Usage examples
- Command reference

Verify that the documentation matches the implementation.

---

## Step 6 – Code Review

Perform a final review.

Checklist:

- Naming consistency
- Error handling
- Security
- Test coverage
- Readability

Treat AI as another reviewer, not the final authority.

---

## Prompt Card

```text
Act as a senior software engineer.

Guide me through this project one phase at a time.

For each phase:

1. Explain the objective.
2. Identify risks.
3. Generate only the required code.
4. Wait for review before continuing.
```

---

## Mini Lab

Extend the Task Manager by adding:

- Search
- Due dates
- Priorities
- Sorting

Use AI to propose the design first, then implement each enhancement incrementally.

---

## Exercises

1. Replace file storage with SQLite.
2. Add automated tests for new features.
3. Create a GitHub Actions workflow that runs the tests.
4. Generate API-style documentation for the project.

---

## Summary

This chapter demonstrated a complete AI-assisted development workflow—from requirements to implementation, testing, documentation, and review. The key lesson is that successful AI-assisted development is iterative, review-driven, and centred on engineering judgement rather than one-shot code generation.

## End of Part 1

Congratulations! You have completed the Foundations section. In Part 2 you will explore advanced day-to-day development workflows including pair programming, prompt engineering, debugging, refactoring, testing, documentation, and code reviews using AI.
