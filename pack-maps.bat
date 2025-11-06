@echo off
setlocal enabledelayedexpansion

set "TOOL=tools\Gdcc_x64\gdcc-ar-wad.exe"
set "SRC=mapsrc"
set "OUTROOT=src"

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

        "%TOOL%" ^
            "file:!MAP_PATH!\!MAP_NAME!" ^
            "file:!MAP_PATH!\TEXTMAP" ^
            "file:!MAP_PATH!\BEHAVIOR" ^
            "file:!MAP_PATH!\ZNODES" ^
            "file:!MAP_PATH!\SCRIPTS" ^
            "file:!MAP_PATH!\ENDMAP" ^
            -o "!OUT_WAD!"

        if errorlevel 1 (
            echo   [FAIL] Failed to pack !MAP_NAME!
        ) else (
            echo   [OK] Packed !MAP_NAME!
        )
    )

    echo.
)

echo [DONE] All projects packed successfully.
pause
exit /b 0
