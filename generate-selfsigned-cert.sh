#!/usr/bin/env bash
set -euo pipefail

CERT_DIR=${1:-./certs}
DOMAIN=${2:-localhost}
DAYS=${3:-365}

mkdir -p "$CERT_DIR"

openssl req -x509 -nodes -newkey rsa:4096 -days "$DAYS" -keyout "$CERT_DIR/privkey.pem" -out "$CERT_DIR/fullchain.pem" -subj "/CN=$DOMAIN"

chmod 600 "$CERT_DIR/privkey.pem" "$CERT_DIR/fullchain.pem"

echo "Self-signed certificate generated:"
echo "  Certificate: $CERT_DIR/fullchain.pem"
echo "  Private Key: $CERT_DIR/privkey.pem"
echo "Mount $CERT_DIR/fullchain.pem to /etc/ssl/certs/fullchain.pem and privkey.pem to /etc/ssl/private/privkey.pem in nginx container."