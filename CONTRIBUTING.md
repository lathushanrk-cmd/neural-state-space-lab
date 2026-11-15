# Contributing

1. Open an issue describing the scientific or software problem before substantial changes.
2. Fork the repository, create a branch and add unit tests with known-answer examples.
3. Run `python -m pytest`, `nssl-demo --output outputs/synthetic` and `ruff check src/ --select E4,E7,E9,F`.
4. Explain scientific changes, assumptions and effects on interpretation.
5. Submit a pull request. Do not include restricted participant data, credentials or licensed raw data.
6. Do not interpret observed recovery as proof of biological stability or causality.

For sensitive security issues, use a private maintainer contact rather than publishing exploit details.
