@echo off
setlocal enabledelayedexpansion
cd /d "C:\Users\Nsini\Code\relaunch\relaunch-website"

echo.
echo  Relaunch -- Deploying to GitHub...
echo  --------------------------------------------------
echo.

REM Show what's about to be committed
echo  Files staged for commit:
echo.
git status --short
echo.

REM Check if there's anything to commit
git diff --cached --quiet
set CACHED_EMPTY=%ERRORLEVEL%
git diff --quiet
set DIRTY=%ERRORLEVEL%

if %CACHED_EMPTY% EQU 0 if %DIRTY% EQU 0 (
  echo  Nothing to commit. Working tree clean.
  echo.
  pause
  exit /b 0
)

REM Force a real commit message
:askmsg
set "msg="
set /p "msg=  Commit message (required): "
if "!msg!"=="" (
  echo  Commit message cannot be empty. Aborting deploy is also fine -- Ctrl+C to bail.
  goto askmsg
)

echo.
echo  Committing and pushing...
echo.

git add .
git commit -m "!msg!"
if errorlevel 1 (
  echo.
  echo  Commit failed. Nothing pushed.
  pause
  exit /b 1
)

git push origin main
if errorlevel 1 (
  echo.
  echo  Push failed. Commit was made locally but not pushed.
  echo  Try again, or check your network/auth.
  pause
  exit /b 1
)

echo.
echo  Done! Netlify will auto-deploy in ~30 seconds.
echo  Site: https://tryrelaunch.com
echo.
pause
