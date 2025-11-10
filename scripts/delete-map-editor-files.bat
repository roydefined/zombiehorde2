@echo off

rem This file removes Ultimate Doombuilder map files from the map source folders.
rem It deletes:
rem - *.dbs
rem - *.backup1
rem - *.backup2
rem - *.backup3

rem NOTE: Removal of backups can have destructive effect and possibly loss of data.
rem Remember this when running this script.

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%\..") do set "ROOT=%%~fi"

set "SRC=%ROOT%\src"

if not exist "%SRC%" (
    echo [ERROR] Source directory "%SRC%" does not exist.
    exit /b 1
)

echo Cleaning map editor files in "%SRC%"...

for /d %%P in ("%SRC%\*") do (
    set "PROJECT_NAME=%%~nP"
    set "PROJECT_PATH=%%~fP"
    set "MAPDIR=!PROJECT_PATH!\maps"

    if exist "!MAPDIR!" (
        echo [PROJECT] !PROJECT_NAME!

        rem Remove *.dbs
        for %%F in ("!MAPDIR!\*.dbs") do (
            if exist "%%~fF" (
                echo   Deleting "%%~nxF"...
                del /f /q "%%~fF" >nul 2>&1
            )
        )

        rem Remove *.backup1, *.backup2, *.backup3
        for %%F in ("!MAPDIR!\*.backup1" "!MAPDIR!\*.backup2" "!MAPDIR!\*.backup3") do (
            if exist "%%~fF" (
                echo   Deleting "%%~nxF"...
                del /f /q "%%~fF" >nul 2>&1
            )
        )

        echo.
    ) else (
        echo [INFO] Skipping "!PROJECT_NAME!". No 'maps/' directory found.
        echo.
    )
)

echo [DONE] All map editor files cleaned.
pause
exit /b 0
