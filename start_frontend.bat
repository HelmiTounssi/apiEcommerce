@echo off
echo ======================================================================
echo 🚀 Démarrage de l'Interface E-commerce Streamlit
echo ======================================================================
echo.

REM Activation de l'environnement virtuel
echo 🔧 Activation de l'environnement virtuel...
call .\venv\Scripts\activate

REM Vérification que le backend est accessible
echo 🔍 Vérification du backend...
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend non accessible sur http://localhost:5000
    echo 💡 Veuillez démarrer le backend avec: .\start.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Backend accessible

REM Démarrage de Streamlit
echo.
echo 🚀 Démarrage de l'interface Streamlit...
echo 🌐 Interface disponible sur: http://localhost:8501
echo 🔗 Backend API: http://localhost:5000
echo ======================================================================
echo.

streamlit run frontend/app_pro.py --server.port 8501 --server.headless true

echo.
echo Interface fermée.
pause
