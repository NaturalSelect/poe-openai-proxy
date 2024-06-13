#!/bin/bash

source docker/version.sh

POE_CONTAINER="naturalselect/poe-proxy:${TAG}"

docker build -t ${POE_CONTAINER} . -f docker/Dockerfile