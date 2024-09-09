FROM ubuntu:22.04
RUN apt update && apt install -y python3 pip
COPY . /root/poe-openai-proxy
RUN /root/poe-openai-proxy/install_python_deps.sh
RUN rm -rf /var/lib/apt/lists/*
EXPOSE 18081
ENTRYPOINT [ "/root/poe-openai-proxy/start.sh" ]