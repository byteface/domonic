# Changelog

All notable changes to domonic are documented here.

## [1.0.1] - 2026-08-22

### Added

- Added modern HTML, DOM, SVG, CSS, XML, parser, server, and Web API coverage across the release sweep.
- Added release metadata to improve PyPI and GitHub discoverability.

### Changed

- Applied Black formatting across the codebase for a cleaner release diff.
- Expanded package keywords, project URLs, classifiers, and README feature coverage.
- Improved tests around DOM, HTML rendering, URL handling, CLI querying, JavaScript helpers, and common edge cases.

### Security

- Resolved Bandit findings by replacing silent exception handling, adding request timeouts, tightening subprocess usage markers, and documenting intentional compatibility surfaces.
- Updated vulnerable development dependencies including `ujson` and `setuptools`.

