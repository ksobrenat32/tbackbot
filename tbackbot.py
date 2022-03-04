#!/usr/bin/env python3

import os
import gnupg
import tarfile
from telethon import TelegramClient

# Configuration, fill this with your data.
bot_token = os.getenv('TG_BOT_TOKEN') # The bot token from BotFather 
api_id = os.getenv('TG_API_ID') # The API id
api_hash = os.getenv('TG_API_HASH') # The API hash
chat_id = os.getenv('TG_CHAT_ID') # The chat to send (channel or user)
toSend = "/data" # The file or directory to send  (absoloute path)
gpgRecipient = os.getenv('GPG_KEY_FP') # The key fingerprint that will be able to decrypt it

thingToSend = (os.path.abspath(toSend))
tarFile = ("{}.txz".format(thingToSend))
encryptedFile = ("{}.txz.gpg".format(thingToSend))


def createTar():
    # If it is a single file, continue as it is
    if os.path.isfile(thingToSend):
        return
    # Otherwise it is a directory, compress it
    else:
        with tarfile.open(tarFile, 'w:xz') as tar:
            tar.add(thingToSend, arcname=os.path.basename(thingToSend))
            tar.close()

def createGPG():
    gpg = gnupg.GPG()
    gpg.encoding = 'utf-8'
    # If it is a single file
    if os.path.isfile(thingToSend):
        stream = open(thingToSend, 'rb')
        status = gpg.encrypt_file(stream,
        recipients=gpgRecipient,
        armor=False,
        always_trust=True,
        output=thingToSend + ".gpg")
    # If it is a dir, use encypt tarfile
    else:
        stream = open(tarFile, 'rb')
        status = gpg.encrypt_file(stream,
        recipients=gpgRecipient,
        armor=False,
        always_trust=True,
        output=thingToSend + ".txz.gpg")
        print ('ok: ', status.ok)
        print ('status: ', status.status)
        print ('stderr: ', status.stderr)

def deleteTmpFiles():
    try:
        if os.path.isfile(thingToSend):
            os.remove(encryptedFile)
        else:
            os.remove(tarFile)
            os.remove(encryptedFile)
    except:
        print("Error: Unable to find or delete file.")

# Script

# Prepare telethon
chat_id=int(chat_id)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    createTar()
    createGPG()
    await bot.send_file(chat_id, encryptedFile)
    deleteTmpFiles()
with bot:
    bot.loop.run_until_complete(main())
