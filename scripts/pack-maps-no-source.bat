@echo off

rem This file will pack all maps from `mapsrc/` into `.wad` files so they can be edited or run.
rem Note unpacking said maps after editing can be done with `unpack-maps.bat`.
rem NOTE: Unlike `pack-maps.bat` this file will NOT include the ACS source of maps.

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
for %%i in ("%SCRIPT_DIR%\..") do set "ROOT=%%~fi"

set "TOOL=%ROOT%\tools\Gdcc_x64\gdcc-ar-wad.exe"
set "SRC=%ROOT%\mapsrc"
set "OUTROOT=%ROOT%\src"

if not exist "%TOOL%" (
    echo [ERROR] gdcc-ar-wad.exe not found at "%TOOL%"
    exit /b 1
)

if not exist "%SRC%" (
    echo [ERROR] Source directory "%SRC%" does not exist.
    exit /b 1
)

echo Packing projects from "%SRC%"...

for /d %%P in ("%SRC%\*") do (
    set "PROJECT_NAME=%%~nP"
    set "PROJECT_PATH=%%~fP"
    set "OUTDIR=%OUTROOT%\!PROJECT_NAME!\maps"

    if not exist "!OUTDIR!" mkdir "!OUTDIR!"

    echo [PROJECT] !PROJECT_NAME!

    for /d %%M in ("!PROJECT_PATH!\*") do (
        set "MAP_NAME=%%~nM"
        set "MAP_PATH=%%~fM"
        set "OUT_WAD=!OUTDIR!\!MAP_NAME!.wad"

        echo   Packing !MAP_NAME! -> "!OUT_WAD!"...

        rem Create temporary empty ENDMAP and MAP_NAME lumps if they do not exist
        set "TMP_ENDMAP_CREATED=0"
        set "TMP_LEVEL_CREATED=0"

        if not exist "!MAP_PATH!\ENDMAP" (
            rem Create empty ENDMAP lump
            type nul > "!MAP_PATH!\ENDMAP"
            set "TMP_ENDMAP_CREATED=1"
        )

        if not exist "!MAP_PATH!\!MAP_NAME!" (
            type nul > "!MAP_PATH!\!MAP_NAME!"
            set "TMP_LEVEL_CREATED=1"
        )

        "%TOOL%" ^
            "file:!MAP_PATH!\!MAP_NAME!" ^
            "file:!MAP_PATH!\TEXTMAP" ^
            "file:!MAP_PATH!\BEHAVIOR" ^
            "file:!MAP_PATH!\ZNODES" ^
            "file:!MAP_PATH!\ENDMAP" ^
            -o "!OUT_WAD!"

        if errorlevel 1 (
            echo   [FAIL] Failed to pack !MAP_NAME!
        ) else (
            echo   [OK] Packed !MAP_NAME!
        )

        rem Clean up the temporary lumps we created.
        if "!TMP_ENDMAP_CREATED!"=="1" (
            del /f /q "!MAP_PATH!\ENDMAP" >nul 2>&1
        )
        if "!TMP_LEVEL_CREATED!"=="1" (
            del /f /q "!MAP_PATH!\!MAP_NAME!" >nul 2>&1
        )
    )

    echo.
)

echo [DONE] All projects packed successfully.
