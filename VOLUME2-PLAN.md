# Volume 2 Build Plan — Part 2: Prompting and Core Development Tasks

Run with somaari-build-guru from the repository root on a clean tree:
`build-guru run VOLUME2-PLAN.md --dry-run`, then `build-guru run VOLUME2-PLAN.md`. The run works on its own `build-guru/VOLUME2-PLAN` branch and never merges or pushes. The check after each task is `sh scripts/check.sh`.

**Scope:** Chapters 7–15 as listed in the README, in a new folder `src/content/docs/02-prompting-and-core-tasks/`. Volume 1 stays as it is except for links and the sidebar.

**Status key:** `[ ]` open · `[x]` done. Tags: `[simple]` haiku · `[moderate]` sonnet · `[complex]` opus · `[manual]` Ashwin (the run pauses and asks).

## Rules for this plan

These are the book's rules from `CLAUDE.md`, with what they mean for Volume 2.

1. **Never invent output.** Every block of AI replies, terminal output or test output comes from a real run. A screenshot is a real capture, never a mock-up. A task that needs a real AI session or a real UI is `[manual]` and sits *before* the tasks that use its result, so the run pauses there.
2. **Code in chapters matches `examples/`.** Run `python3 scripts/check_examples.py` and the example's tests after each code task.
3. **Facts that change** (tool names, menu paths, versions, prices) are checked against current official docs. Screenshots of tool interfaces go out of date fast: caption each with the tool, its version and the month, and prefer a text block when a screenshot adds nothing.
4. **Sources** for any claim about productivity or research go into the chapter's Further Reading.
5. **No tool by brand alone.** Examples may use one tool, labeled as an example of its kind (Chapter 0 §0.2).
6. **New readers.** Explain each term on first use and link the glossary (`/glossary/#id`).
7. Follow the style and chapter template in `CLAUDE.md`: American spelling, `## N.M Title`, no `#` heading, `{#id}` anchors only where needed, and this section order: Learning Objectives, numbered sections, Engineering Insight, Common Mistakes, Hands-On Lab, Chapter Summary, Review Questions, Further Reading, Next Chapter.
8. Each chapter's front matter gets `draft: true` until its review task. Nothing in Volume 2 is published until the release stage.

## How images, screenshots and diagrams work in this volume

| Kind | How it is made | Where it lives | Who |
|---|---|---|---|
| Diagram | A `mermaid` fence in the chapter. No colors; `src/styles/somaari.css` themes it. | In the chapter | build-guru |
| Screenshot of a tool UI | A real capture, PNG, at most 1,200 px wide and 300 KB. Cropped to the relevant area. No account names, emails, API keys, tokens or private file paths visible. | `src/assets/chNN/chNN-name.png` | Ashwin (`[manual]`) |
| Terminal output | A fenced `text` block pasted from a real run. Not a screenshot, so it can be searched and read by a screen reader. | In the chapter | build-guru, from Ashwin's real run |
| Session transcript | The verbatim AI session, saved for the worked example. | `transcripts/chNN-*.md` (not published) | Ashwin (`[manual]`) |

Every image is inserted as `![Alt text that says what it shows](../../../assets/chNN/name.png)` followed by an italic caption line: what it shows, the tool and version, and the month captured. Alt text describes the content, not "screenshot of". The CSP allows images from the site itself (`img-src 'self' data:`), so no external image hosts.

**Screenshot setup for Ashwin.** Use one clean browser profile or editor profile with no personal data. Use the light theme, 100% zoom, and the same window width for the whole volume so the screenshots look alike. Capture the relevant region, not the whole screen.

## Decisions

- [ ] [manual] D1: Which project do the Volume 2 examples build on? Recommended: continue the Chapter 6 Notes Manager (`examples/ch06-notes-manager`), so readers keep one project from Part 1 into Part 2. Record the answer here: ______
- [ ] [manual] D2: Which tool(s) appear in screenshots? Pick one chat assistant and one editor assistant as *examples of their kinds*, and record names and versions here: ______
- [ ] [manual] D3: Confirm the Part 2 name "Prompting and Core Development Tasks" and the folder `02-prompting-and-core-tasks`. Record the answer here: ______

