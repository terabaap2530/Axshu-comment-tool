#!/bin/bash
echo "[+] Installing AXSHU Server Tool..."
echo "[+] Updating packages..."
pkg update && pkg upgrade -y

echo "[+] Installing Python..."
pkg install python -y

echo "[+] Installing required Python packages..."
pip install requests

echo "[+] Making script executable..."
chmod +x axshu-tool.py

echo "[+] Installation complete!"
echo "[+] Run: python axshu-tool.py to start the tool"
