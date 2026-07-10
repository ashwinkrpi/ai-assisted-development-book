# Chapter 10 – Refactoring Legacy Code with AI

> *Most developers spend more time understanding and improving existing code than writing new code. AI can dramatically accelerate this process when used responsibly.*

## Learning Objectives

- Analyze unfamiliar code with AI.
- Identify code smells and technical debt.
- Plan safe, incremental refactoring.
- Verify behavioural equivalence after changes.

---

## Understanding Before Changing

Before modifying legacy code, ask AI to explain:

- The purpose of the module
- Inputs and outputs
- Dependencies
- Control flow
- Potential side effects

Avoid requesting refactoring until you understand the existing behaviour.

---

## Identifying Code Smells

Use AI to detect:

- Long methods
- Large classes
- Duplicate logic
- Tight coupling
- Excessive nesting
- Poor naming
- Dead code

Prioritize issues by risk and business impact.

---

## Planning the Refactoring

Generate a step-by-step plan instead of one large rewrite.

Example phases:

1. Add tests.
2. Rename variables.
3. Extract helper methods.
4. Remove duplication.
5. Simplify logic.

Each step should be independently reviewable.

---

## Verifying Behaviour

Generate:

- Regression tests
- Boundary tests
- Negative tests

Run all tests after every refactoring step.

---

## Prompt Card

```text
You are a senior software engineer.

Analyse this legacy code.

Explain:
- Purpose
- Data flow
- Dependencies
- Code smells

Then propose a sequence of safe, incremental refactoring steps without changing behaviour.
```

---

## Mini Lab

Choose a class from an existing project.

Use AI to:

1. Explain the code.
2. Identify technical debt.
3. Create a refactoring plan.
4. Perform one refactoring.
5. Verify behaviour with tests.

---

## Exercises

1. List five common code smells.
2. Explain why incremental refactoring is safer than a complete rewrite.
3. Describe how AI can assist without replacing engineering judgement.

---

## Summary

AI is an excellent assistant for understanding and modernising legacy systems, but successful refactoring still depends on disciplined engineering, automated testing, and careful review.
