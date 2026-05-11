@echo off
setlocal enabledelayedexpansion
cd /d "C:\Users\Nsini\Code\relaunch\relaunch-website"

REM ────────────────────────────────────────────────────────────────────────
REM Usage:
REM   deploy.bat                       — prompts for commit message
REM   deploy.bat "your message"        — uses that message, no prompt, no pause
REM   deploy.bat /skip-sync            — skips partial sync, prompts for message
REM   deploy.bat /skip-sync "msg"      — both
REM ────────────────────────────────────────────────────────────────────────

set "SKIPSYNC="
set "INLINEMSG="
if /I "%~1"=="/skip-sync" (
  set "SKIPSYNC=1"
  set "INLINEMSG=%~2"
) else (
  set "INLINEMSG=%~1"
)

echo.
echo  Relaunch -- Deploying to GitHub...
echo  --------------------------------------------------
echo.

REM Sync shared partials (nav + footer) into every page before commit.
REM Single source of truth lives in clients/^<slug^>/_partials/. Run before staging.
if defined SKIPSYNC (
  echo  Skipping partial sync ^(/skip-sync flag passed^).
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

REM Use inline message if provided, otherwise prompt.
set "msg=%INLINEMSG%"
if "!msg!"=="" (
  :askmsg
  set "msg="
  set /p "msg=  Commit message (required): "
  if "!msg!"=="" (
    echo  Commit message cannot be empty. Aborting deploy is also fine -- Ctrl+C to bail.
    goto askmsg
  )
)

echo.
echo  Committing and pushing: !msg!
echo.

git add .
git commit -m "!msg!"
if errorlevel 1 (
  echo.
  echo  Commit failed. Nothing pushed.
  if "%INLINEMSG%"=="" pause
  exit /b 1
)

git push origin main
if errorlevel 1 (
  echo.
  echo  Push failed. Commit was made locally but not pushed.
  echo  Try again, or check your network/auth.
  if "%INLINEMSG%"=="" pause
  exit /b 1
)

echo.
echo  Done! Netlify will auto-deploy in ~30 seconds.
echo  Site: https://tryrelaunch.com
echo.
REM Only pause when run interactively (no inline message).
if "%INLINEMSG%"=="" pause
