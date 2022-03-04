#!/usr/bin/env bash
set -e

# Running command.
CMD="/app/tbackbot.py"

# Check if variables are set
if [[ -n "$TG_BOT_TOKEN" ]] && [[ -n "$TG_API_ID" ]] && [[ -n "$TG_API_HASH" ]] && [[ -n "$TG_CHAT_ID" ]] && [[ -n "$GPG_KEY_FP" ]]; then
    echo "Variables set"
else
    echo "Missing variables"
    exit 1
fi


# If keys dir is not empty
if [[ -n "$(ls -A /keys)" ]]; then
    echo '
-------------------------------------
|         Starting container        |
-------------------------------------
'
    # Set timezone
    rm /etc/localtime
    ln -s /usr/share/zoneinfo/${TZ} /etc/localtime
    # Import keys
    for file in $(ls /keys)
    do
	gpg --import /keys/${file}
    done
else
    # No keys, tell user how to create them
    echo ' 
You are missing the gpg public keys

1. List keys

    gpg --list-keys

2. Export public key

    gpg --export -a <key-fingerprint> > public.key

You now can save the public.key file in the 'keys' folder.
'
    CMD="echo 'Exiting container ...'"
    echo
fi

# Run the command.
${CMD}
