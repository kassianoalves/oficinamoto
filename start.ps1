# Script PowerShell para iniciar Oficina Moto

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🏍️  OFICINA MOTO - Sistema de Gerenciamento" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$root_dir = Get-Location

# Função para iniciar em nova janela
function Start-InNewWindow {
    param(
        [string]$Title,
        [string]$WorkingDirectory,
        [string]$Command
    )
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$WorkingDirectory'; $Command" -WindowStyle Normal
}

Write-Host "[1] Iniciando Backend (Django)..." -ForegroundColor Yellow
$backend_cmd = "& '$(Join-Path $root_dir 'backend' 'venv' 'Scripts' 'activate.ps1')'; python manage.py runserver"
Start-InNewWindow -Title "Backend - Oficina Moto" -WorkingDirectory "$root_dir\backend" -Command $backend_cmd

Start-Sleep -Seconds 3

Write-Host "[2] Iniciando Frontend (Vue 3)..." -ForegroundColor Yellow
$frontend_cmd = "npm run dev"
Start-InNewWindow -Title "Frontend - Oficina Moto" -WorkingDirectory "$root_dir\frontend" -Command $frontend_cmd

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "✅ Servers iniciados!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend:  http://127.0.0.1:5173" -ForegroundColor Green
Write-Host "🗄️  Backend:   http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "👨‍💼 Admin:     http://127.0.0.1:8000/admin" -ForegroundColor Green
Write-Host ""
Write-Host "Feche as janelas para parar os servidores." -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan

Read-Host "Pressione ENTER para fechar este terminal"
