#!/usr/bin/env bash

set -e

echo "<strong>Helm Status</strong>"
helm ls -A

echo "<strong>Helm App Status</strong>"
helm status $DEPLOYMENT -n $NAMESPACE

echo "<strong>Pod status</strong>"
kubectl get pods -n $NAMESPACE | grep $DEPLOYMENT

echo "<strong>App Logs</strong>"
kubectl logs deployment/$DEPLOYMENT -n $NAMESPACE --tail=100
