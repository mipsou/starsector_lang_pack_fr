@echo off
set "JAVA=d:\Fractal Softworks\Starsector\jre\bin\java.exe"

if "%~1"=="" (
    echo Usage: extract_jar.bat ^<jar_file^>
    exit /b 1
)

"%JAVA%" -jar "%~1" -list
