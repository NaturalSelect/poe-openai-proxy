# poe-openai-proxy Makefile

default: all

phony := all
all: build

phony += build
build: docker

phony += docker
docker:
	@build/build_docker.sh

.PHONY: $(phony)