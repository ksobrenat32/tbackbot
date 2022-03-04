#!/usr/bin/env python3

import os
import gnupg
import tarfile
from telethon import TelegramClient

# Configuration, fill this with your data.
bot_token = "" # The bot token from BotFather 
api_id = "" # The API id
api_hash = "" # The API hash
chat_id = "" # The chat to send (channel or user)
toSend = "" # The file or directory to send  (absoloute path)
gpgRecipient = "" # The key fingerprint that will be able to decrypt it

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
        output=thingToSend + ".gpg")
    # If it is a dir, use encypt tarfile
    else:
        stream = open(tarFile, 'rb')
        status = gpg.encrypt_file(stream,
        recipients=gpgRecipient,
        armor=False,
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
