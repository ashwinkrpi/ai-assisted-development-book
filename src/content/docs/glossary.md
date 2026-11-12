# Glossary

Short definitions of the AI terms used in this book, plus a few you'll often meet in AI tool documentation. Each entry links to where the book explains the term in more detail.

---

### Agent {#agent}

An AI tool that works on a task in several steps on its own: it decides what to do next, uses [tools](#tool-use) such as reading files or running commands, looks at the results, and continues until the task is done or it needs your input. Agentic coding tools can edit files in your repository and run your tests. See [Chapter 0, Section 0.2](00-before-you-begin.md#02-three-kinds-of-ai-coding-tools) and [Chapter 4, Section 4.5](01-foundations/04-ai-assisted-software-development-lifecycle.md#45-working-with-ai-agents).

### Context window {#context-window}

The maximum amount of text, measured in [tokens](#token), that a model can take into account at once. It holds everything: the [system prompt](#system-prompt), your prompts, the conversation so far, pasted files, tool output, and the response being generated. When a conversation gets too long, the tool has to drop, summarize or reject part of it. See [Chapter 3, Section 3.4](01-foundations/03-understanding-large-language-models.md#34-tokens-and-context-windows).

### Fine-tuning {#fine-tuning}

Further training of an already-trained model on a smaller, focused set of examples, to adjust its behavior for particular tasks or styles. It changes the model's weights, unlike prompting. See [Chapter 3, Section 3.3](01-foundations/03-understanding-large-language-models.md#33-training-fine-tuning-and-inference).

### Hallucination {#hallucination}

Output that sounds fluent and confident but is wrong, such as a function, library or command-line flag that doesn't exist. Hallucinations are a side effect of how LLMs generate text, not a rare bug. See [Chapter 3, Section 3.5](01-foundations/03-understanding-large-language-models.md#35-why-hallucinations-happen).

### Inference {#inference}

Using a trained model to generate output. Every time you send a prompt and get a response, the model is running inference. Inference doesn't change the model; it doesn't learn from your conversation. See [Chapter 3, Section 3.3](01-foundations/03-understanding-large-language-models.md#33-training-fine-tuning-and-inference).

### LLM (large language model) {#llm}

A neural network trained on very large amounts of text and code to predict the next [token](#token) in a sequence. Repeating that prediction one token at a time produces answers, code and explanations. Most AI coding tools are built on an LLM. See [Chapter 3, Section 3.2](01-foundations/03-understanding-large-language-models.md#32-what-is-a-large-language-model).

### MCP (Model Context Protocol) {#mcp}

An open standard for connecting AI tools to other systems, such as databases, issue trackers or documentation, so an [agent](#agent) can use them as [tools](#tool-use). A program that offers tools this way is called an MCP server. See [modelcontextprotocol.io](https://modelcontextprotocol.io/).

### Prompt {#prompt}

The input you give an AI model: your question or instructions, plus any code, files or examples you include. See [Chapter 0, Section 0.5](00-before-you-begin.md#05-prompting-basics).

### RAG (retrieval-augmented generation) {#rag}

A technique where a tool first searches a collection of documents (for example, your codebase or internal docs) for passages relevant to your question, then adds them to the prompt so the model can base its answer on them. It helps the model use information it wasn't trained on, but the answer is still generated, so it can still be wrong.

### RLHF (reinforcement learning from human feedback) {#rlhf}

A training step in which people rate or compare a model's responses, and the model is trained to produce responses people rate more highly. Model providers use it, and related methods, to make models more helpful and safer. See [Chapter 3, Section 3.3](01-foundations/03-understanding-large-language-models.md#33-training-fine-tuning-and-inference).

### System prompt {#system-prompt}

Instructions given to the model before your own prompt, usually by the application rather than by you. They set its role, rules and behavior, such as "You are a coding assistant; never run destructive commands without asking." Context files such as `CLAUDE.md` or `AGENTS.md` are added to the model's context in a similar way. See [Chapter 4, Section 4.5](01-foundations/04-ai-assisted-software-development-lifecycle.md#45-working-with-ai-agents).

### Temperature {#temperature}

A setting that controls how random the model's choice of the next token is. Lower values make output more predictable; higher values make it more varied. Because most tools use some randomness, the same prompt can give different answers. See [Chapter 3, Section 3.2](01-foundations/03-understanding-large-language-models.md#32-what-is-a-large-language-model).

### Token {#token}

The unit of text a model works with: often a word, part of a word, or a piece of punctuation or whitespace. Context windows, usage limits and API prices are measured in tokens. Different models split text into tokens differently. See [Chapter 3, Section 3.2](01-foundations/03-understanding-large-language-models.md#32-what-is-a-large-language-model).

### Tool use {#tool-use}

A model's ability to ask the application to run an action on its behalf, such as searching the web, reading a file, running a command, or calling an API, and then use the result. Tool use is what lets an [agent](#agent) act on your project instead of only producing text. See [Chapter 3, Section 3.3](01-foundations/03-understanding-large-language-models.md#33-training-fine-tuning-and-inference).
