@echo off
REM Script para iniciar facilmente o projeto Oficina Moto

echo ============================================
echo 🏍️  OFICINA MOTO - Sistema de Gerenciamento
echo ============================================
echo.

setlocal enabledelayedexpansion

REM Obter o diretório atual
set "root_dir=%cd%"

echo [1] Iniciando Backend (Django)...
start cmd /k "cd %root_dir%\backend && venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak

echo [2] Iniciando Frontend (Vue 3)...
start cmd /k "cd %root_dir%\frontend && npm run dev"

echo.
echo ============================================
echo ✅ Servers iniciados!
echo.
echo 📍 Frontend:  http://127.0.0.1:5173
echo 🗄️  Backend:   http://127.0.0.1:8000
echo 👨‍💼 Admin:     http://127.0.0.1:8000/admin
echo.
echo Feche as janelas para parar os servidores.
echo ============================================

pause
