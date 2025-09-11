#!/bin/bash

# This script installs the git-sync.service file into the systemd directory,
# reloads the daemon, and enables and starts the service.

# --- SCRIPT SETUP ---

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVICE_FILE="git-sync.service"
DEST_PATH="/etc/systemd/system/${SERVICE_FILE}"

# --- SANITY CHECKS ---

# Check if the service file exists in the current directory
if [[ ! -f "${SCRIPT_DIR}/${SERVICE_FILE}" ]]; then
    echo "Error: The file '${SERVICE_FILE}' was not found in the current directory."
    exit 1
fi

# Check for root permissions
if [[ "$EUID" -ne 0 ]]; then
    echo "This script must be run as root or with sudo."
    echo "Please try again with: sudo ./install_service.sh"
    exit 1
fi

# --- INSTALLATION PROCESS ---

echo "Starting installation of ${SERVICE_FILE}..."

# 1. Copy the service file to the systemd directory
echo "1. Copying ${SERVICE_FILE} to ${DEST_PATH}..."
cp "${SCRIPT_DIR}/${SERVICE_FILE}" "${DEST_PATH}"
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to copy the service file."
    exit 1
fi
echo "Service file copied successfully."

# 2. Reload the systemd daemon to recognize the new service
echo "2. Reloading systemd daemon..."
systemctl daemon-reload
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to reload systemd daemon."
    exit 1
fi
echo "Systemd daemon reloaded."

# 3. Enable the service to start on boot
echo "3. Enabling ${SERVICE_FILE} to start on boot..."
systemctl enable "${SERVICE_FILE}"
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to enable the service."
    exit 1
fi
echo "Service enabled successfully."

# 4. Start the service immediately
echo "4. Starting ${SERVICE_FILE}..."
systemctl start "${SERVICE_FILE}"
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to start the service."
    exit 1
fi
echo "Service started successfully."

# --- FINAL STATUS CHECK ---

echo ""
echo "Installation complete!"
echo "Checking the status of the service (may take a moment to become active)..."

# Give the service a moment to start
sleep 3
systemctl status "${SERVICE_FILE}" --no-pager

echo ""
echo "If the service is 'active (running)', the installation was successful."
