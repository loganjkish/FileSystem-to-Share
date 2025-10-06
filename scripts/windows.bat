@echo off
powershell -NoProfile -Command "Start-Process powershell -ArgumentList '-NoProfile -Command \"Start-Service WebClient -ErrorAction SilentlyContinue; Set-Service WebClient -StartupType Automatic\"' -Verb RunAs"

set /p USERNAME=Enter username:
set /p PASSWORD=Enter password:

net use %DRIVE%: >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Drive letter is taken. Please choose another letter.
    pause
    exit /b
)

net use <DriveLetter>: '<WebDAV-Server-URL>' /user:%USERNAME% %PASSWORD% /persistent:yes
