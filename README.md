# Telegram Backup Bot (tbackbot)

This is a python3 script that helps to backup a directory or file
 to telegram which is kinda unlimited storage for free, at least
 at the moment of writing this.

The file goes encrypted, if it is a directory it also goes compressed.

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
    -e TG_BOT_TOKEN="" `#The bot token` \
    -e TG_API_ID="" `#Telegram API ID` \
    -e TG_API_HASH="" `#Telegram API hash` \
    -e TG_CHAT_ID="" `#Telegram chat id` \
    -e GPG_KEY_FP="" `#GnuPG key fingerprint` \
    -v ./data1:/data/dir1:z `#The first directory to backup` \
    -v ./data2:/data/dir2:z `#The second directory to backup` \
    -v ./keys:/keys:z `#A directory with the gpg public key` \
    ghcr.io/ksobrenat32/tbackbot
```

### Manual

#### 1. Install dependencies

```sh
pip install -r requirements
```

#### 2. Fill the data

You need to edit the configuration inside the script with data like
 [Telegram API Keys](https://docs.telethon.dev/en/stable/basic/signing-in.html)
 , the path to the file, the gpg key fingerprint and directory to backup.

#### 3. Run it

You can run it all the times you want but dont abuse it, or you
 may become get flagged.

 ```sh
/path/to/tbakbot.py
 ```

## Repeating schedule

You may want this backups to run in an schedule, you can do it with
systemd timers.

### Systemd

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
ExecStart=/usr/bin/podman run --cidfile=%t/%n.ctr-id --cgroups=no-conmon --rm --sdnotify=conmon --replace -d --name tbackbot --env-file /path/to/tbackbot/.env -v /backup/dir1:/data/dir1:ro,z -v /backup/dir2:/data/dir2:ro,z -v /backup/gpg/keys:/keys:z ghcr.io/ksobrenat32/tbackbot:latest
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
