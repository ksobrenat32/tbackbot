FROM python:3-bullseye AS compile-image

# Install requirements
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
 
FROM python:3-slim AS build-image

LABEL org.opencontainers.image.authors="https://github.com/ksobrenat32" \
    description="A docker container to backup to telegram"

# Get dependencies from compile-image and add them to path
COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Enviroment variables
ENV TZ="America/Mexico_City"
ENV TG_BOT_TOKEN="" 
ENV TG_API_ID=""
ENV TG_API_HASH="" 
ENV TG_CHAT_ID=""
ENV TAR_NAME="data"

# The directory to backup
VOLUME ["/data"]

# Install gnupg
RUN apt-get update -y && \
    apt-get install -y gpg && \
    rm -rf /var/lib/apt/lists/*

# Change to dir
WORKDIR /app

# Copy python script
COPY ./tbackbot.py /app/tbackbot.py
RUN chmod +x /app/tbackbot.py

# Copy and run entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
