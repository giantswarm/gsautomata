FROM alpine:3.12

ARG KUBECTL_VERSION=1.19.5
ARG HELM_VERSION=v3.4.1

# Install jq
RUN apk add --update --no-cache jq bash

# Install kubectl and helm
RUN apk add --update --no-cache curl && \
    curl -LO https://storage.googleapis.com/kubernetes-release/release/v${KUBECTL_VERSION}/bin/linux/amd64/kubectl && \
    mv kubectl /usr/bin/kubectl && \
    chmod +x /usr/bin/kubectl && \
    wget -q https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz -O - | tar -xzO linux-amd64/helm > /usr/local/bin/helm && \
    chmod +x /usr/local/bin/helm

COPY ./ /app

WORKDIR /app

ENTRYPOINT ./executeautomation.sh
