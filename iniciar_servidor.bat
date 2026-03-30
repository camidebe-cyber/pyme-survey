@echo off
title PyME Survey - Iniciar Servidor
color 0B

echo.
echo  ============================================================
echo   WALMART CHILE - Cuestionario PyME
echo  ============================================================
echo.

:: Matar servidor anterior si estaba corriendo
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8777 ^| findstr LISTENING 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)

:: Detectar IP local actual
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0" ^| findstr /v "169.254"') do (
    set RAW_IP=%%a
)
set LOCAL_IP=%RAW_IP: =%

if "%LOCAL_IP%"=="" (
    echo  [!] No se encontro IP de red. Conectate a WiFi o activa el Hotspot.
    pause
    exit /b 1
)

:: ============================================================
:: ABRIR FIREWALL AUTOMATICAMENTE (requiere admin)
:: ============================================================
echo  Intentando abrir puerto 8777 en el Firewall de Windows...
powershell -Command "New-NetFirewallRule -DisplayName 'PyME Survey 8777' -Direction Inbound -Protocol TCP -LocalPort 8777 -Action Allow -Profile Any -ErrorAction SilentlyContinue" >nul 2>&1

:: Verificar si la regla existe ahora
powershell -Command "if (Get-NetFirewallRule -DisplayName 'PyME Survey 8777' -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" >nul 2>&1
if %errorlevel%==0 (
    set FIREWALL_OK=1
    echo  [OK] Firewall abierto correctamente.
) else (
    set FIREWALL_OK=0
    echo.
    echo  ============================================================
    echo  [!] ATENCION: El Firewall NO pudo abrirse automaticamente.
    echo      Tus compadran acceder desde su PC.
    echo.
    echo      SOLUCIONES:
    echo      1. Pide a IT abrir el puerto TCP 8777 inbound
    echo      2. Usa un Hotspot personal (ver abajo)
    echo      3. Usa Microsoft Forms como alternativa
    echo  ============================================================
    echo.
)

echo.
echo  Tu IP actual: %LOCAL_IP%

if "%FIREWALL_OK%"=="1" (
    echo  Link para companeras: http://%LOCAL_IP%:8777/
) else (
    echo  Link local (solo TU PC): http://localhost:8777/
    echo  Link de red: http://%LOCAL_IP%:8777/ ^(BLOQUEADO por Firewall^)
    echo.
    echo  ALTERNATIVA SIN IT: Conecta tu celular como Hotspot personal,
    echo  conecta tu PC y la de tu companera al mismo Hotspot,
    echo  y vuelve a ejecutar este archivo.
)
echo.
echo  Iniciando servidor...
echo.

:: Iniciar uvicorn en background
start /min "" cmd /c "cd /d "%~dp0" && .venv\Scripts\python -m uvicorn main:app --host 0.0.0.0 --port 8777"

:: Esperar que arranque
timeout /t 3 /nobreak > nul

:: Abrir el panel de resultados en el navegador
start "" "http://localhost:8777/resultados"

echo  Servidor iniciado!
echo.
echo  Panel de admin : http://localhost:8777/resultados
echo.
pause

:: Al cerrar, matar el servidor
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8777 ^| findstr LISTENING 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)
echo Servidor detenido. Hasta luego!
