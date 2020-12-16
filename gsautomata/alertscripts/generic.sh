#!/usr/bin/env bash

set -e

echo "<strong>Node status</strong>"
kubectl get nodes -o wide
