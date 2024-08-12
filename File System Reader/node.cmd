
@REM @ECHO off
@REM SETLOCAL
@REM CALL :find_dp0

@REM IF EXIST "%dp0%\node.exe" (
@REM   SET "_prog=%dp0%\node.exe"
@REM ) ELSE (
@REM   SET "_prog=node"
@REM   SET PATHEXT=%PATHEXT:;.JS;=;%
@REM )

@REM "%_prog%"  "%dp0%\node_modules\http-server\bin\http-server" %* 
@REM ENDLOCAL
@REM @REM node node.js
@REM EXIT /b %errorlevel%
@REM :find_dp0
@REM SET dp0=%~dp0
@REM EXIT /b

@REM http-server --no-cache
@REM node node.js
nodemon node.js