## Stage 1 — Scaffolding

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/` and add a "Part 2 — Prompting and Core Development Tasks" group to the sidebar in `astro.config.mjs`. Draft pages must not break `npm run build`, the links validator or `stats.json`. Check what Starlight does with `draft: true` pages named in the sidebar; if it fails, use `autogenerate` for this folder. `stats.json` must count only published chapters. Add a short test for the count to `scripts/` if the existing tests allow.
- [ ] [moderate] Add image support: create `src/assets/` and show one real image through a throwaway test page (not committed) to confirm Astro optimizes it with `sharp`, the built path is under `/_astro/`, and the CSP in `public/_headers` needs no change. Record the result in a line under the new figures section of `CONTRIBUTING.md` (the next task adds that section; create it here if it doesn't exist yet).
- [ ] [moderate] Add `scripts/check_images.py` and call it from `scripts/check.sh`. It fails when an image in a chapter has empty alt text, has no caption line after it, is larger than 300 KB, is wider than 1,200 px, or when a file in `src/assets/` is not used by any page. Add tests for each failure.
- [ ] [simple] Add a "Figures and screenshots" section to `CONTRIBUTING.md` with the table and screenshot setup from this plan.
- [ ] [simple] Add the new glossary terms Volume 2 needs (for example few-shot prompt, structured output, system prompt, context window budget, acceptance criteria, regression test, code coverage, architecture decision record) as `{#id}` headings in `src/content/docs/glossary.md`. Only terms the chapters will use; define each in plain language.
- [ ] [simple] Extend `scripts/check_examples.py` to scan the Volume 2 folder and the new `examples/ch*/` folders. Confirm `sh scripts/check.sh` still passes.


## Chapter 7 — Prompt Engineering for Software Engineers

**Page:** `src/content/docs/02-prompting-and-core-tasks/07-prompt-engineering-for-software-engineers.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/07-prompt-engineering-for-software-engineers.md` · **Sections:**

- 7.1 What prompt engineering is, and what it is not
- 7.2 Anatomy of an effective prompt: role, context, task, constraints, output format
- 7.3 Worked example: the same task with a vague prompt and a specific one
- 7.4 Prompt patterns for code: explain, generate, review, refactor
- 7.5 Iterating: read, correct, re-ask, and when to start over

**Images planned:**

- Diagram `ch07-prompt-anatomy`: Mermaid diagram of the parts of a prompt and how each narrows the answer.
- Screenshot `src/assets/ch07/ch07-vague-prompt.png`: a chat assistant answering a vague prompt for a small coding task.
- Screenshot `src/assets/ch07/ch07-specific-prompt.png`: the same assistant answering the specific version of that prompt.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/07-prompt-engineering-for-software-engineers.md` with front matter (`title: Chapter 7 — Prompt Engineering for Software Engineers`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 7.1` to `## 7.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [simple] Write the `ch07-prompt-anatomy` Mermaid diagram in the chapter: a diagram of the parts of a prompt and how each narrows the answer. No colors or `style` lines.
- [ ] [manual] Run the worked example for §7.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch07-vague-vs-specific-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch07/` (ch07-vague-prompt.png, ch07-specific-prompt.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 7.1 to 7.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch07-vague-vs-specific-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 7 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Take one task from your own work, write a vague and a specific prompt, run both, and compare the answers against a checklist you wrote first), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 7. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 7: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 7: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 8 — Advanced Prompting Techniques

**Page:** `src/content/docs/02-prompting-and-core-tasks/08-advanced-prompting-techniques.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/08-advanced-prompting-techniques.md` · **Sections:**

- 8.1 Decomposing a large task into reviewable steps
- 8.2 Asking the AI to plan before it writes, and to state its assumptions
- 8.3 Examples in the prompt (few-shot) and when they help or hurt
- 8.4 Structured outputs: asking for JSON and validating it in code
- 8.5 Keeping a prompt library in your repository

**Images planned:**

- Diagram `ch08-decomposition`: Mermaid flowchart: one large task split into steps, each with its own check.
- Screenshot `src/assets/ch08/ch08-plan-first.png`: an assistant listing a plan and its assumptions before writing code.
- Screenshot `src/assets/ch08/ch08-structured-json.png`: a request for JSON output and the reply, with one field wrong.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/08-advanced-prompting-techniques.md` with front matter (`title: Chapter 8 — Advanced Prompting Techniques`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 8.1` to `## 8.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [moderate] Build `examples/ch08-structured-output/`: A small Python script that asks for JSON from a saved model reply, validates it against a schema with pytest tests for good and bad replies. It makes no live AI calls. Add `pyproject.toml`, tests that pass with `python3 -m pytest -v`, and a short README. Add the example to `.github/workflows/examples.yml` if it lists examples.
- [ ] [simple] Write the `ch08-decomposition` Mermaid diagram in the chapter: a flowchart: one large task split into steps, each with its own check. No colors or `style` lines.
- [ ] [manual] Run the worked example for §8.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch08-plan-and-structured-output-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch08/` (ch08-plan-first.png, ch08-structured-json.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [complex] Write sections 8.1 to 8.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch08-plan-and-structured-output-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 8 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Build a prompt-library folder with three tested prompts, and a validator that rejects a reply that does not match the schema), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 8. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 8: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 8: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 9 — Context Management for AI-Assisted Development

**Page:** `src/content/docs/02-prompting-and-core-tasks/09-context-management-for-ai-assisted-development.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/09-context-management-for-ai-assisted-development.md` · **Sections:**

- 9.1 What the AI can and cannot see in each kind of tool
- 9.2 The context window as a budget (links back to Chapter 3 §3.4)
- 9.3 What to include: files, errors, conventions, decisions
- 9.4 Project instruction files that tools read automatically
- 9.5 Trimming and refreshing context in a long session

**Images planned:**

- Diagram `ch09-context-budget`: Mermaid diagram of a context window filled by instructions, files, history and the new request.
- Screenshot `src/assets/ch09/ch09-add-files-to-context.png`: an editor assistant with files attached as context.
- Screenshot `src/assets/ch09/ch09-instruction-file.png`: the same editor showing a project instruction file the tool reads.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/09-context-management-for-ai-assisted-development.md` with front matter (`title: Chapter 9 — Context Management for AI-Assisted Development`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 9.1` to `## 9.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [moderate] Build `examples/ch09-context-budget/`: A script that counts tokens in a list of files with tiktoken and reports which files fit a stated budget, with tests. It makes no AI calls. Add `pyproject.toml`, tests that pass with `python3 -m pytest -v`, and a short README. Add the example to `.github/workflows/examples.yml` if it lists examples.
- [ ] [simple] Write the `ch09-context-budget` Mermaid diagram in the chapter: a diagram of a context window filled by instructions, files, history and the new request. No colors or `style` lines.
- [ ] [manual] Capture the screenshots listed above from the tool chosen in D2 into `src/assets/ch09/` (ch09-add-files-to-context.png, ch09-instruction-file.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 9.1 to 9.5. Short, direct sentences. Every AI reply or output block is pasted from a real run you were given or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 9 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Write a project instruction file for your own repository, then test whether the AI follows it on three tasks), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 9. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 9: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 9: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 10 — Conversational Workflows

**Page:** `src/content/docs/02-prompting-and-core-tasks/10-conversational-workflows-for-ai-assisted-development.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/10-conversational-workflows-for-ai-assisted-development.md` · **Sections:**

- 10.1 Why long conversations drift
- 10.2 One task per conversation, and when to continue one
- 10.3 Summarizing and restarting with a handoff note
- 10.4 Correcting the AI without compounding the error
- 10.5 Keeping a development journal of prompts and decisions (extends Chapter 6 §6.8)

**Images planned:**

- Diagram `ch10-conversation-loop`: Mermaid diagram of the loop: state the step, get the answer, verify, summarize, continue or restart.
- Screenshot `src/assets/ch10/ch10-drifting-conversation.png`: a long conversation where the AI has lost an early constraint.
- Screenshot `src/assets/ch10/ch10-handoff-note.png`: a short handoff note pasted into a fresh conversation.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/10-conversational-workflows-for-ai-assisted-development.md` with front matter (`title: Chapter 10 — Conversational Workflows`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 10.1` to `## 10.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [simple] Write the `ch10-conversation-loop` Mermaid diagram in the chapter: a diagram of the loop: state the step, get the answer, verify, summarize, continue or restart. No colors or `style` lines.
- [ ] [manual] Run the worked example for §10.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch10-drift-and-restart-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch10/` (ch10-drifting-conversation.png, ch10-handoff-note.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 10.1 to 10.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch10-drift-and-restart-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 10 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Run one feature across two conversations using a handoff note, and record where the AI lost or kept the context), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 10. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 10: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 10: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 11 — AI-Assisted Requirements Engineering

**Page:** `src/content/docs/02-prompting-and-core-tasks/11-ai-assisted-requirements-engineering.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/11-ai-assisted-requirements-engineering.md` · **Sections:**

- 11.1 From a vague request to a checkable requirement
- 11.2 Letting the AI ask clarifying questions
- 11.3 Writing acceptance criteria and edge cases
- 11.4 Turning acceptance criteria into tests
- 11.5 Checking AI-written requirements for invented detail

**Images planned:**

- Diagram `ch11-request-to-tests`: Mermaid diagram: vague request, questions, criteria, tests.
- Screenshot `src/assets/ch11/ch11-clarifying-questions.png`: an assistant asking clarifying questions about a feature request.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/11-ai-assisted-requirements-engineering.md` with front matter (`title: Chapter 11 — AI-Assisted Requirements Engineering`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 11.1` to `## 11.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [moderate] Build `examples/ch11-acceptance-criteria/`: Acceptance criteria for a new Notes Manager feature as pytest tests that fail before the feature exists, plus the criteria in Markdown. Follows decision D1. Add `pyproject.toml`, tests that pass with `python3 -m pytest -v`, and a short README. Add the example to `.github/workflows/examples.yml` if it lists examples.
- [ ] [simple] Write the `ch11-request-to-tests` Mermaid diagram in the chapter: a diagram: vague request, questions, criteria, tests. No colors or `style` lines.
- [ ] [manual] Run the worked example for §11.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch11-requirements-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch11/` (ch11-clarifying-questions.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 11.1 to 11.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch11-requirements-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 11 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Take a one-line feature request, produce acceptance criteria with the AI, and write the failing tests before any code), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 11. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 11: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 11: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 12 — AI-Assisted Architecture and System Design

**Page:** `src/content/docs/02-prompting-and-core-tasks/12-ai-assisted-architecture-and-system-design.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/12-ai-assisted-architecture-and-system-design.md` · **Sections:**

- 12.1 What AI is good and bad at in design work
- 12.2 Asking for options and trade-offs, not a single answer
- 12.3 Checking a design against your constraints
- 12.4 Recording the decision: a short architecture decision record
- 12.5 Drawing the design: component and sequence diagrams

**Images planned:**

- Diagram `ch12-options-compared`: Mermaid component diagram of two design options for the same feature.
- Diagram `ch12-sequence`: Mermaid sequence diagram of the chosen design.
- Screenshot `src/assets/ch12/ch12-design-options.png`: an assistant comparing two design options with trade-offs.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/12-ai-assisted-architecture-and-system-design.md` with front matter (`title: Chapter 12 — AI-Assisted Architecture and System Design`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 12.1` to `## 12.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [simple] Write the `ch12-options-compared` Mermaid diagram in the chapter: Mermaid component diagram of two design options for the same feature. No colors or `style` lines.
- [ ] [simple] Write the `ch12-sequence` Mermaid diagram in the chapter: Mermaid sequence diagram of the chosen design. No colors or `style` lines.
- [ ] [manual] Run the worked example for §12.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch12-design-options-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch12/` (ch12-design-options.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [complex] Write sections 12.1 to 12.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch12-design-options-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 12 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Ask the AI for two designs for a feature, choose one against written constraints, and write the decision record), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 12. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 12: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 12: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 13 — AI-Assisted Code Generation

**Page:** `src/content/docs/02-prompting-and-core-tasks/13-ai-assisted-code-generation.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/13-ai-assisted-code-generation.md` · **Sections:**

- 13.1 From an approved design to small, reviewable changes
- 13.2 Prompting for code that follows your conventions
- 13.3 Reviewing generated code as a diff
- 13.4 Typical defects in generated code and how to spot them
- 13.5 When to write it yourself

**Images planned:**

- Diagram `ch13-generate-review-loop`: Mermaid diagram of the generate, review diff, run tests, accept or revert loop.
- Screenshot `src/assets/ch13/ch13-diff-review.png`: an editor diff view of an AI change being reviewed.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/13-ai-assisted-code-generation.md` with front matter (`title: Chapter 13 — AI-Assisted Code Generation`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 13.1` to `## 13.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [moderate] Build `examples/ch13-notes-tags/`: The feature specified in Chapter 11 added to the Notes Manager, with the tests from Chapter 11 now passing. Follows decision D1. Add `pyproject.toml`, tests that pass with `python3 -m pytest -v`, and a short README. Add the example to `.github/workflows/examples.yml` if it lists examples.
- [ ] [simple] Write the `ch13-generate-review-loop` Mermaid diagram in the chapter: a diagram of the generate, review diff, run tests, accept or revert loop. No colors or `style` lines.
- [ ] [manual] Run the worked example for §13.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch13-code-generation-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch13/` (ch13-diff-review.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 13.1 to 13.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch13-code-generation-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 13 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Generate the feature in three small steps, reviewing each diff, and list every change you rejected and why), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 13. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 13: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 13: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 14 — AI-Assisted Debugging and Troubleshooting

**Page:** `src/content/docs/02-prompting-and-core-tasks/14-ai-assisted-debugging-and-troubleshooting.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/14-ai-assisted-debugging-and-troubleshooting.md` · **Sections:**

- 14.1 The debugging loop: reproduce, hypothesize, test, fix, guard
- 14.2 Giving the AI what it needs: the error, the code, what you tried
- 14.3 Making the AI rank hypotheses and say how to test each
- 14.4 Verifying a fix and adding a regression test
- 14.5 When the AI is confidently wrong

**Images planned:**

- Diagram `ch14-debug-loop`: Mermaid diagram of the debugging loop.
- Screenshot `src/assets/ch14/ch14-stack-trace-prompt.png`: a stack trace and the relevant code pasted into an assistant.
- Screenshot `src/assets/ch14/ch14-hypotheses.png`: the assistant ranking hypotheses with a test for each.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/14-ai-assisted-debugging-and-troubleshooting.md` with front matter (`title: Chapter 14 — AI-Assisted Debugging and Troubleshooting`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 14.1` to `## 14.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [moderate] Build `examples/ch14-debugging/`: A small program with a real, reproducible bug, a failing test that shows it, and the fixed version with the regression test. Add `pyproject.toml`, tests that pass with `python3 -m pytest -v`, and a short README. Add the example to `.github/workflows/examples.yml` if it lists examples.
- [ ] [simple] Write the `ch14-debug-loop` Mermaid diagram in the chapter: a diagram of the debugging loop. No colors or `style` lines.
- [ ] [manual] Run the worked example for §14.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch14-debugging-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch14/` (ch14-stack-trace-prompt.png, ch14-hypotheses.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 14.1 to 14.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch14-debugging-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 14 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Debug the supplied program with an AI, then write down which AI suggestion was wrong and how you found out), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 14. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 14: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 14: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Chapter 15 — AI-Assisted Testing and Quality Assurance

**Page:** `src/content/docs/02-prompting-and-core-tasks/15-ai-assisted-testing-and-quality-assurance.md` · **Old draft (idea source only):** `git show 7a7363f:chapters/02-ai-assisted-development/15-ai-assisted-testing-and-quality-assurance.md` · **Sections:**

- 15.1 What makes a test worth keeping
- 15.2 Asking the AI for tests, and reviewing them for tests that cannot fail
- 15.3 Edge cases and test data
- 15.4 Coverage: what it measures and what it does not
- 15.5 Quality gates for AI-written tests in CI (builds on Chapter 4 §4.4)

**Images planned:**

- Diagram `ch15-test-review`: Mermaid diagram of the checks a generated test must pass before it is kept.
- Screenshot `src/assets/ch15/ch15-coverage-report.png`: a coverage report produced by a real run on the example.
- Screenshot `src/assets/ch15/ch15-weak-test.png`: a generated test that passes without checking anything.

- [ ] [moderate] Create `src/content/docs/02-prompting-and-core-tasks/15-ai-assisted-testing-and-quality-assurance.md` with front matter (`title: Chapter 15 — AI-Assisted Testing and Quality Assurance`, `description`, `draft: true`), the Learning Objectives, and the section headings `## 15.1` to `## 15.5` above with a one-line note under each. Read the old draft for ideas only; its text is short and untested, so don't copy it. Add the chapter to the Part 2 sidebar. Link the previous chapter's Next Chapter section to it.
- [ ] [moderate] Build `examples/ch15-testing/`: A small module with an AI-style test file that has weak tests, the same module with strengthened tests, and a coverage run with its real output. Add `pyproject.toml`, tests that pass with `python3 -m pytest -v`, and a short README. Add the example to `.github/workflows/examples.yml` if it lists examples.
- [ ] [simple] Write the `ch15-test-review` Mermaid diagram in the chapter: a diagram of the checks a generated test must pass before it is kept. No colors or `style` lines.
- [ ] [manual] Run the worked example for §15.3 in a real AI session using the tool from D2, and save the full session as `transcripts/ch15-testing-session.md` unedited. Do not tidy the replies, even wrong ones.
- [ ] [manual] Capture the screenshots listed above from that session into `src/assets/ch15/` (ch15-coverage-report.png, ch15-weak-test.png), following the screenshot setup. Check each for visible account names, emails or keys before saving.
- [ ] [moderate] Write sections 15.1 to 15.5. Short, direct sentences. Every AI reply or output block is pasted from `transcripts/ch15-testing-session.md` or the example's real test run; where none exists, mark the block as *Illustrative:* as Chapters 3–5 do. Code blocks match `examples/`.
- [ ] [simple] Insert the Chapter 15 images with alt text and an italic caption (tool, version, month). Skip any image file that does not exist and list it in your reply.
- [ ] [moderate] Write the Engineering Insight, Common Mistakes, Hands-On Lab (Ask an AI for tests, find the ones that cannot fail, and make each fail on purpose by breaking the code), Chapter Summary, five Review Questions, and the Next Chapter section for Chapter 15. Link each glossary term on its first use.
- [ ] [simple] Write Further Reading for Chapter 15: official docs and papers only, each with a one-line note on what it is. You cannot browse the web: use URLs already in the book where they fit, and for any other source write the title and publisher with a `<!-- needs-url -->` comment. The manual review task finds and checks the URLs.
- [ ] [manual] Review Chapter 15: check every fact and external URL against current docs, check the screenshots still match the tool, read it as a new reader, then remove `draft: true`.

## Stage 11 — Release

- [ ] [moderate] Update the README (Release Plan row for Volume 2, chapter badge `0–15`, "What's in Volume 2" table with links replacing the planned list, repository structure), `src/content/docs/index.md` (Volume 2 is out), `CHANGELOG.md` (v2.0.0), and the Part 1 "End of Part 1" wording in Chapter 6.
- [ ] [simple] Run `sh scripts/check.sh` and fix anything it reports.
- [ ] [manual] Preview the branch on phone and desktop (`npm run build && npm run preview`): every new image loads, alt text reads well, diagrams render in at least one light and one dark theme.
- [ ] [manual] Merge the branch into `main`, tag `v2.0.0`, and push. CI (`site.yml`) deploys book.somaari.in.
