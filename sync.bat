@echo off

git pull
git diff --no-prefix -U200
git add .
git commit -m "sync"
git push
pause