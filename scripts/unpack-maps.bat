@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%\..") do set "ROOT=%%~fi"

set "TOOL=%ROOT%\tools\Gdcc_x64\gdcc-ar-wad.exe"
set "SRC=%ROOT%\src"
set "OUTROOT=%ROOT%\mapsrc"

if not exist "%TOOL%" (
    echo [ERROR] gdcc-ar-wad.exe not found at "%TOOL%"
    exit /b 1
)

if not exist "%SRC%" (
    echo [ERROR] Source directory "%SRC%" does not exist.
    exit /b 1
)

echo Searching for projects in "%SRC%"...

for /d %%P in ("%SRC%\*") do (
    set "PROJECT_NAME=%%~nP"
    set "MAPDIR=%%~fP\maps"

    if exist "!MAPDIR!" (
        echo [PROJECT] !PROJECT_NAME!
        set "OUTDIR=%OUTROOT%\!PROJECT_NAME!"
        if not exist "!OUTDIR!" mkdir "!OUTDIR!"

        set "HADWADS=0"
        for %%W in ("!MAPDIR!\*.wad") do (
            if exist "%%~fW" (
                set "HADWADS=1"
                echo   Extracting %%~nxW to "!OUTDIR!"...
                "%TOOL%" wad:"%%~fW" --extract -o "!OUTDIR!"
                if errorlevel 1 (
                    echo   [FAIL] Failed to extract %%~nxW
                ) else (
                    echo   [OK] Extracted %%~nxW

                    set "MAPFOLDER=!OUTDIR!\%%~nW"

                    if exist "!MAPFOLDER!\ENDMAP" (
                        echo     Removing ENDMAP from "!MAPFOLDER!"...
                        del /f /q "!MAPFOLDER!\ENDMAP"
                    )

                    set "LEVELFILE=!MAPFOLDER!\%%~nW"
                    if exist "!LEVELFILE!" (
                        echo     Removing level file "%%~nW" from "!MAPFOLDER!"...
                        del /f /q "!LEVELFILE!"
                    )
                )
            )
        )

        if "!HADWADS!"=="0" (
            echo   [WARN] No .wad files found in "!MAPDIR!"
        )
        echo.
    ) else (
        echo [INFO] Skipping "!PROJECT_NAME!". No 'maps/' directory found.
        echo.
    )
)

echo [DONE] All projects processed.
