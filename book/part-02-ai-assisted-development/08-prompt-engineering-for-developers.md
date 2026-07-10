# Chapter 8 – Prompt Engineering for Developers

> *Good prompts are clear requirements. Great prompts are collaborative conversations.*

## Learning Objectives

- Structure prompts for software engineering tasks.
- Provide effective context to AI.
- Iterate on prompts to improve results.
- Avoid common prompting mistakes.

## Why Prompt Engineering Matters

AI models respond to the information you provide. Clear, structured prompts generally produce more accurate, maintainable, and useful results than vague requests.

Compare:

**Poor:** `Write a login system.`

**Better:**

```text
Act as a senior backend engineer.

Implement a JWT-based login service using FastAPI.

Requirements:
- PostgreSQL
- Password hashing with bcrypt
- Unit tests
- OpenAPI documentation

Explain design decisions before writing code.
```

## A Prompt Framework

A reliable engineering prompt contains:

1. Role
2. Goal
3. Context
4. Constraints
5. Expected output

## Iterative Prompting

Instead of asking for an entire application:

1. Clarify requirements.
2. Design the solution.
3. Implement one component.
4. Review.
5. Test.
6. Continue.

## Common Mistakes

- Vague requests
- Missing context
- Asking for too much at once
- Accepting the first answer without review

## Prompt Card

```text
You are a senior software engineer.

For every request:

- Clarify missing requirements.
- State assumptions.
- Explain trade-offs.
- Generate only the requested change.
- Recommend tests.
```

## Mini Lab

Choose an existing feature from one of your projects. Write three increasingly detailed prompts for the same task and compare the quality of the AI responses.

## Exercises

1. Rewrite three vague prompts into structured engineering prompts.
2. Explain why context improves AI output.
3. Describe when you would split one prompt into several smaller prompts.

## Summary

Prompt engineering is the skill of communicating engineering intent clearly. Small, iterative, context-rich prompts consistently produce better software outcomes than broad one-shot requests.
