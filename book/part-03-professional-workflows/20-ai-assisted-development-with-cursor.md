# Chapter 20 – AI-Assisted Development with Cursor

> *Repository-aware AI is most effective when it understands your codebase, your intent, and your engineering standards.*

## Learning Objectives

After completing this chapter you will be able to:

- Use Cursor as an AI-first development environment.
- Navigate large codebases with AI assistance.
- Perform safe, incremental refactoring.
- Review AI-generated changes before committing them.

---

## What Makes Cursor Different?

Cursor combines an editor with integrated AI capabilities that understand your project context. Instead of working only with the current file, Cursor can reason about related files and suggest changes across the codebase.

Typical use cases include:

- Understanding unfamiliar repositories
- Explaining project architecture
- Refactoring across multiple files
- Generating tests
- Updating documentation
- Fixing defects

---

## A Recommended Workflow

1. Open the project.
2. Ask Cursor to explain the architecture.
3. Identify the files affected by a change.
4. Implement one logical change.
5. Review the generated diff.
6. Run tests and static analysis.
7. Commit reviewed code.

Keep changes focused and easy to review.

---

## Working with Repository Context

Provide Cursor with:

- Project goals
- Coding standards
- Relevant modules
- Acceptance criteria

The better the context, the more accurate the recommendations.

---

## Reviewing AI Changes

Before accepting modifications:

- Read every changed file.
- Confirm coding standards.
- Execute automated tests.
- Review security implications.
- Ensure documentation is updated if behaviour changes.

---

## Prompt Card

```text
Act as a senior software engineer.

Before making changes:

1. Explain the current implementation.
2. Identify affected files.
3. Describe the proposed solution.
4. Implement one logical change.
5. Explain how to verify it.
```

---

## Mini Lab

Choose an existing feature.

Use Cursor to:

1. Explain the implementation.
2. Identify related files.
3. Refactor one module.
4. Generate tests.
5. Review the resulting changes before committing.

---

## Exercises

1. Explain the benefits of repository-aware AI.
2. List three tasks that Cursor can simplify.
3. Describe why incremental commits improve review quality.

---

## Summary

Cursor enables developers to work effectively with large repositories by combining editor productivity with project-aware AI. The best results come from providing clear context, making small changes, and validating every AI-generated modification.

## Next Chapter

Chapter 21 explores AI-assisted development with Claude, focusing on long-context reasoning, architectural analysis, and technical writing.
