# Eva - iAsistente en Depilación Láser

Chatbot de asistencia para SinVello usando OpenAI Responses API y Streamlit.

## Requisitos

- Docker y Docker Compose
- API Key de OpenAI
- Service Account de Google (para guardar conversaciones en Google Sheets)

## Configuración

1. Copia el archivo de ejemplo de variables de entorno:
```bash
cp .env.example .env
```

2. Edita `.env` con tus credenciales:
```
OPENAI_API_KEY=sk-tu-api-key
```

3. Coloca tu archivo `proyecto-eva-service-account.json` en el directorio raíz.

## Despliegue

```bash
docker-compose up -d --build
```

## Migración de Assistants API

Este proyecto fue migrado de la Assistants API (deprecated agosto 2026) a la nueva Responses API.

Cambios principales:
- `beta.threads` → `conversations`
- `beta.threads.runs` + polling → `responses.create` (una sola llamada)
- Las instrucciones del assistant van ahora en el parámetro `instructions` o en un Prompt del Dashboard
