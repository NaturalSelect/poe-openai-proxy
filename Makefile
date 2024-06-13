# poe-openai-proxy Makefile

default: all

phony := all
all: build

phony += build
build: image

phony += image
image:
	@docker/build_image.sh

.PHONY: $(phony)