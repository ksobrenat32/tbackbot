#!/usr/bin/env bash
set -e

# Running command.
CMD="/app/tbackbot.py"

# Check if variables are set
if [ -n "$TG_BOT_TOKEN" ] && [ -n "$TG_API_ID" ] && [ -n "$TG_API_HASH" ] && [ -n "$TG_CHAT_ID" ] && [ -n "$TAR_NAME" ]; then
    echo "Variables set"
else
    echo "Missing variables"
    exit 1
fi

echo '
-----------------------------
|     Starting container    |
-----------------------------
'

# If keys exists
if [[ -e /public.key ]] ; then
    # Set timezone
    rm /etc/localtime
    ln -s /usr/share/zoneinfo/${TZ} /etc/localtime
    # GPG import key and get the fingerprint
    gpg --import /public.key
    export GPG_KEY_FP=$(gpg --fingerprint --with-colons | grep fpr:: | sed 's/fpr:://g' | sed -r 's/://g' | head -n 1)
else
    echo ' 
You are missing the gpg public key, to
export it:

1. First list your keys
    gpg --list-keys

2. Export the public key to a file
    gpg --export -a <key-fingerprint> > public.key

You now can save the public.key and mount
it in /public.key inside the container.
'
    CMD="echo 'Exiting container ...'"
    echo
fi

# Run the command.
${CMD}
