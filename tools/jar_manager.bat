@echo off
setlocal enabledelayedexpansion

:: Configuration
set "JAVA_HOME=d:\Fractal Softworks\Starsector\jre"
set "JAVA=%JAVA_HOME%\bin\java.exe"
set "OUTPUT_DIR=%~dp0..\jar_content"
set "BACKUP_DIR=%OUTPUT_DIR%\backups"
set "TIMESTAMP=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
set "TIMESTAMP=%TIMESTAMP: =0%"

:: Vérification de Java
if not exist "%JAVA%" (
    echo Erreur: Java non trouvé dans %JAVA_HOME%
    exit /b 1
)

:: Création des répertoires
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

:: Fonction d'aide
if "%1"=="" goto :usage
if "%1"=="help" goto :usage
if "%1"=="--help" goto :usage

:: Actions principales
if "%1"=="extract" goto :extract
if "%1"=="list" goto :list
if "%1"=="backup" goto :backup

echo Action non reconnue: %1
goto :usage

:extract
if "%2"=="" (
    echo Erreur: Spécifiez le chemin du JAR à extraire
    goto :usage
)
echo Extraction de %2...
set "JAR_PATH=%2"
set "EXTRACT_DIR=%OUTPUT_DIR%\%~n2_%TIMESTAMP%"
mkdir "%EXTRACT_DIR%"

:: Backup avant extraction
call :backup "%JAR_PATH%"

:: Extraction avec Java
"%JAVA%" -jar "%JAR_PATH%" -extract "%EXTRACT_DIR%"
if errorlevel 1 (
    echo Erreur lors de l'extraction
    exit /b 1
)
echo Extraction terminée dans %EXTRACT_DIR%
goto :eof

:list
if "%2"=="" (
    echo Erreur: Spécifiez le chemin du JAR à lister
    goto :usage
)
echo Contenu de %2:
"%JAVA%" -jar "%2" -list
goto :eof

:backup
if "%2"=="" (
    echo Erreur: Spécifiez le chemin du JAR à sauvegarder
    goto :usage
)
echo Création d'une sauvegarde de %2...
copy "%2" "%BACKUP_DIR%\%~n2_%TIMESTAMP%%~x2"
if errorlevel 1 (
    echo Erreur lors de la sauvegarde
    exit /b 1
)
echo Sauvegarde créée: %BACKUP_DIR%\%~n2_%TIMESTAMP%%~x2
goto :eof

:usage
echo.
echo Gestionnaire de JAR pour Starsector
echo Usage:
echo   jar_manager.bat extract ^<jar_path^>  : Extrait le contenu du JAR
echo   jar_manager.bat list ^<jar_path^>     : Liste le contenu du JAR
echo   jar_manager.bat backup ^<jar_path^>   : Crée une sauvegarde du JAR
echo.
echo Exemples:
echo   jar_manager.bat extract "d:\Fractal Softworks\Starsector\starsector-core\starfarer.api.jar"
echo   jar_manager.bat list "d:\Fractal Softworks\Starsector\starsector-core\starfarer.api.jar"
echo.
exit /b 0

:eof
exit /b 0
