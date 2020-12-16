#!/usr/bin/env bash

set -e

echo "<strong>Cluster status on Control Plane</strong>"

kubectl describe awscluster -n default $CLUSTER_ID
echo "<br>"
kubectl describe awscontrolplane -n default -l giantswarm.io/cluster=$CLUSTER_ID
echo "<br>"
kubectl describe awsmachinedeployments -n default -l giantswarm.io/cluster=$CLUSTER_ID
echo "<br>"
kubectl get apps -n $CLUSTER_ID
echo "<br>"
echo "<br>"
echo "<br>"
