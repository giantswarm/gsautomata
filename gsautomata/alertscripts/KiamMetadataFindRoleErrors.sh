#!/usr/bin/env bash

set -e

echo "<strong>Kiam Pods Status</strong>"
kubectl get pods -n kube-system | grep kiam

echo "<strong>Kiam Server Logs</strong>"
kubectl logs daemonset/kiam-server -n kube-system --tail=100

echo "<strong>Kiam Agent Logs</strong>"
kubectl logs daemonset/kiam-agent -n kube-system --tail=10 > /tmp/agent_logs.txt
cat /tmp/agent_logs.txt

if grep -q "certificate signed by unknown authority" "/tmp/agent_logs.txt"; then
    echo "<strong>Certificate issue detected, restarting kiam-agent pods</strong>"
    kubectl delete secret kiam-agent-tls -n kube-system
    kubectl rollout restart daemonset/kiam-agent -n kube-system
fi
