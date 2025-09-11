@echo off
echo ======================================================================
echo 🚀 Démarrage de l'Application E-commerce Complète
echo ======================================================================
echo.

REM Activation de l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call .\venv\Scripts\activate

REM Démarrage du backend en arrière-plan
echo 🚀 Démarrage du backend...
start "Backend API" cmd /k "python start.py"

REM Attendre que le backend démarre
echo ⏳ Attente du démarrage du backend...
timeout /t 5 /nobreak >nul

REM Vérification que le backend est accessible
echo 🔍 Vérification du backend...
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend non accessible
    echo ⏳ Attente supplémentaire...
    timeout /t 5 /nobreak >nul
    curl -s http://localhost:5000 >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Impossible de démarrer le backend
        pause
        exit /b 1
    )
)

echo ✅ Backend accessible sur http://localhost:5000

REM Démarrage du frontend
echo.
echo 🚀 Démarrage du frontend...
echo 🌐 Interface disponible sur: http://localhost:8501
echo 🔗 Backend API: http://localhost:5000
echo ======================================================================
echo.

streamlit run frontend/app_pro.py --server.port 8501 --server.headless true

echo.
echo Application fermée.
pause
