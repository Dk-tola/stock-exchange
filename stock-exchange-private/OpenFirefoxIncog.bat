@ECHO OFF

timeout /t 3

echo VENV ACTIVATED. OPENING "FIREFOX - Incognito"

setlocal
set "PROFILE_NAME=Incognito"
set "URL=http://127.0.0.1:5000"
start "" "C:\Program Files\Mozilla Firefox\firefox.exe" -P %PROFILE_NAME% -private-window %URL%"
endlocal

exit