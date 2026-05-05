@echo off
cd /d "C:\Users\Nsini\Downloads\relaunch-website"

echo.
echo  ONE-TIME CLEANUP -- removing node_modules from git tracking
echo  --------------------------------------------------
echo.
echo  This removes node_modules/ from the repo without deleting
echo  the local files. After this, run deploy.bat to push the
echo  cleanup to GitHub.
echo.
echo  This only needs to run ONCE. Don't run it again.
echo.
set /p "confirm=  Type YES to continue: "
if /I not "%confirm%"=="YES" (
  echo  Aborted.
  pause
  exit /b 0
)

echo.
echo  Removing node_modules from git tracking...
git rm -r --cached node_modules
if errorlevel 1 (
  echo  Cleanup failed. Maybe node_modules wasn't tracked.
  pause
  exit /b 1
)

echo.
echo  Done. Now run deploy.bat to push the cleanup.
echo  After that, future deploys will ignore node_modules entirely.
echo.
pause
