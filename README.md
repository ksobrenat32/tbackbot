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

### 1. Install dependencies

```sh
pip install -r requirements
```

### 2. Fill the data

You need to edit the configuration inside the script with data like
 [Telegram API Keys](https://docs.telethon.dev/en/stable/basic/signing-in.html)
 and the path to the file or directory to backup.

### 3. Add the script to a cronjob

You can run it all the times you want but dont abuse it, so you
 won’t get flagged.

```cronjob
0 4 * * * /path/to/tbakbot.py
```

## Notes

- If you are sending the file to a channel, be sure to
 have more than one user so it is not suspicious.
- DO NOT ABUSE, seriously.
