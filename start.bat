@echo off
echo Activation de l'environnement virtuel...
call .\venv\Scripts\activate.bat
echo.
echo Lancement de l'API E-commerce avec Architecture en Couches...
python start.py
pause

