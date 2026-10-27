# Contributing

Thanks for your interest in this portfolio.

This is primarily a **curated learning and engineering portfolio**, rather than a general-purpose open-source framework. Suggestions that improve accuracy, reproducibility, accessibility, documentation, or existing code are welcome.

## Before opening a change

1. Search existing issues and pull requests to avoid duplication.
2. Open an issue for larger changes to discuss scope before writing code.
3. Keep changes focused on one project or one clear problem.
4. Do not upload real customer records, private course material, credentials, API keys, or third-party proprietary data.

## Working on a project

- Follow the instructions in the project's own README.
- Prefer deterministic or clearly attributed public/synthetic data.
- Preserve train/test splits, time-aware validation, and other modeling assumptions when updating experiments.
- Document datasets, dependencies, expected output, limitations, and any new runtime requirements.
- Include tests for behavior changes and verify existing tests still pass.

For the portfolio-level Python checks:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

The HTML demos are educational prototypes; do not present them as authorized production services.

## Pull requests

Explain **what changed, why it matters, how you tested it, and any remaining limitations**. Reference the issue when applicable. Small fixes, broken-link reports and documentation clarifications are especially helpful.

### Attribution and rights

Some work originated in academic teams, courses and publicly available datasets. Preserve acknowledgments and original source links. Do not submit content you lack permission to distribute.

**Licensing note:** This repository does not currently declare a general reuse license. Public visibility alone does not grant permission to reuse copyrighted code or documentation. A license may be considered after reviewing third-party and academic contributions.
