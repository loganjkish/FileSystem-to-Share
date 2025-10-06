#!/usr/bin/env bash
if [ "$(id -u)" -ne 0 ]; then
    echo "This script requires root."
    exit 1
fi

if ! command -v mount.davfs >/dev/null 2>&1; then
    echo "Davfs2 is not installed."
    if command -v pacman >/dev/null 2>&1; then
        echo "Try: sudo pacman -S davfs2"
    elif command -v apt >/dev/null 2>&1; then
        echo "Try: sudo apt install davfs2"
    elif command -v dnf >/dev/null 2>&1; then
        echo "Try: sudo dnf install davfs2"
    fi
    exit 1
fi


read -p "Username: " user
read -s -p "Password: " pass

mkdir -p "<MOUNT_POINT>"

if ! mount -t davfs "<WebDAV-Server-URL>" "<MOUNT_POINT>" -o username="$user",password="$pass"; then
    echo "Failed to mount WebDAV. Some distros require credentials in ~/.davfs2/secrets or /etc/davfs2/secrets"
    echo "See 'man davfs2' for details."
    exit 1
fi