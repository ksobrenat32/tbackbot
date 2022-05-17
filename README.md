# Telegram Backup Bot (tbackbot)

This is a python3 script that helps to backup a directory
 to telegram which is kinda unlimited storage for free, at
 least at the moment of writing this. The directory goes
 compressed and encrypted.

## Requirements

- Telegram account
- Telegram bot
- Telegram API keys
- GPG key (For the encryption part)

## How to use

### Container

```sh
podman run -d --name tbk-test \
    --replace \
    -e TZ="" `#Timezone` \
    -e TG_BOT_TOKEN="" `#The bot token from bot father` \
    -e TG_API_ID="" `#Telegram API ID` \
    -e TG_API_HASH="" `#Telegram API hash` \
    -e TG_CHAT_ID="" `#Telegram chat id (user or channel)` \
    -e TAR_NAME="" `#Name of the generated tar` \
    -v ./data1:/data/dir1:ro,z `#The first directory to backup` \
    -v ./data2:/data/dir2:ro,z `#The second directory to backup` \
    -v ./public.key:/public.key:ro,z `#A directory with the gpg public key` \
    ghcr.io/ksobrenat32/tbackbot
```

### Repeating schedule

You may want this backups to run in an schedule, you can do it with
systemd timers.

#### Systemd

/etc/systemd/system/run-tbakbot.service

```systemd
[Unit]
Description=Podman container for backup
Wants=network-online.target
After=network-online.target
RequiresMountsFor=%t/containers

[Service]
Environment=PODMAN_SYSTEMD_UNIT=%n
TimeoutStopSec=70
ExecStartPre=/bin/rm -f %t/%n.ctr-id
ExecStart=/usr/bin/podman run --cidfile=%t/%n.ctr-id --cgroups=no-conmon --rm --sdnotify=conmon --replace -d --name tbackbot --env-file /path/to/tbackbot/env -v /backup/dir1:/data/dir1:ro,z -v /backup/dir2:/data/dir2:ro,z -v /path/to/gpg/public.key:/public.key:ro,z ghcr.io/ksobrenat32/tbackbot:latest
ExecStop=/usr/bin/podman stop --ignore --cidfile=%t/%n.ctr-id
ExecStopPost=/usr/bin/podman rm -f --ignore --cidfile=%t/%n.ctr-id
Type=notify
NotifyAccess=all

[Install]
WantedBy=default.target
```

/etc/systemd/system/run-tbakbot.timer

```systemd
[Timer]
OnCalendar=*-*-* 04:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

And just enable the timer with

```sh
sudo systemctl enable --now run-tbakbot.timer
```

## Notes

- If you are sending the file to a channel, be sure to
 have more than one user so it is not flagged as suspicious.
- DO NOT ABUSE, seriously.
