#!/bin/bash

if [ -z "${POE_DEVCONTAINER_TAG}" ]
then
    POE_DEVCONTAINER_TAG="naturalselect/poe-openai-proxy"
fi

if [ -z "${POE_VERSION}" ]
then
    POE_VERSION="v1.0.0"
fi

POE_CONTAINER="${POE_DEVCONTAINER_TAG}:${POE_VERSION}"

docker build -t ${POE_CONTAINER} . -f docker/Dockerfile