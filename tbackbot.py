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

gpgRecipient = os.getenv('GPG_KEY_FP') # The key fingerprint that will be able to decrypt it
tarName = os.getenv('TAR_NAME') # The name of the generated tar

dirToSend = ('/data') # Path to dir to send
tarFile = ("{}.txz".format(tarName)) # Tarfile's name
encryptedTar = ("{}.gpg".format(tarFile)) # Encrypted Tarfile's name

def createTar():
    with tarfile.open(tarFile, 'w:xz') as tar:
        tar.add(dirToSend, arcname=os.path.basename(dirToSend))
        tar.close()

def createGPG():
    gpg = gnupg.GPG()
    gpg.encoding = 'utf-8'
    stream = open(tarFile, 'rb')
    status = gpg.encrypt_file(stream,
    recipients=gpgRecipient,
    armor=False,
    always_trust=True,
    output=encryptedTar)
    print ('ok: ', status.ok)
    print ('status: ', status.status)
    print ('stderr: ', status.stderr)

def deleteTmpFiles():
    try:
        os.remove(tarFile)
        os.remove(encryptedTar)
    except:
        print("Error: Unable to find or delete file.")

# Script

# Prepare telethon
chat_id=int(chat_id)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    createTar()
    createGPG()
    await bot.send_file(chat_id, encryptedTar)
    deleteTmpFiles()
with bot:
    bot.loop.run_until_complete(main())
