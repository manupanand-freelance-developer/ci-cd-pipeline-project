#!/bin/sh

git add .
echo commit comment?
read comment
git commit -m "${comment}"
git push origin main
git status