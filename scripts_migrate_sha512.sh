#!/usr/bin/env bash
grep -rl "sha256" . | grep -v ".git" || true
echo "Review occurrences before automatic replacement."
