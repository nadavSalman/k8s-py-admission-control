#!/bin/bash

# Set variables
WEBHOOK_NAME="py-admission-webhook.default.svc"
CERT_DIR="./certs"
DAYS_VALID=3650  # 10 years validity

# Ensure the certs directory exists
mkdir -p $CERT_DIR

echo "Generating private key and certificate..."
openssl req -x509 -newkey rsa:4096 \
    -keyout $CERT_DIR/private.key \
    -out $CERT_DIR/cert.pem \
    -days $DAYS_VALID \
    -nodes \
    -addext "subjectAltName = DNS.1:${WEBHOOK_NAME}"

# kubectl get secret admission-webhook-secret  -n default -o jsonpath="{.data.tls\.crt}" 



echo "Displaying certificate metadata..."
openssl x509 -in $CERT_DIR/cert.pem -noout -text | grep -E 'Subject:|Subject Alternative Name:'

echo "Displaying (SAN) Subject Alternative Name..."
openssl x509 -in $CERT_DIR/cert.pem -noout -ext subjectAltName

# Display generated files
ls -l $CERT_DIR

echo "Key and certificate generation complete!"



kubectl create secret tls admission-webhook-secret \
  --cert=$CERT_DIR/cert.pem \
  --key=$CERT_DIR/private.key \
  --dry-run=client -o yaml > ../deployment/webhook-tls-secret.yaml






# Apply the secret to your Kubernetes cluster
# kubectl apply -f webhook-tls-secret.yaml

echo "TLS secret created and applied successfully!"



