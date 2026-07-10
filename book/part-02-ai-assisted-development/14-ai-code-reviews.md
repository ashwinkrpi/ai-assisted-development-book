# Chapter 14 – AI Code Reviews

> *AI can review every pull request in seconds, but human reviewers remain responsible for engineering decisions.*

## Learning Objectives

- Use AI to improve code reviews.
- Identify correctness, security, performance and maintainability issues.
- Write effective review prompts.
- Combine AI feedback with human judgement.

## Why Code Reviews Matter

Code reviews improve software quality, spread knowledge and reduce defects before deployment. AI can accelerate reviews by highlighting potential issues and suggesting improvements.

## AI Review Checklist

Ask AI to evaluate:

- Correctness
- Readability
- Maintainability
- Security
- Performance
- Error handling
- Test coverage
- Documentation

## Suggested Workflow

1. Read the change yourself.
2. Run automated tests.
3. Ask AI to review the diff.
4. Compare AI findings with your own observations.
5. Discuss significant issues with the author.
6. Approve only after verification.

## Example Prompt

```text
Act as a senior software engineer reviewing this pull request.

Review for:
- Bugs
- Security risks
- Performance issues
- Code style
- Missing tests
- Documentation gaps

Explain each recommendation and its impact.
```

## Common Pitfalls

- Accepting every AI suggestion.
- Ignoring business context.
- Optimising readability at the expense of correctness.
- Reviewing generated code without executing tests.

## Mini Lab

Review a recent pull request from one of your projects. Compare AI feedback with the comments from human reviewers and note where they agreed or differed.

## Exercises

1. List five review categories AI should always evaluate.
2. Explain why automated tests should run before code review.
3. Describe a situation where human reviewers should override AI feedback.

## Summary

AI makes code reviews faster and more consistent by surfacing issues that reviewers might overlook. The best reviews combine automated analysis, AI recommendations and experienced human judgement.
