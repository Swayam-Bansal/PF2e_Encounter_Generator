#!/bin/bash
set -e  # Exit on error
PYTHON_VERSION="3.13.0"
# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)     PLATFORM=linux;;
    Darwin*)    PLATFORM=mac;;
    CYGWIN*|MINGW*|MSYS*) PLATFORM=windows;;
    *)          PLATFORM="unknown"
esac
echo "Detected OS: $PLATFORM"
# Check for correct Python version
PYTHON=$(which python3 || which python)
PYTHON_VER=$($PYTHON -V 2>&1)
if [[ "$PYTHON_VER" != *"$PYTHON_VERSION"* ]]; then
    echo " Python $PYTHON_VERSION not found. Found: $PYTHON_VER"
    echo "Please install Python $PYTHON_VERSION and ensure it's the default."
    exit 1
fi
# Create virtual environment
$PYTHON -m venv bootDev_hackathon2025
# Activate venv based on platform
if [ "$PLATFORM" = "windows" ]; then
    ACTIVATE_SCRIPT="venv/Scripts/activate"
else
    ACTIVATE_SCRIPT="venv/bin/activate"
fi
echo "Activating virtual environment..."
source "$ACTIVATE_SCRIPT"
# Upgrade pip & install requirements
pip install --upgrade pip
pip install -r requirements.txt
echo "Required dependencies successfully installed...!"
echo "If virtual env did not activate, please run the following command in the open terminal:"
echo "  source $ACTIVATE_SCRIPT"
