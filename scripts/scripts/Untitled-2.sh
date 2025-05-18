#!/bin/bash

kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: trigger-mutation
  namespace: default
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "100m"
        memory: "100Mi"
EOF

kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pass-without-mutation
  namespace: default
spec:``
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "10m"
        memory: "10Mi"
EOF