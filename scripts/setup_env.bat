@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
set PATH=%PATH%;%USERPROFILE%\AppData\Roaming\Python\Python313\Scripts

echo === Configuration de l'environnement ===
echo.
python scripts/check_env.py

if errorlevel 1 (
    echo Erreur lors de la configuration
    pause
    exit /b 1
)

echo.
echo Configuration terminée
echo.
