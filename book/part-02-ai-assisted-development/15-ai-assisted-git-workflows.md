# Chapter 15 – AI-Assisted Git Workflows

> *AI can streamline Git workflows, but disciplined version control practices remain essential.*

## Learning Objectives

- Use AI to improve everyday Git workflows.
- Create meaningful commits and pull requests.
- Resolve merge conflicts with AI assistance.
- Generate release notes and changelogs.

## Git and AI

AI can help with:

- Writing commit messages
- Explaining Git errors
- Reviewing diffs
- Drafting pull request descriptions
- Summarising releases
- Resolving merge conflicts

## Recommended Workflow

1. Create a feature branch.
2. Implement small, reviewable changes.
3. Run tests.
4. Ask AI to review the diff.
5. Generate a concise commit message.
6. Open a pull request.
7. Review and merge.

## Commit Messages

Prefer descriptive commits:

```text
feat(auth): add password reset email validation

fix(api): handle null customer identifier

refactor(cache): simplify eviction strategy
```

## Merge Conflicts

Before accepting AI suggestions:

- Understand both versions.
- Preserve intended behaviour.
- Re-run tests.
- Review affected files.

## Prompt Card

```text
Act as an experienced Git reviewer.

Review this diff.

Suggest:
- A commit message
- Pull request summary
- Potential risks
- Follow-up tasks
```

## Mini Lab

Take a completed feature:

1. Create focused commits.
2. Ask AI to improve commit messages.
3. Generate a pull request description.
4. Produce release notes from the merged commits.

## Exercises

1. Rewrite three vague commit messages.
2. Explain why small commits simplify reviews.
3. Describe a safe process for resolving merge conflicts with AI.

## Summary

AI complements Git by improving communication and reducing routine effort, while developers remain responsible for repository history, review quality and release integrity.

## End of Part 2

You have now completed the core AI-assisted development workflows. The next part of the book focuses on professional development environments, enterprise workflows, and integrating multiple AI tools into real software engineering teams.
