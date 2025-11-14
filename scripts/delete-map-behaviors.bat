@echo off

rem This file removes all compiled BEHAVIOR lumps from every map under `mapsrc/`.
rem Called after pack-maps.bat finished packaging maps.

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%\..") do set "ROOT=%%~fi"

set "SRC=%ROOT%\mapsrc"

if not exist "%SRC%" (
    echo [ERROR] Source directory "%SRC%" does not exist.
    exit /b 1
)

echo Cleaning BEHAVIOR lumps from "%SRC%"...
echo.

for /d %%P in ("%SRC%\*") do (
    set "PROJECT_NAME=%%~nP"
    set "PROJECT_PATH=%%~fP"

    echo [PROJECT] !PROJECT_NAME!

    for /d %%M in ("!PROJECT_PATH!\*") do (
        set "MAP_NAME=%%~nM"
        set "MAP_PATH=%%~fM"

        set "FILE_BEHAVIOR=!MAP_PATH!\BEHAVIOR"

        if exist "!FILE_BEHAVIOR!" (
            echo   Deleting BEHAVIOR lump for !MAP_NAME!...
            del /f /q "!FILE_BEHAVIOR!" >nul 2>&1

            if exist "!FILE_BEHAVIOR!" (
                echo   [FAIL] Failed to delete BEHAVIOR for !MAP_NAME!
            ) else (
                echo   [OK] Deleted BEHAVIOR for !MAP_NAME!
            )
        ) else (
            echo   [SKIP] !MAP_NAME! has no BEHAVIOR lump
        )
    )

    echo.
)

echo [DONE] All BEHAVIOR lumps removed.
exit /b 0
