#!/usr/bin/env bash

set -e

./alertscripts/generic_controlplane.sh

echo "<strong>Generating TC Kubeconfig for $CLUSTER_ID.</strong>"
./getkubeconfig.sh
export KUBECONFIG="/tmp/tc_kubeconfig"
echo "<strong>Kubeconfig set.</strong>"

./alertscripts/generic.sh

if test -f "./alertscripts/$ALERTNAME.sh"; then
    echo "Executing specific automation for $ALERTNAME."
    ./alertscripts/$ALERTNAME.sh
fi
