#!/bin/bash
echo "Comment: $n"
git add -A && git commit "$n"
git push
