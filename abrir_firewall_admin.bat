@echo off
title Abrir Firewall Puerto 8777 - PyME Survey

:: ============================================================
:: Auto-elevacion a Administrador
:: ============================================================
net session >nul 2>&1
if %errorlevel% == 0 goto :ADMIN_OK

echo Solicitando permisos de administrador...
powershell -Command "Start-Process '%~f0' -Verb RunAs"
exit /b

:ADMIN_OK
echo.
echo  ============================================================
echo   WALMART - Abriendo puerto 8777 en el Firewall
echo  ============================================================
echo.

:: Eliminar regla anterior si existe (para evitar duplicados)
netsh advfirewall firewall delete rule name="PyME Survey 8777" >nul 2>&1

:: Crear la regla de entrada
netsh advfirewall firewall add rule name="PyME Survey 8777" ^^
    protocol=TCP dir=in localport=8777 action=allow

if %errorlevel%==0 (
    echo.
    echo  [OK] Firewall abierto correctamente en el puerto 8777!
    echo.
    echo  Tus companeros pueden acceder en:
    for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0" ^| findstr /v "169.254"') do (
        set RAW_IP=%%a
    )
    echo  http://%RAW_IP: =%:8777/
    echo.
) else (
    echo.
    echo  [ERROR] No se pudo abrir el firewall. Contacta a IT.
    echo.
)

pause
