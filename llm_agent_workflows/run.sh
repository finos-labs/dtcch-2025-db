#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 Setting up Multi-Agent System...${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

# Check if virtualenv is installed
if ! command -v python3 -m venv &> /dev/null; then
    echo -e "${BLUE}📦 Installing virtualenv...${NC}"
    python3 -m pip install --user virtualenv
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}🔧 Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}🔌 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}📚 Installing dependencies...${NC}"
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}⚠️  No .env file found. Creating template...${NC}"
    cat > .env << EOL
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token
EOL
    echo -e "${RED}⚠️  Please edit .env file with your AWS credentials before running the application.${NC}"
    exit 1
fi

# Run the application
echo -e "${GREEN}🚀 Starting Multi-Agent System...${NC}"
echo ""
python main.py
