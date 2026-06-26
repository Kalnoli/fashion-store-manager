#!/bin/bash
# Script de inicio para Fashion Store Manager

# Colores para la terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}       ${YELLOW}👗 Fashion Store Manager v1.0${NC}                      ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}       Sistema de Gestión de Tienda de Ropa          ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚡ Creando entorno virtual...${NC}"
    python3 -m venv venv
fi

# Activar entorno virtual
echo -e "${YELLOW}🔧 Activando entorno virtual...${NC}"
source venv/bin/activate

# Instalar dependencias
echo -e "${YELLOW}📦 Instalando dependencias...${NC}"
pip install -q -r requirements.txt

# Limpiar pantalla
clear

# Iniciar aplicación
echo -e "${GREEN}✅ Todo listo!${NC}"
echo -e "${BLUE}🚀 Iniciando Fashion Store Manager...${NC}"
echo ""
echo -e "Abre tu navegador en: ${GREEN}http://localhost:8501${NC}"
echo -e "Presiona ${YELLOW}Ctrl+C${NC} para detener la aplicación"
echo ""

# Ejecutar Streamlit
streamlit run app.py --server.headless true --server.address 0.0.0.0 --server.port 8501