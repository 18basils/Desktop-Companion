@echo off
setlocal
cd /d "%~dp0"

:: Prefer base Python pythonw.exe (pure GUI binary - 0 console window)
set "PYW=%LOCALAPPDATA%\Programs\Python\Python313\pythonw.exe"
if not exist "%PYW%" set "PYW=%~dp0.venv\Scripts\pythonw.exe"
if not exist "%PYW%" set "PYW=pythonw.exe"

start "" "%PYW%" "%~dp0companion.py"
exit
