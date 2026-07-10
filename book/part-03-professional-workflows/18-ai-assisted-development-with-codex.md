# Chapter 18 – AI-Assisted Development with Codex

> *Agentic coding tools can automate repetitive implementation tasks, but they are most effective when guided by clear engineering intent.*

## Learning Objectives

After completing this chapter you will be able to:

- Understand where Codex fits into a professional development workflow.
- Delegate well-defined implementation tasks to an AI coding agent.
- Review AI-generated changes before accepting them.
- Integrate agentic coding into an existing Git workflow.

---

## What Is Codex?

Codex is designed to assist with software development by understanding codebases, generating changes, and helping implement engineering tasks. It works best when given clear objectives, relevant project context, and well-defined boundaries.

Typical use cases include:

- Implementing small features
- Refactoring modules
- Generating tests
- Updating documentation
- Fixing straightforward defects

---

## Recommended Workflow

1. Understand the requirement.
2. Create or update a design.
3. Ask Codex to implement one logical change.
4. Review the generated diff.
5. Run tests and static analysis.
6. Commit reviewed changes.

Avoid asking for large, multi-feature implementations in a single request.

---

## Writing Effective Tasks

A good Codex task includes:

- Objective
- Relevant files
- Constraints
- Acceptance criteria
- Definition of done

Example:

```text
Implement password reset email validation.

Constraints:
- Do not modify authentication flow.
- Preserve existing APIs.
- Add unit tests.
- Update documentation.
```

---

## Reviewing Generated Changes

Before merging:

- Read every modified file.
- Confirm coding standards.
- Execute automated tests.
- Check performance and security implications.
- Verify documentation updates.

---

## Prompt Card

```text
Act as a senior software engineer.

Implement only the requested task.

Before making changes:
1. Summarize the requirement.
2. List assumptions.
3. Describe affected files.
4. Implement incrementally.
5. Explain how to verify the result.
```

---

## Mini Lab

Choose a small feature from an existing project.

Use Codex to:

1. Plan the implementation.
2. Modify one module.
3. Generate tests.
4. Review the diff.
5. Commit the approved changes.

---

## Exercises

1. List three tasks that are well suited to Codex.
2. Explain why review is essential before merging AI-generated code.
3. Write an implementation task with clear acceptance criteria.

---

## Summary

Codex is most valuable when used as an engineering assistant operating within a disciplined workflow. Small, reviewable tasks combined with automated testing and human oversight produce reliable, maintainable software.

## Next Chapter

Chapter 19 explores AI-assisted development with GitHub Copilot and compares inline code completion with conversational and agentic workflows.
