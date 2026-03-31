# 📋 PROYECTO PYME SURVEY - INFORMACIÓN COMPLETA
> Guardado el 2026-03-31 | Camila Bravo | Walmart Chile

---

## 🌐 LINKS IMPORTANTES

| Qué | URL |
|---|---|
| 🌍 Formulario original (público) | https://pyme-survey.onrender.com/ |
| ✨ Formulario nuevo (público) | https://pyme-survey.onrender.com/formulario |
| 📊 Panel de resultados (público) | https://pyme-survey.onrender.com/resultados |
| 💻 Panel local (solo tu PC) | http://localhost:8777/resultados |
| 💾 Código en GitHub | https://github.com/camidebe-cyber/pyme-survey |
| ⚙️ Dashboard Render | https://dashboard.render.com |

---

## 🖥️ SERVIDOR LOCAL

**Para iniciarlo:** doble clic en `iniciar_servidor.bat` o `run_server.bat`

```
C:\Users\c0b0w1w\Documents\puppy_workspace\pyme_survey\run_server.bat
```

**Puerto:** 8777  
**Variable de entorno:** `PUBLIC_URL=https://pyme-survey.onrender.com`

---

## 🔑 CREDENCIALES Y TOKENS

| Servicio | Usuario / Info |
|---|---|
| GitHub | https://github.com/camidebe-cyber |
| GitHub Token | ⚠️ Guardado solo en tu PC — renovar en github.com/settings/tokens/new (expira ~90 días) |
| Render | Cuenta conectada a GitHub camidebe-cyber |

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
pyme_survey/
├── main.py                  # App principal FastAPI
├── admin.py                 # Panel /resultados + exports Excel
├── db.py                    # Base de datos SQLite
├── questions.py             # ⭐ TODAS LAS PREGUNTAS AQUÍ
├── formulario_router.py     # Rutas del formulario nuevo
├── requirements.txt         # Dependencias Python
├── render.yaml              # Config despliegue Render
├── run_server.bat           # Iniciar servidor local
├── iniciar_servidor.bat     # Alternativa inicio
├── templates/
│   ├── welcome.html         # Bienvenida formulario original
│   ├── survey.html          # Preguntas formulario original
│   ├── result.html          # Resultado final
│   ├── admin.html           # Panel de resultados
│   ├── admin_detail.html    # Detalle por empresa
│   ├── formulario_welcome.html  # Bienvenida formulario nuevo
│   └── formulario_survey.html   # Preguntas formulario nuevo
```

---

## 📝 CÓMO EDITAR PREGUNTAS

Todas las preguntas están en `questions.py`.

**Para cambiar texto de pregunta:** busca `"text":` con el número de pregunta  
**Para cambiar subtítulo:** busca `"subtitle":`  
**Para cambiar alternativas:** busca `"options":`  
**Para agregar campo de texto al seleccionar:** usar:
```python
{
    "value": "valor",
    "label": "Texto visible",
    "icon": "✅",
    "has_text_followup": True,
    "followup_placeholder": "Texto del campo (máx X car.)",
    "followup_maxlength": 20,  # límite de caracteres
}
```

---

## 📊 RESUMEN PREGUNTAS (25 TOTAL)

| # | Bloque | Pregunta |
|---|---|---|
| 1 | Identificación | ¿Cómo se llama tu empresa o marca? |
| 2 | Identificación | ¿En qué categoría está tu producto? |
| 3 | Identificación | ¿Hace cuánto tiempo eres proveedor de Walmart? |
| 4 | Identificación | ¿Ingresaste al programa Potencia PyME? |
| 5 | Ecosistema | ¿Conoces tu Fill Rate actual? |
| 6 | Ecosistema | ¿Sabes qué es el In-Stock y lo monitoreas? |
| 7 | Ecosistema | ¿Tienes acceso y usas Retail Link? |
| 8 | Ecosistema | ¿Con qué frecuencia revisas el desempeño de ventas? |
| 9 | Ecosistema | ¿Conoces los requisitos para entrega en CD? |
| 10 | Ecosistema | ¿Sabes cómo tener visibilidad de inventario en sala? |
| 11 | Ecosistema | ¿Conoces y usas Phronesis? |
| 12 | Comercial | ¿Participas en actividades promocionales? |
| 13 | Comercial | ¿Sabes cómo agendar cita en el CD? |
| 14 | Comercial | ¿Tienes info de en qué locales están tus productos? |
| 15 | Comercial | ¿Con qué frecuencia tienes quiebres de stock? |
| 16 | Comercial | ¿Conoces el proceso de alzas de costo en Walmart? |
| 17 | Comercial | ¿Sabes la diferencia entre costo neto y costo limpio? |
| 18 | Negocio | ¿Conoces el Programa de Marca Propia de Walmart? |
| 19 | Negocio | ¿Quién es el representante de tu cuenta en Walmart? |
| 20 | Operacional | ¿Sabes a quién contactar cuando tienes problemas? |
| 21 | Operacional | ¿La persona que contactas te responde siempre? |
| 22 | Operacional | ¿Cuando hay un rechazo, entiendes por qué ocurrió? |
| 23 | Operacional | ¿Sabes qué es el Fee de Última Milla? |
| 24 | Operacional | ¿Sabes qué es el Fee de Reposición? |
| 25 | Operacional | ¿Tu planta tiene certificación de calidad vigente? (GFSI) |

---

## 🚀 CÓMO SUBIR CAMBIOS A RENDER

Cada vez que edites algo, ejecuta estos comandos en la terminal:

```bash
cd C:\Users\c0b0w1w\Documents\puppy_workspace\pyme_survey

# Con git portable:
"C:\Users\c0b0w1w\Documents\puppy_workspace\PortableGit\cmd\git.exe" add -A
"C:\Users\c0b0w1w\Documents\puppy_workspace\PortableGit\cmd\git.exe" commit -m "descripcion del cambio"
"C:\Users\c0b0w1w\Documents\puppy_workspace\PortableGit\cmd\git.exe" -c http.proxy=http://sysproxy.wal-mart.com:8080 -c https.proxy=http://sysproxy.wal-mart.com:8080 push origin main
```

Render detecta el push y actualiza automáticamente en ~2-3 minutos ✅

---

## 📥 EXPORTS EXCEL DISPONIBLES

| Botón | URL | Contenido |
|---|---|---|
| 🟢 Excel Completo | `/resultados/export/excel` | Todas las respuestas formateadas |
| 🟡 Contactos | `/resultados/export/contactos` | Solo RUT + Razón Social + Email |

---

## ⚠️ NOTAS IMPORTANTES

- **Render plan gratuito:** se duerme a los 15 min sin uso. La primera visita tarda ~60 seg en cargar.
- **Base de datos Render:** es efímera — si Render redespliega, los datos se borran. Para datos persistentes se necesita plan de pago con Disk.
- **Base de datos local:** se guarda en `survey.db` en la carpeta del proyecto.
- **GitHub Token:** expira en ~90 días. Renovar en https://github.com/settings/tokens/new
- **Proxy Walmart para git:** siempre usar `-c http.proxy=http://sysproxy.wal-mart.com:8080`