# Contributing to AI-Assisted Software Development

First off, **thank you** for considering contributing! ❤️

Whether you're fixing a typo, improving an example, reporting a bug, or
adding a new lab, every contribution helps make this book better for the
community.

------------------------------------------------------------------------

# Code of Conduct

Be respectful, constructive, and welcoming.

We want this repository to be a safe place for students, professionals,
hobbyists, and open-source contributors of all experience levels.

------------------------------------------------------------------------

# Ways You Can Contribute

## 📝 Improve Documentation

-   Fix grammar or spelling
-   Improve explanations
-   Add diagrams
-   Clarify examples
-   Improve chapter flow

## 💻 Improve Code

-   Fix bugs
-   Improve readability
-   Optimize performance
-   Add comments
-   Refactor examples

## 🧪 Add Tests

-   Unit tests
-   Integration tests
-   Edge cases
-   Regression tests

## 🎓 Improve Learning Material

-   New labs
-   Exercises
-   Sample projects
-   Architecture diagrams
-   AI prompt templates

------------------------------------------------------------------------

# Development Principles

Every contribution should follow these principles:

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

Search existing issues before opening a new one.

------------------------------------------------------------------------

# Pull Request Checklist

Before submitting a Pull Request:

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

AI-generated content is welcome, but contributors are responsible for:

-   Reviewing technical accuracy
-   Verifying code compiles and runs
-   Checking security implications
-   Ensuring originality where required
-   Editing for clarity and consistency

AI should assist the contribution process---not replace thoughtful
engineering.

------------------------------------------------------------------------

# Commit Message Examples

``` text
docs(ch3): clarify context window example
fix: correct REST API validation bug
feat: add RAG sample application
test: increase unit test coverage for task manager
refactor: simplify repository abstraction
```

------------------------------------------------------------------------

# Review Process

Maintainers review contributions for:

-   Technical correctness
-   Consistency with the book
-   Readability
-   Educational value
-   Security and maintainability

Feedback is part of the collaboration process. Please don't be
discouraged if changes are requested.

------------------------------------------------------------------------

# Recognition

All meaningful contributors will be acknowledged in the project's
contributors list and Git history.

------------------------------------------------------------------------

# Thank You

Open source thrives because people share knowledge.

Thank you for helping make **AI-Assisted Software Development** a better
resource for developers around the world.

**Happy building! 🚀**
