@echo off
set "PYTHON=%~dp0.\venv\Scripts\python.exe"

set cmd=%1

IF /I "%cmd%" EQU "m" set cmd=migrate
IF /I "%cmd%" EQU "mm" set cmd=makemigrations
if /I "%cmd%" EQU "show" set cmd=showmigrations
if /I "%cmd%" EQU "t" set cmd=test


%PYTHON% %~dp0manage.py %cmd% %2 %3 %4 %5 %6 %7 %8 %9
