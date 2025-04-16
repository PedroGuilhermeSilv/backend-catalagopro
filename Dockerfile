FROM python:3.11-slim

# Install necessary packages including bash
RUN apt update -y && apt-get upgrade -y && apt install -y --no-install-recommends \
    bash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install pdm

WORKDIR /home/python/app

COPY . /home/python/app

# Make the script executable and ensure it's using bash
RUN chmod +x /home/python/app/commands.sh && \
    sed -i '1s|^|#!/bin/bash\n|' /home/python/app/commands.sh

EXPOSE 8000

CMD ["/bin/bash", "/home/python/app/commands.sh"]