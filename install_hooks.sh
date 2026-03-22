#!/bin/bash
# --- INSTALL pre-commit ---
echo '1. Installing pre-commit`s from pip3'
python -m pip install pre-commit
echo '✅ pre-commit installed'

echo ''
echo '2. Install pre-commit hooks'
pre-commit install
