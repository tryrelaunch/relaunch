@echo off
echo.
echo  Relaunch — Deploying to GitHub...
echo  ─────────────────────────────────
echo.

cd /d %~dp0

git add .

set /p msg="Commit message (or press Enter for 'Update site'): "
if "%msg%"=="" set msg=Update site

git commit -m "%msg%"

git push

echo.
echo  Done! Netlify will auto-deploy in ~30 seconds.
echo  Site: https://tryrelaunch.com
echo.
pause
