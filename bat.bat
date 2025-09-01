@echo off
title CrossPilot / hijacker cleanup for Chrome & Edge
echo This will CLOSE Chrome/Edge, remove forced-install policies, and reset startup pages.
echo Run as Administrator. Press Ctrl+C to abort. Otherwise continuing in 5 seconds...
timeout /t 5 >nul

REM 1) Kill browsers
taskkill /F /IM chrome.exe /T >nul 2>&1
taskkill /F /IM msedge.exe /T >nul 2>&1

REM 2) Paths
set "CHR=%LocalAppData%\Google\Chrome\User Data"
set "EDG=%LocalAppData%\Microsoft\Edge\User Data"
set "BK=%USERPROFILE%\Desktop\Browser_Cleanup_Backup"
mkdir "%BK%" >nul 2>&1

REM 3) Back up critical files (in case you want to restore)
for %%P in ("%CHR%\Default\Preferences" "%CHR%\Default\Secure Preferences" "%CHR%\Default\Last Session" "%CHR%\Default\Last Tabs") do (
  if exist "%%~fP" copy /y "%%~fP" "%BK%" >nul 2>&1
)
for %%P in ("%EDG%\Default\Preferences" "%EDG%\Default\Secure Preferences" "%EDG%\Default\Last Session" "%EDG%\Default\Last Tabs") do (
  if exist "%%~fP" copy /y "%%~fP" "%BK%" >nul 2>&1
)

REM 4) Nuke Chrome/Edge forced-install policies (common hijack vector)
reg delete "HKCU\Software\Policies\Google\Chrome\ExtensionInstallForcelist" /f >nul 2>&1
reg delete "HKLM\Software\Policies\Google\Chrome\ExtensionInstallForcelist" /f >nul 2>&1
reg delete "HKCU\Software\Policies\Google\Chrome\ExtensionInstallSources" /f >nul 2>&1
reg delete "HKLM\Software\Policies\Google\Chrome\ExtensionInstallSources" /f >nul 2>&1
reg delete "HKCU\Software\Policies\Google\Chrome\ExtensionInstallAllowlist" /f >nul 2>&1
reg delete "HKLM\Software\Policies\Google\Chrome\ExtensionInstallAllowlist" /f >nul 2>&1

reg delete "HKCU\Software\Policies\Microsoft\Edge\ExtensionInstallForcelist" /f >nul 2>&1
reg delete "HKLM\Software\Policies\Microsoft\Edge\ExtensionInstallForcelist" /f >nul 2>&1
reg delete "HKCU\Software\Policies\Microsoft\Edge\ExtensionInstallSources" /f >nul 2>&1
reg delete "HKLM\Software\Policies\Microsoft\Edge\ExtensionInstallSources" /f >nul 2>&1
reg delete "HKCU\Software\Policies\Microsoft\Edge\ExtensionInstallAllowlist" /f >nul 2>&1
reg delete "HKLM\Software\Policies\Microsoft\Edge\ExtensionInstallAllowlist" /f >nul 2>&1

REM 5) Remove startup links that open CrossPilot
powershell -NoP -NonI -Command ^
  "$paths=@($env:APPDATA+'\Microsoft\Windows\Start Menu\Programs\Startup', $env:ProgramData+'\Microsoft\Windows\Start Menu\Programs\StartUp');" ^
  "foreach($p in $paths){ if(Test-Path $p){ Get-ChildItem -Path $p -Recurse -Include *.lnk,*.url -ErrorAction SilentlyContinue |" ^
  "  Select-String -SimpleMatch 'crosspilot' | ForEach-Object{ Remove-Item -LiteralPath $_.Path -Force -ErrorAction SilentlyContinue } } }"

REM 6) Reset Chrome/Edge last-session restore (prevents the tab from coming back)
for %%P in ("%CHR%\Default\Last Session" "%CHR%\Default\Last Tabs" "%CHR%\Default\Sessions") do (
  if exist "%%~fP" del /f /q "%%~fP" >nul 2>&1
)
for %%P in ("%EDG%\Default\Last Session" "%EDG%\Default\Last Tabs" "%EDG%\Default\Sessions") do (
  if exist "%%~fP" del /f /q "%%~fP" >nul 2>&1
)

REM 7) Remove any leftover extension folders that reference CrossPilot/CRXLauncher/XFinder
powershell -NoP -NonI -Command ^
  "$targets=@('%LocalAppData%\Google\Chrome\User Data\Default\Extensions','%LocalAppData%\Microsoft\Edge\User Data\Default\Extensions');" ^
  "foreach($t in $targets){ if(Test-Path $t){ Get-ChildItem -Path $t -Directory -Recurse -ErrorAction SilentlyContinue |" ^
  "  ForEach-Object{ $hit=$false; Get-ChildItem -Path $_.FullName -Recurse -File -ErrorAction SilentlyContinue |" ^
  "    Select-String -Pattern 'crosspilot','crxlauncher','xfinder' -SimpleMatch -Quiet -ErrorAction SilentlyContinue |" ^
  "    ForEach-Object{ $hit=$true }; if($hit){ Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue } } } }"

REM 8) Hard reset Chrome/Edge startup pages by recreating Preferences if they contain crosspilot
powershell -NoP -NonI -Command ^
  "function FixPrefs($prefPath){ if(Test-Path $prefPath){ $txt= Get-Content -LiteralPath $prefPath -Raw; " ^
  " if($txt -match 'crosspilot'){ Move-Item -LiteralPath $prefPath ($prefPath+'.bak') -Force; } } };" ^
  "FixPrefs('%LocalAppData%\Google\Chrome\User Data\Default\Preferences');" ^
  "FixPrefs('%LocalAppData%\Microsoft\Edge\User Data\Default\Preferences');"

echo.
echo DONE. A backup (if any) is in: %BK%
echo Reboot Windows, then open Chrome and set On startup = "Open the New Tab page".
echo Consider reinstalling only trusted extensions from the Chrome Web Store.
pause
