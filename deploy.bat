@echo off
setlocal enabledelayedexpansion
cd /d "C:\Users\Nsini\Code\relaunch\relaunch-website"

echo.
echo  Relaunch -- Deploying to GitHub...
echo  --------------------------------------------------
echo.

REM Sync shared partials (nav + footer) into every page before commit.
REM Single source of truth lives in clients/^<slug^>/_partials/. Run before staging.
REM Pass /skip-sync as the first arg to bypass (e.g. when Python isn't installed yet).
if /I "%~1"=="/skip-sync" (
  echo  Skipping partial sync ^(--skip-sync flag passed^).
  echo.
  goto :after_sync
)
echo  Syncing partials...
if exist "clients\malarky\sync-partials.py" (
  REM Only trust the py launcher. On Windows, "python" on PATH is often a Microsoft Store
  REM ad shim that fails when invoked, so checking "where python" is unreliable.
  REM The py launcher ships with the real python.org installer and never triggers the shim.
  py -3 --version >nul 2>&1
  if errorlevel 1 (
    echo.
    echo  Python not installed ^(or only the Microsoft Store shim is present^).
    echo  Install with:  winget install Python.Python.3.12
    echo  Then reopen PowerShell and re-run deploy.bat.
    echo.
    echo  Skipping sync for this deploy ^(safe — sync is idempotent and pages
    echo  on disk are already current^). Install Python before the next push.
    echo.
  ) else (
    py -3 "clients\malarky\sync-partials.py"
    if errorlevel 1 (
      echo  Partial sync failed. Aborting.
      pause
      exit /b 1
    )
    echo.
  )
)
:after_sync

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
