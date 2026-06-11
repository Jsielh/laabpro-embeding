@echo off
echo ====================================
echo  LaabPro Backend - Iniciando...
echo ====================================
echo.

cd backend
call venv\Scripts\activate.bat

echo Backend ejecutandose en http://localhost:8000
echo.
echo Presiona Ctrl+C para detener
echo.

python run.py
