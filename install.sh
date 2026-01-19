#!/bin/bash

# ===========================================
# Script de instalación de Eva - SinVello
# ===========================================

set -e

echo ""
echo "========================================="
echo "   Instalador de Eva - SinVello"
echo "========================================="
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}Error: Ejecuta este script desde el directorio del proyecto${NC}"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creando archivo .env...${NC}"
    cat > .env << 'EOF'
# OpenAI API Key
OPENAI_API_KEY=sk-proj-5E82dmCOghXO1fiFnURfT3BlbkFJO5RgT6lApGIw4aZuK3CZ

# Google Sheets (opcional - cambia si usas otro spreadsheet)
SPREADSHEET_ID=1qWlfX_inOnDdK5GtJzX3n_0dutbnEYssEjuR9yudN-o
EOF
    echo -e "${GREEN}Archivo .env creado${NC}"
else
    echo -e "${YELLOW}Archivo .env ya existe, no se sobreescribe${NC}"
fi

# Verificar archivos necesarios
echo ""
echo "Verificando archivos necesarios..."

if [ ! -f "proyecto-eva-service-account.json" ]; then
    echo -e "${RED}FALTA: proyecto-eva-service-account.json${NC}"
    echo "       Copia este archivo manualmente desde tu backup"
    MISSING_FILES=1
else
    echo -e "${GREEN}OK: proyecto-eva-service-account.json${NC}"
fi

if [ ! -f "sinvello_logo.png" ]; then
    echo -e "${RED}FALTA: sinvello_logo.png${NC}"
    echo "       Copia este archivo manualmente desde tu backup"
    MISSING_FILES=1
else
    echo -e "${GREEN}OK: sinvello_logo.png${NC}"
fi

if [ -n "$MISSING_FILES" ]; then
    echo ""
    echo -e "${YELLOW}Faltan archivos. Cópialos antes de continuar:${NC}"
    echo "  cp /ruta/backup/proyecto-eva-service-account.json ."
    echo "  cp /ruta/backup/sinvello_logo.png ."
    echo ""
    read -p "Presiona Enter cuando hayas copiado los archivos..."
fi

# Construir y levantar
echo ""
echo -e "${YELLOW}Construyendo imagen Docker...${NC}"
docker-compose build --no-cache

echo ""
echo -e "${YELLOW}Levantando contenedor...${NC}"
docker-compose up -d

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}   Eva instalada correctamente!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "URL: https://eva.sinvelloporlaser.es"
echo ""
echo "Comandos útiles:"
echo "  docker-compose logs -f    # Ver logs"
echo "  docker-compose restart    # Reiniciar"
echo "  docker-compose down       # Parar"
echo ""
