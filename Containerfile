FROM python:3-bullseye AS compile-image

# Install requirements
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt
 
FROM python:3-slim AS build-image

LABEL org.opencontainers.image.authors="https://github.com/ksobrenat32" \
    description="A docker container to backup to telegram"

# Timezone for the crontab
ENV TZ="America/Mexico_City"
# The bot token from BotFather 
ENV TG_BOT_TOKEN="" 
# The telegram API id
ENV TG_API_ID=""
# The telegram API hash
ENV TG_API_HASH="" 
# The telegram chat id (user or channel)
ENV TG_CHAT_ID=""
# The key fingerprint of the recipient
ENV GPG_KEY_FP=""
# The name of the tarbal, default is 'data'
ENV TAR_NAME="data"

# The directory to backup
VOLUME ["/data"]
# The keys directory
VOLUME ["/keys"]

# Install gnupg
RUN apt-get update -y -qq
RUN apt-get install -y -qq gpg

# Change to dir
WORKDIR /app

# Get dependencies from compile-image and add them to path
COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy python script
COPY ./tbackbot.py /app/tbackbot.py
RUN chmod +x /app/tbackbot.py

# Copy and run entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
