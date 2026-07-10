# Chapter 21 – AI-Assisted Development with Claude

> *Long-context reasoning enables AI to analyse large codebases, architecture documents, and technical specifications with greater continuity.*

## Learning Objectives

After completing this chapter you will be able to:

- Use Claude for architecture reviews and design discussions.
- Analyse large documents and repositories effectively.
- Compare long-context reasoning with editor-centric AI workflows.
- Validate AI recommendations before implementation.

---

## Why Use Claude?

Claude is particularly useful for tasks that require understanding substantial amounts of information at once, such as:

- Architecture documents
- Design proposals
- Requirements specifications
- Large code reviews
- Technical documentation
- Migration plans

Rather than focusing only on code generation, Claude excels at analysis and explanation.

---

## A Recommended Workflow

1. Gather relevant documentation.
2. Provide architectural context.
3. Ask Claude to summarise the system.
4. Identify risks and trade-offs.
5. Refine the design.
6. Implement changes using your preferred coding tools.
7. Review and validate the results.

---

## Effective Prompts

Provide:

- Business context
- Technical constraints
- Architecture diagrams (when available)
- Relevant interfaces
- Acceptance criteria

Ask Claude to explain assumptions before proposing solutions.

---

## Reviewing Recommendations

Before acting on AI suggestions:

- Confirm alignment with requirements.
- Evaluate scalability.
- Consider operational impacts.
- Verify security implications.
- Discuss significant architectural changes with the team.

---

## Prompt Card

```text
Act as a principal software architect.

Review this architecture.

Provide:
1. A concise summary.
2. Strengths.
3. Risks.
4. Alternative approaches.
5. Recommendations ranked by priority.
```

---

## Mini Lab

Take an existing architecture document.

Use Claude to:

1. Summarise the architecture.
2. Identify technical risks.
3. Recommend improvements.
4. Highlight missing documentation.
5. Produce an executive summary for stakeholders.

---

## Exercises

1. Explain why long-context reasoning is useful for architecture reviews.
2. Compare conversational analysis with inline code completion.
3. Identify three engineering tasks that benefit from analysing large documents.

---

## Summary

Claude is well suited to software engineering activities that involve understanding complex systems, evaluating design decisions, and communicating technical information. Combined with coding-focused tools, it becomes a valuable part of a professional AI-assisted development workflow.

## Next Chapter

Chapter 22 explores AI-assisted development with Gemini and discusses multimodal workflows, research, and integrating external information into software engineering.
