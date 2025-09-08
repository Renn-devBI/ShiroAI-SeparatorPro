#!/bin/bash
echo "Building ShiroAI Separator Pro..."
echo ""

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install spleeter from local directory if available
if [ -d "spleeter" ]; then
    pip install -e spleeter/
else
    echo "Warning: spleeter directory not found. Make sure to include spleeter in the build directory."
fi

# Build executable
python build_exe.py

echo ""
echo "Build completed! Check the 'dist' folder."