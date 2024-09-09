FROM ubuntu:22.04
RUN apt update && apt install -y python3 pip
COPY . /root/poe-openai-proxy
RUN pip install -r /root/poe-openai-proxy/requirement.txt
RUN rm -rf /var/lib/apt/lists/*
EXPOSE 18081
ENTRYPOINT [ "/root/poe-openai-proxy/start.sh" ]