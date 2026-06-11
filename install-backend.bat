@echo off
echo ====================================
echo  LaabPro - Instalacion Backend
echo ====================================
echo.

cd backend

echo [1/3] Creando entorno virtual...
python -m venv venv

echo [2/3] Activando entorno...
call venv\Scripts\activate.bat

echo [3/3] Instalando dependencias...
pip install -r requirements.txt

echo.
echo ====================================
echo  INSTALACION COMPLETA!
echo ====================================
echo.
echo Siguiente paso:
echo 1. Edita backend\.env con tu API key
echo 2. Ejecuta: start-backend.bat
echo.
pause
