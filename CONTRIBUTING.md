# Contributing to AI-Assisted Software Development

First off, **thank you** for considering contributing! ❤️

Whether you're spotting a typo, suggesting a better example, reporting a
bug, or proposing a new lab, every contribution helps make this book better
for the community.

------------------------------------------------------------------------

# How Contributions Work

Pull requests on this repository are limited to collaborators, so outside
pull requests can't be opened. Please contribute through
[Issues](https://github.com/ashwinkrpi/ai-assisted-development-book/issues)
instead: describe the problem or suggestion, and the change will be made
in the book.

You're also welcome to fork the repository and adapt the examples for
your own use.

------------------------------------------------------------------------

# Code of Conduct

Be respectful, constructive, and welcoming.

We want this repository to be a safe place for students, professionals,
hobbyists, and open-source contributors of all experience levels.

------------------------------------------------------------------------

# Ways You Can Contribute

Open an issue for any of the following.

## 📝 Improve Documentation

-   Report grammar or spelling mistakes
-   Improve explanations
-   Add diagrams
-   Clarify examples
-   Improve chapter flow

## 💻 Improve Code

-   Report bugs in the examples
-   Suggest readability improvements
-   Point out performance problems
-   Flag code that needs comments
-   Propose refactorings

## 🧪 Suggest Tests

-   Unit tests
-   Integration tests
-   Edge cases
-   Regression tests

## 🎓 Suggest Learning Material

-   New labs
-   Exercises
-   Sample projects
-   Architecture diagrams
-   AI prompt templates

------------------------------------------------------------------------

# Development Principles

Every change to the book follows these principles:

-   Requirements before implementation
-   Small, focused pull requests
-   Readable code over clever code
-   Test before submitting
-   Keep documentation up to date
-   Never commit secrets or credentials

------------------------------------------------------------------------

# Repository Structure

``` text
chapters/                 # book source, published by MkDocs
├── index.md              # site landing page
└── 01-foundations/       # Part 1 (Volume 1): chapters 1–6
examples/                 # runnable companion code, one folder per example
transcripts/              # verbatim AI session transcripts behind worked examples
scripts/check_examples.py # checks chapter code blocks match examples/
images/                   # README banner images
.github/workflows/        # site deployment and example tests
mkdocs.yml                # site configuration and navigation
```

This layout helps you point to the right file in an issue, or find your
way around a fork.

Chapter text goes in `chapters/`. If you add a page, also add it to the
`nav` section of `mkdocs.yml`, and check that `mkdocs build --strict`
passes. Don't commit `site/`, because CI builds it.

Code in a chapter that readers are meant to run lives in `examples/`.
Start the chapter's code block with a comment naming the file, such as
`# tests/test_cli.py`, and keep it identical to that file.
`python3 scripts/check_examples.py` reports any difference, and CI runs
it with each example's tests. Output shown in a chapter must be pasted
from a real run.

------------------------------------------------------------------------

# Reporting Issues

Please include:

-   Clear description
-   Expected behavior
-   Actual behavior
-   Steps to reproduce
-   Screenshots (if applicable)
-   Environment details
-   The chapter and section, for problems in the book text

Search existing issues before opening a new one.

------------------------------------------------------------------------

# Pull Request Checklist (Collaborators)

Before a collaborator submits a Pull Request:

-   [ ] The change solves a specific problem.
-   [ ] Documentation has been updated.
-   [ ] Tests pass.
-   [ ] No secrets or credentials are included.
-   [ ] Markdown renders correctly.
-   [ ] Commit messages are clear.

------------------------------------------------------------------------

# Writing Guidelines

For documentation:

-   Use clear, concise language.
-   Prefer active voice.
-   Include practical examples.
-   Keep formatting consistent.
-   Explain *why*, not just *how*.

------------------------------------------------------------------------

# AI-Assisted Contributions

Using AI to help write an issue or a suggested fix is welcome, but you're
responsible for:

-   Reviewing technical accuracy
-   Verifying any suggested code compiles and runs
-   Checking security implications
-   Ensuring originality where required
-   Editing for clarity and consistency

AI should assist the contribution process---not replace thoughtful
engineering.

------------------------------------------------------------------------

# Commit Message Examples (Collaborators)

``` text
docs(ch3): clarify context window example
fix: correct REST API validation bug
feat: add RAG sample application
test: increase unit test coverage for task manager
refactor: simplify repository abstraction
```

------------------------------------------------------------------------

# Review Process

Maintainers review issues and suggested changes for:

-   Technical correctness
-   Consistency with the book
-   Readability
-   Educational value
-   Security and maintainability

Feedback is part of the collaboration process. Please don't be
discouraged if a suggestion is changed, combined with others, or not
taken up.

------------------------------------------------------------------------

# Licensing of Contributions

By submitting a contribution, you agree that it is licensed under the
same terms as the part of the repository it changes: CC BY-NC-SA 4.0
for book content and MIT for code (see [LICENSE](LICENSE)). You also
grant the author, Ashwin Koppam Raghavendra, permission to include your
contribution in commercial editions of the book, such as print or ebook
editions. Only submit work you have the right to license this way.

------------------------------------------------------------------------

# Recognition

Everyone whose issue leads to a meaningful change will be acknowledged
in the commit that makes it.

------------------------------------------------------------------------

# Thank You

Open source thrives because people share knowledge.

Thank you for helping make **AI-Assisted Software Development** a better
resource for developers around the world.

**Happy building! 🚀**
