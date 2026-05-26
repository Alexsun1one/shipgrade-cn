#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

bash scripts/verify.sh
mkdir -p .release
COPYFILE_DISABLE=1 tar \
  --exclude='.git' \
  --exclude='.release' \
  --exclude='*/__pycache__' \
  --exclude='*.pyc' \
  --exclude='.DS_Store' \
  --exclude='._*' \
  -czf .release/shipgrade-cn-v0.1.tar.gz \
  .
shasum -a 256 .release/shipgrade-cn-v0.1.tar.gz > .release/shipgrade-cn-v0.1.tar.gz.sha256
cat .release/shipgrade-cn-v0.1.tar.gz.sha256
