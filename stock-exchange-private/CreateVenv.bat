@echo off

REM Set the name of the virtual environment
set "VENV_NAME=myvenv"

REM Create the virtual environment
py -3.6 -m venv %VENV_NAME%

echo Virtual environment %VENV_NAME% created.

REM Activate the virtual environment (optional)
call %VENV_NAME%\Scripts\activate

REM Install packages (example)
pip install -r requirements2.txt

echo Virtual environment %VENV_NAME% is now active.
