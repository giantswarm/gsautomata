kubectl delete secret kiam-ca-tls -n kube-system
kubectl delete secret kiam-server-tls -n kube-system
kubectl rollout restart daemonset/kiam-server -n kube-system
kubectl rollout restart deployment/external-dns -n kube-system
