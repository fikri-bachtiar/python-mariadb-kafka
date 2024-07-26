#!/bin/bash
./scripts/lint_mypy.sh && ./scripts/lint_flake8.sh && ./scripts/lint_black.sh && ./scripts/lint_isort.sh