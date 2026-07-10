# Chapter 12 – AI-Assisted Testing

> *Tests are the safety net of modern software development. AI can help write them, but developers must ensure they validate the correct behaviour.*

## Learning Objectives

After completing this chapter you will be able to:

- Use AI to design effective test strategies.
- Generate unit, integration, and regression tests.
- Identify edge cases and negative scenarios.
- Review AI-generated tests for quality and completeness.

---

## Why Testing Matters

Testing verifies that software behaves as expected and helps prevent regressions when changes are introduced. AI can accelerate test creation, allowing developers to focus on behaviour rather than boilerplate.

---

## Types of Tests

AI can assist with generating:

- Unit tests
- Integration tests
- Functional tests
- Regression tests
- Boundary and edge-case tests
- Negative test cases

Each type serves a different purpose and should be part of a balanced testing strategy.

---

## Test-Driven Thinking

Before generating implementation code, ask AI to help define the expected behaviour.

Example prompt:

```text
Review the following requirements.

Generate:
- Acceptance criteria
- Positive test cases
- Negative test cases
- Edge cases

Do not generate implementation code.
```

This approach helps clarify requirements before development begins.

---

## Reviewing AI-Generated Tests

Always check that generated tests:

- Verify observable behaviour.
- Avoid implementation details.
- Cover normal, boundary, and error conditions.
- Are readable and maintainable.

Remove redundant tests and improve names where necessary.

---

## Improving Test Coverage

AI can suggest additional scenarios such as:

- Invalid input
- Empty collections
- Large data sets
- Network failures
- Permission errors
- Timeouts

Use these suggestions to improve confidence in the application.

---

## Prompt Card

```text
Act as a senior software test engineer.

Given these requirements:

1. Identify acceptance criteria.
2. Generate unit tests.
3. Generate integration tests.
4. Suggest missing edge cases.
5. Explain what each test verifies.
```

---

## Mini Lab

Select an existing class from one of your projects.

Use AI to:

1. Review its behaviour.
2. Generate a comprehensive unit test suite.
3. Add negative tests.
4. Improve test readability.
5. Measure test coverage before and after.

---

## Exercises

1. Explain the difference between unit and integration testing.
2. List five edge cases AI might suggest for an API endpoint.
3. Review an AI-generated test suite and identify improvements.

---

## Summary

AI significantly reduces the effort required to create automated tests, but developers remain responsible for ensuring that tests accurately reflect business requirements and provide meaningful coverage. The strongest testing strategy combines AI-assisted generation with careful human review.
