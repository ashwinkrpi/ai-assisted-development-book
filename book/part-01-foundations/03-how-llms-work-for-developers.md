# Chapter 3 – How Large Language Models Work for Developers

> *You do not need to become a machine learning engineer to become an effective AI-assisted software developer. You do need to understand how LLMs think, where they excel, and where they fail.*

## Learning Objectives

After completing this chapter you will be able to:

- Explain what a Large Language Model (LLM) is.
- Understand tokens and context windows.
- Recognize why hallucinations occur.
- Write prompts that provide sufficient context.
- Work effectively with coding assistants.

---

## 1. What Is an LLM?

A Large Language Model is a neural network trained to predict the most likely next token in a sequence. Although this sounds simple, the model learns statistical relationships between words, source code, documentation, and many other forms of text.

An LLM is **not** a database of answers. It generates responses based on patterns learned during training and the context you provide.

---

## 2. Thinking in Tokens

Humans read words. LLMs process **tokens**.

A token may represent:

- a complete word
- part of a word
- punctuation
- source code symbols
- whitespace in some tokenizers

Longer conversations consume more tokens, reducing the amount of context available for new information.

### Practical Advice

- Keep prompts focused.
- Remove unnecessary information.
- Supply only the files needed for the current task.

---

## 3. Context Windows

The context window is the amount of information an LLM can consider when generating a response.

Think of it as the model's working memory.

When the context window is exceeded, older information may be dropped or summarized, reducing accuracy.

### Best Practices

- Work feature by feature.
- Provide architecture summaries for large projects.
- Reference specific files instead of entire repositories when possible.

---

## 4. Why Hallucinations Happen

Hallucinations occur when the model generates plausible but incorrect information.

Examples include:

- Inventing APIs
- Incorrect library versions
- Non-existent configuration options
- Fabricated citations

Never assume generated code is correct simply because it looks convincing.

---

## 5. Prompting for Better Results

Poor prompt:

```text
Write an API.
```

Improved prompt:

```text
Act as a senior backend engineer.

Build a REST API using FastAPI.

Requirements:
- JWT authentication
- PostgreSQL
- SQLAlchemy
- Unit tests
- OpenAPI documentation

Explain important design decisions before writing code.
```

The second prompt provides role, technology, constraints, and expected output.

---

## 6. LLMs as Engineering Partners

Use an LLM to:

- Explain unfamiliar code
- Brainstorm designs
- Generate test cases
- Review pull requests
- Improve documentation

Avoid delegating final engineering decisions without review.

---

## Prompt Card

```text
You are my senior software engineering reviewer.

Before answering:

1. Identify missing information.
2. State assumptions.
3. Explain trade-offs.
4. Suggest alternative approaches.
5. Then produce the implementation.
```

---

## Mini Lab

Take a small project from your computer.

Ask an AI assistant to:

1. Explain the architecture.
2. Identify dependencies.
3. Suggest three improvements.
4. Generate unit tests for one module.
5. Review the generated tests yourself.

Record which suggestions you accepted and which you rejected.

---

## Exercises

1. Explain the difference between a token and a word.
2. Why do context windows matter when working with large repositories?
3. Give three examples of AI hallucinations in software development.
4. Rewrite a vague coding prompt into a detailed engineering prompt.

---

## Summary

LLMs are powerful prediction engines that become valuable software engineering assistants when provided with clear context and carefully reviewed outputs. Understanding tokens, context windows, and hallucinations enables developers to collaborate with AI more effectively while maintaining responsibility for software quality.

## Next Chapter

Chapter 4 introduces the AI-Assisted Development Lifecycle and demonstrates how AI can support every phase of software delivery—from requirements through deployment.
