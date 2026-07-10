# Chapter 19 – AI-Assisted Development with GitHub Copilot

> *Inline suggestions are most valuable when they complement your thinking rather than replace it.*

## Learning Objectives

After completing this chapter you will be able to:

- Use GitHub Copilot effectively for day-to-day development.
- Combine inline completions with chat-based assistance.
- Generate tests, documentation, and refactorings.
- Review Copilot suggestions before accepting them.

---

## Understanding GitHub Copilot

GitHub Copilot integrates directly into supported IDEs and provides context-aware code suggestions. Unlike conversational AI tools, Copilot primarily assists while you write code, helping maintain flow and reduce repetitive typing.

Typical uses include:

- Completing functions
- Generating boilerplate
- Suggesting unit tests
- Writing documentation comments
- Refactoring repetitive code

---

## Recommended Workflow

1. Understand the requirement.
2. Write function signatures and comments.
3. Allow Copilot to suggest implementations.
4. Review every suggestion.
5. Run tests.
6. Refine the implementation.
7. Commit reviewed code.

Avoid accepting large suggestions without understanding them.

---

## Using Copilot Chat

When available, Copilot Chat can:

- Explain existing code
- Suggest improvements
- Generate test cases
- Help debug issues
- Summarize pull requests

Use chat to explore alternatives before making significant architectural changes.

---

## Reviewing Suggestions

Before accepting generated code:

- Check correctness.
- Verify coding standards.
- Consider security implications.
- Ensure consistency with the existing codebase.
- Confirm adequate test coverage.

---

## Prompt Card

```text
Act as my senior software engineer.

Review this function and:

1. Explain what it does.
2. Identify improvements.
3. Suggest tests.
4. Recommend a cleaner implementation if appropriate.
```

---

## Mini Lab

Implement a small feature using GitHub Copilot.

Record:

- Which suggestions you accepted.
- Which you rejected.
- Why you made each decision.
- Whether manual changes improved the final implementation.

---

## Exercises

1. List three situations where Copilot accelerates development.
2. Explain why reviewing generated code is essential.
3. Compare inline completion with conversational AI assistance.

---

## Summary

GitHub Copilot improves developer productivity by reducing repetitive work and providing context-aware suggestions. Developers achieve the best results by treating Copilot as a coding partner while maintaining responsibility for design, correctness, testing, and maintainability.

## Next Chapter

Chapter 20 explores AI-assisted development with Cursor and compares editor-centric AI workflows with conversational and agentic approaches.
