@echo off

:: === ACSUtils packing script ===
:: This version copies files and runs preprocessing steps, but SKIPS the compiler calls.
:: Compilation is handled by PubDoomer, which prepares the files and then compiles them.
:: Alternatively you may use `build-project.bat` after calling this file to build the project itself.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%modules\acsutils"

rmdir dist /S /Q
mkdir dist

copy misc\cvarinfo.acsutils dist\
copy misc\decorate.acsutils dist\

py tools\preprocess.py
@if ERRORLEVEL 1 (
    echo PREPROCESS.PY FAILED
    PAUSE
    EXIT
)

py tools\changeflaggen.py
@if ERRORLEVEL 1 (
    echo CHANGEFLAGGEN FAILED
    PAUSE
    EXIT
)

@PAUSE
