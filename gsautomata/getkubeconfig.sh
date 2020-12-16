#!/usr/bin/env bash

set -e

kubectl get secret -n $CLUSTER_ID $CLUSTER_ID-kubeconfig -o json | jq '.data | map_values(@base64d)' | jq '.kubeConfig' --raw-output > /tmp/tc_kubeconfig
chmod 500 /tmp/tc_kubeconfig
