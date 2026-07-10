# Chapter 11 – Debugging with AI

> *AI can help you investigate failures, but disciplined debugging remains an engineering skill.*

## Learning Objectives

- Use AI to investigate defects.
- Analyse stack traces and logs effectively.
- Identify likely root causes.
- Verify fixes with tests.

## A Structured Debugging Workflow

1. Reproduce the issue.
2. Gather logs, stack traces and inputs.
3. Ask AI to explain the failure.
4. Form hypotheses.
5. Apply one fix at a time.
6. Verify with automated tests.
7. Review the final change.

## Analysing Errors

Provide AI with:

- Error messages
- Relevant source code
- Runtime environment
- Expected behaviour
- Actual behaviour

Avoid sharing secrets or production credentials.

## Root Cause Analysis

Ask AI to distinguish symptoms from causes.

Example prompt:

```text
Act as a senior software engineer.

Given this stack trace and source code:

- Explain what failed.
- List likely root causes.
- Rank them by probability.
- Suggest how to verify each hypothesis before changing the code.
```

## Verifying the Fix

After applying a fix:

- Reproduce the original scenario.
- Run regression tests.
- Check related functionality.
- Review performance and security impacts.

## Prompt Card

```text
Analyse this defect.

Explain:
1. Symptoms
2. Likely root causes
3. Diagnostic steps
4. Recommended fix
5. Regression tests
```

## Mini Lab

Choose a previously fixed bug from one of your projects. Recreate the debugging process with AI, compare its diagnosis with the original fix, and record any additional insights.

## Exercises

1. Explain why reproducing a bug is the first debugging step.
2. List three types of information that improve AI debugging assistance.
3. Describe the difference between a symptom and a root cause.

## Summary

AI accelerates debugging by helping engineers interpret logs, understand stack traces and evaluate possible fixes. The final responsibility for identifying the true root cause and validating the solution remains with the development team.
