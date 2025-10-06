#!/usr/bin/env bash
read -p "Username: " user
read -s -p "Password: " pass
echo

mkdir -p "<MOUNT_POINT>"
sudo mount_webdav "https://$user:$pass@<WebDAV-Server-URL>" "<MOUNT_POINT>"
