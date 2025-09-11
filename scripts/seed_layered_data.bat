@echo off
echo Peuplement de la base de donnees
echo =================================

cd /d "%~dp0"

echo Activation de l'environnement virtuel...
call ..\venv\Scripts\activate.bat

echo.
echo Peuplement de la base de donnees avec des donnees de test...
python seed_layered_data.py

echo.
echo Peuplement termine!
pause

