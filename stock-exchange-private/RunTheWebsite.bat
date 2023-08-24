@ECHO OFF
TITLE Stock Exchange Website

echo BEGIN RUNNING THE WEBSITE?

pause

call venv\Scripts\activate

start "OPEN FIREFOX" cmd /c OpenFirefoxIncog.bat

echo RUNNING "py wsgi.py"
py wsgi.py