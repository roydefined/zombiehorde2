@echo off

rem This file will compile every single map file available in `mapsrc/` and store them in a `BEHAVIOR` lump.

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%\..") do set "ROOT=%%~fi"

set "BCC=%ROOT%\tools\Zt-bcc_x86\zt-bcc.exe"

set "SRC=%ROOT%\mapsrc"

if not exist "%BCC%" (
    echo [ERROR] BCC compiler not found at "%BCC%"
    exit /b 1
)

if not exist "%SRC%" (
    echo [ERROR] Source directory "%SRC%" does not exist.
    exit /b 1
)

echo Compiling ACS scripts from "%SRC%"...
echo.

for /d %%P in ("%SRC%\*") do (
    set "PROJECT_NAME=%%~nP"
    set "PROJECT_PATH=%%~fP"

    echo [PROJECT] !PROJECT_NAME!

    for /d %%M in ("!PROJECT_PATH!\*") do (
        set "MAP_NAME=%%~nM"
        set "MAP_PATH=%%~fM"

        set "SRC_ACS=!MAP_PATH!\SCRIPTS"
        set "DST_BEHAVIOR=!MAP_PATH!\BEHAVIOR"

        rem Skip if script doesn't exist
        if not exist "!SRC_ACS!" (
            echo   [SKIP] !MAP_NAME! contains no script
        )

        rem Compile if script exists
        if exist "!SRC_ACS!" (
            echo   Compiling !MAP_NAME!...

            "%BCC%" ^
                -i "%ROOT%\libsrc" ^
                -i "%ROOT%\src\ZombieHorde2" ^
                "!SRC_ACS!" "!DST_BEHAVIOR!"

            if errorlevel 1 (
                echo   [FAIL] Failed to compile !MAP_NAME!
            )

            if not errorlevel 1 (
                echo   [OK] Compiled !MAP_NAME!
            )
        )
    )

    echo.
)

echo [DONE] All map scripts compiled.
