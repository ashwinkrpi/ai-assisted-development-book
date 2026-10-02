# Chapter 0 — Before You Begin

> *You don't need to understand everything about AI to start using it well. You need to know what kind of tool you're holding, what it can see, and how to check its work.*

## Learning Objectives

By the end of this chapter, you will be able to:

- Tell apart the three main kinds of AI coding tools, and say what each one is good for.
- Choose a tool to start with, set it up, and understand roughly what it costs.
- Check the privacy settings that matter before you use AI on real code.
- Write a basic prompt that gives the AI context, a goal and constraints.
- Complete a first short exercise: ask an AI tool to explain some code, and check whether it was right.

---

## 0.1 Who This Book Is For

This book is for developers who have written some code but are new to using AI tools in their work. You don't need any background in machine learning.

You will get the most from it if you already know:

| Skill | Enough to… | If you're new to it |
|---|---|---|
| Basic Python | Read and write small functions, run a script, install a package with `pip` | [The official Python tutorial](https://docs.python.org/3/tutorial/) |
| Git | Clone a repository, commit, and push | [*Pro Git*, chapters 1–3](https://git-scm.com/book/en/v2) and [GitHub's Hello World guide](https://docs.github.com/en/get-started/start-your-journey/hello-world) |
| The command line | Move between folders, run commands, read their output | [MDN's command line crash course](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Environment_setup/Command_line) and [The Missing Semester](https://missing.csail.mit.edu/) |

If a term in this book is new to you, check the [Glossary](glossary.md). Terms are linked to it the first time they appear in each chapter.

---

## 0.2 Three Kinds of AI Coding Tools

Most AI coding tools are built on a [large language model (LLM)](glossary.md#llm): a program trained on huge amounts of text and code that generates new text in response to your input, which is called a [prompt](glossary.md#prompt). Chapter 3 explains how LLMs work. For now, what matters is how the tool around the model lets you use it. There are three main kinds.

**Chat assistants.** You type a question or paste some code into a chat window, and the AI replies. Examples include the chat apps for Claude, ChatGPT and Gemini, and the chat panels built into editors. They're good for explaining code, discussing designs, and drafting small pieces of code. The AI only sees what you paste in, and you copy its answers back into your project yourself.

**Inline autocomplete.** As you type in your editor, the tool suggests the rest of the line or the next few lines, and you accept a suggestion with a key press. Examples include GitHub Copilot's code completions and the autocomplete in editors such as Cursor and JetBrains IDEs. Autocomplete is good for repetitive code and for finishing a pattern you've started. Because suggestions arrive constantly and look like your own code, it's easy to accept them without reading them carefully.

**Agentic tools.** You describe a task, and the tool works on it in several steps: it reads files in your repository, runs commands such as your tests, and edits files itself. Examples include Claude Code, Cursor's agent, and GitHub Copilot's agent mode. A tool that acts like this is called an [agent](glossary.md#agent). Agents can complete larger tasks, but they can also make more changes, faster, than you can easily check.

| Kind | What the AI can see | Who changes your files | How much to trust it |
|---|---|---|---|
| Chat assistant | Only what you paste in | You | Read every answer; it can't see the rest of your project, so it may guess |
| Inline autocomplete | The file you're editing and some nearby context | You, by accepting suggestions | Read each suggestion before accepting it, as if you'd typed it yourself |
| Agentic tool | Your repository, plus command output | The agent, usually after asking you | Review every change as a diff before you keep it (Chapter 4, Section 4.5) |

None of these kinds is "the best." Many developers use all three: chat to think through a problem, autocomplete while typing, and an agent for a well-defined task. This book's workflow applies to all of them. The more a tool can do on its own, the more carefully you need to review what it did.

---

## 0.3 Choosing and Setting Up a Tool

To work through this book you need access to at least one AI tool. A chat assistant is enough for most labs; Chapters 4 to 6 are easier with a tool that works inside your editor or repository.

**Accounts and cost.** Most tools need an account. Many have a free tier with usage limits, which is enough to get started. Paid individual plans for popular tools cost roughly US$10–20 per month as of late 2026; for example, GitHub Copilot Pro is $10 per month, and Claude Pro and Cursor's individual plan are $20 per month. Higher tiers with more usage cost more. Prices and limits change often, so check the tool's pricing page before you sign up.

**Running models locally.** You can also run an open model on your own computer with a tool such as [Ollama](https://ollama.com/download). This costs nothing beyond your hardware, and your code never leaves your machine. The trade-off is that local models are usually smaller and less capable than the largest cloud models, and they run slowly without a capable GPU. Chapter 5, Section 5.6 sets up a local model on a Raspberry Pi 5.

**A sensible starting point.** If you're unsure, start with the free tier of one chat assistant and one editor-integrated tool. Use them for a few weeks before paying for anything. You'll learn more from using one tool carefully than from trying many.

---

## 0.4 Privacy Settings to Check First

Anything you send to a cloud AI tool leaves your computer. Before you use a tool on code that isn't yours alone, check these settings and policies:

- **Training on your data.** Some consumer plans may use your conversations and code to improve their models unless you turn that off. Business and API plans usually have stricter defaults. Find the setting and decide deliberately.
- **Data retention.** How long does the provider keep your prompts and code?
- **What the tool can read.** Editor and agentic tools can read files in your project, including files you'd never paste into a chat, such as `.env` files containing passwords or API keys.
- **Your employer's rules.** Many companies only allow approved tools, or require a company account rather than a personal one. Check before using AI on work code.

Chapter 5, Section 5.5 covers security in more detail, including keeping secrets out of prompts and out of your repository.

---

## 0.5 Prompting Basics

A prompt is everything you give the AI to work with. You don't need special tricks to write a good one. You need to give the AI the same information you'd give a new colleague who has never seen your project. Part 2 of this book covers prompting in depth; these five habits are enough to start.

1. **Give context.** Say what the code is for, which language and libraries you're using, and paste the relevant code. The AI can't see anything you don't show it (unless your tool reads your files for you).
2. **State the goal.** Say what you want to end up with, and what "done" looks like.
3. **Add constraints.** Say what must not change, which style to follow, and anything to avoid.
4. **Ask for assumptions.** Ask the AI to list what it's assuming before it writes code, so you can correct misunderstandings early.
5. **Iterate.** Treat the first answer as a draft. Point out what's wrong or missing and ask again, rather than starting over or accepting something that isn't right.

Here's a weak prompt and a better one for the same task:

```
Write a function to parse dates.
```

```
I'm writing a Python 3.12 script that reads a CSV export from our billing
system. The "created" column contains dates like "03/10/2026" (day/month/year).

Write a function parse_created(value: str) -> datetime.date that parses one
of these values. Use only the standard library. If the value is empty or
invalid, raise ValueError with a message that includes the bad value.

Before writing the code, list any assumptions you're making about the input.
```

The second prompt tells the AI the language version, the input format (which is ambiguous without it: `03/10/2026` could be March or October), the exact function signature, a constraint (standard library only), the error behavior, and asks for assumptions. Each of those removes a guess the AI would otherwise make.

---

## 0.6 How to Read This Book

Chapter 1 introduces the four principles and the eight-step workflow that the rest of the book is built on. Chapters 2 and 3 explain why AI is changing software development and how LLMs work. Chapters 4 and 5 apply the workflow to the development lifecycle and to your tools. Chapter 6 brings it together in a complete project.

Each chapter ends with a hands-on lab. Do them: the habits this book teaches come from practice, not from reading.

---

## Engineering Insight

> The more an AI tool can do on its own, the more carefully you need to check what it did.

---

## Common Mistakes

- Pasting secrets, customer data or company code into a tool before checking its privacy settings and your employer's policy.
- Assuming a chat assistant can see your project. It only sees what you paste in.
- Accepting autocomplete suggestions without reading them because they "look right."
- Letting an agent make large changes and accepting them without reviewing the diff.
- Paying for several tools before learning to use one well.

---

## Hands-On Lab: Ask an AI to Explain Code, Then Check It

This lab takes about ten minutes.

1. Pick a short file (20–50 lines) from a project you know well, so you can judge the answer. If you don't have one, use any small Python file from an open-source project you understand.
2. Paste it into an AI chat assistant with this prompt:

    ```
    Explain what this code does, step by step. Then list anything that looks
    like a bug or an edge case it doesn't handle. If you're unsure about
    something, say so.

    [paste the code]
    ```

3. Read the explanation and check each claim against the code. For each one, note whether it's correct, partly correct, or wrong.
4. Check the possible bugs it found. Are they real? Did it miss any you know about?
5. Write two or three sentences on what you'd trust this tool to do without checking, and what you'd always check.

Keep your notes. Chapter 1's lab asks you to start a development journal, and this can be its first entry.

---

## Chapter Summary

AI coding tools come in three main kinds: chat assistants, inline autocomplete, and agentic tools that work in your repository. They differ in what the AI can see and who changes your files, and the more a tool does on its own, the more review it needs. Before using any of them on real code, check its privacy settings and your employer's rules. Good prompts give the AI context, a goal and constraints, ask for its assumptions, and treat the first answer as a draft.

---

## Review Questions

1. What are the three main kinds of AI coding tools, and what can the AI see in each?
2. Why does an agentic tool need more careful review than a chat assistant?
3. What are the trade-offs of running a model locally instead of using a cloud tool?
4. Name three privacy questions to answer before using an AI tool on work code.
5. Rewrite this prompt using the five prompting habits: "Fix my login function."

---

## Further Reading

- [Anthropic: prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview). Most of its advice applies to any model.
- [Ollama](https://ollama.com/download), for running open models locally.

---

## Next Chapter

Chapter 1 introduces AI-assisted software development: what it is, the four principles behind this book, and the eight-step workflow you'll use in every chapter that follows.
