#!/usr/bin/env bash

set -e

echo "<strong>Pod status in kube-system namespace</strong>"
kubectl get pods -n kube-system | grep coredns

echo "<strong>Deployment status</strong>"
kubectl describe deployment -n kube-system coredns
