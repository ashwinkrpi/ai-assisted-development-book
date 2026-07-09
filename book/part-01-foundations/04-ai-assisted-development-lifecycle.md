# Chapter 4 – The AI-Assisted Development Lifecycle

> *AI delivers the most value when it is integrated into every stage of software development rather than treated as a code generator.*

## Learning Objectives

After completing this chapter you will be able to:

- Map AI capabilities to each phase of the SDLC.
- Apply AI to requirements, design, implementation, testing, deployment, and operations.
- Build an iterative workflow with human review at every stage.
- Identify appropriate prompts for each engineering activity.

---

## 1. Introduction

Traditional software development follows a lifecycle that transforms ideas into reliable software. AI enhances this lifecycle by accelerating routine tasks, improving communication, and surfacing insights. It does **not** replace engineering discipline.

---

## 2. AI Across the SDLC

```text
Requirements
    ↓
Analysis
    ↓
Architecture
    ↓
Implementation
    ↓
Testing
    ↓
Documentation
    ↓
Code Review
    ↓
Deployment
    ↓
Operations
```

Every stage benefits from different prompting techniques and different levels of human oversight.

---

## 3. Requirements and Analysis

Use AI to:

- Clarify ambiguous requirements.
- Identify missing acceptance criteria.
- Suggest edge cases.
- Draft user stories.

**Prompt**

```text
Review these requirements.
Identify ambiguities, missing business rules, risks and questions that should be answered before development starts.
```

---

## 4. Architecture and Design

AI can compare architectural options and explain trade-offs.

Typical tasks:

- Component decomposition
- API design
- Database modelling
- Technology selection
- Sequence diagrams

Engineers should validate scalability, security and operational requirements before implementation.

---

## 5. Implementation

Instead of requesting an entire application, build incrementally.

Recommended workflow:

1. Create interfaces.
2. Implement one feature.
3. Review the result.
4. Add tests.
5. Refactor.

Smaller prompts usually produce better results.

---

## 6. Testing

AI can generate:

- Unit tests
- Integration test ideas
- Boundary cases
- Negative tests
- Regression test suggestions

Always review generated tests to ensure they verify behaviour rather than implementation details.

---

## 7. Documentation

Generate:

- API documentation
- README files
- Architecture summaries
- Release notes
- User guides

Documentation should evolve together with the codebase.

---

## 8. Code Review

Ask AI to review changes for:

- Bugs
- Security issues
- Performance
- Readability
- Maintainability

Treat AI as an additional reviewer—not the final approver.

---

## 9. Deployment and Operations

AI can assist with:

- Dockerfiles
- CI/CD pipelines
- Infrastructure as Code
- Log analysis
- Incident summaries
- Runbooks

Production decisions remain a human responsibility.

---

## Best Practices

- Keep prompts focused.
- Review every generated artifact.
- Preserve small, reviewable commits.
- Use automated tests.
- Protect confidential information.

---

## Prompt Card

```text
Act as a senior software architect.

For the following feature:

1. Clarify requirements.
2. Identify risks.
3. Propose an architecture.
4. Explain trade-offs.
5. Generate implementation incrementally.
6. Recommend tests.
7. Produce documentation.
```

---

## Mini Lab

Choose a small feature and apply AI during every SDLC phase:

- Requirements
- Design
- Coding
- Testing
- Documentation
- Review

Record where AI saved the most effort and where manual intervention was required.

---

## Exercises

1. Match three AI use cases to three SDLC phases.
2. Explain why incremental implementation is preferable to one-shot code generation.
3. Describe two situations where AI should not make the final decision.

---

## Summary

AI-assisted development is a workflow, not a single prompt. Teams gain the most value when AI supports every stage of delivery while engineers remain accountable for quality, security and business outcomes.

## Next Chapter

Chapter 5 focuses on setting up a modern AI-assisted development environment, including IDEs, terminal tools, version control, and best practices for integrating AI into your daily workflow.
