#!/bin/bash

# Lead Research Agent - Run Script
# Starts the Streamlit application with proper environment setup

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print header
echo -e "${GREEN}"
echo "╔════════════════════════════════════════╗"
echo "║    Lead Research Agent - Starting      ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found!${NC}"
    echo "Creating .env from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .env created. Please edit it with your API keys.${NC}"
    else
        echo -e "${RED}✗ .env.example not found!${NC}"
        exit 1
    fi
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing requirements...${NC}"
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed${NC}"
    else
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Check database
echo "Setting up database..."
if [ ! -d "database" ]; then
    mkdir -p database
    echo -e "${GREEN}✓ Database directory created${NC}"
fi

# Start Streamlit
echo -e "${GREEN}"
echo "🚀 Starting Streamlit application..."
echo "📱 Open browser at: http://localhost:8501"
echo -e "${NC}"

streamlit run streamlit_app/main.py

# Exit message
echo -e "${GREEN}✓ Application closed${NC}"
