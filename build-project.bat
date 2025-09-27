@echo off

:: === Zombie Horde 2 project build script ===
:: This script copies over the previously packed ACSUtils files and puts them inside the library project.
:: Secondly this script ensures all files are compiled.

:: Note: You must call `pack-acsutils.bat` before calling this file to ensure all files exist.
:: Alternatively make sure that they do another way.

set "SCRIPT_DIR=%~dp0"
set "ROOT=C:\Projects\zombiehorde2"
set "BCC=%SCRIPT_DIR%tools\Zt-bcc_x86\zt-bcc.exe"

:: ACSUtils
set "ACSUTILS_DIST=%SCRIPT_DIR%modules\acsutils\dist"
set "BCSUTILS_TARGET_DIR=%ROOT%\libsrc\acs_source\bcsutils"

:: Library
set "LIBSRC_DIR=%ROOT%\libsrc"
set "LIBSRC_ACS_SOURCE=%ROOT%\libsrc\acs_source"
set "LIBSRC_ACS=%ROOT%\libsrc\acs"

:: ZH2 core
set "CORE_SRC_DIR=%ROOT%\src\ZombieHorde2\acs_source"
set "CORE_OUT_DIR=%ROOT%\src\ZombieHorde2\acs"

echo Copy ACSUtils artifacts...
copy /y "%ACSUTILS_DIST%\bcsutils.bcs" "%BCSUTILS_TARGET_DIR%\bcsutils.acs" >nul
copy /y "%ACSUTILS_DIST%\cvarinfo.acsutils" "%LIBSRC_DIR%\cvarinfo.acsutils" >nul
copy /y "%ACSUTILS_DIST%\decorate.acsutils" "%LIBSRC_DIR%\decorate.acsutils" >nul

echo Compile files...

:: MACRO definitions used for the different ACS files.
set "MACRO_LIB=-D DEV"
set "MACRO_CORE=-D DEV -D DEV_PLAYERCAP"

:: Included directories used with different ACS files.
:: Library uses ACSUtils, ZH2 Core uses both ACSUtils and the lbirary.
set "INCLUDE_LIBSRC=-i %ROOT%\libsrc\acs_source"
set "INCLUDE_CORE=-i %ROOT%\libsrc\acs_source -i %ROOT%\libsrc\acs_source\bcsutils"

:: Output paths for compiled ACS.
set "SRC_BCSUTILS=%ROOT%\libsrc\acs_source\bcsutils.acs"
set "OUT_BCSUTILS=%ROOT%\libsrc\acs\bcsutils.o"

set "SRC_LIB=%ROOT%\libsrc\acs_source\zh2lib.acs"
set "OUT_LIB=%ROOT%\libsrc\acs\zh2lib.o"

set "SRC_CORE=%CORE_SRC_DIR%\zh2game.acs"
set "OUT_CORE=%CORE_OUT_DIR%\zh2game.o"

echo [bcsutils]
"%BCC%" "%SRC_BCSUTILS%" "%OUT_BCSUTILS%" || exit /b 1

echo [libsrc]
"%BCC%" %INCLUDE_LIBSRC% %MACRO_LIB% "%SRC_LIB%" "%OUT_LIB%" || exit /b 1

echo [core]
"%BCC%" %INCLUDE_CORE% %MACRO_CORE% "%SRC_CORE%" "%OUT_CORE%" || exit /b 1

@echo SUCCESS

@PAUSE
