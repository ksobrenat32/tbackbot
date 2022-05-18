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
tarName = os.getenv('TAR_NAME') # The name of the generated tar

gpgRecipient = os.getenv('GPG_KEY_FP') # The key fingerprint that will be able to decrypt it

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
    
def splitFile():
    try:
        split_command = ' '.join(["split -d -b 1G --additional-suffix='.split'", encryptedTar, encryptedTar])
        os.system(split_command)
    except:
        print("Error: Unable to use the split program.")
    

def deleteTmpFiles():
    try:
        dir_files = os.listdir()
        for file in dir_files:
            if file.endswith(".split"):
                os.remove(file)
        os.remove(tarFile)
        os.remove(encryptedTar)
    except:
        print("Error: Unable to find or delete file.")

# Script

# Prepare telethon
chat_id=int(chat_id)
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def main():
    print("Creating tar ...")
    createTar()
    print("Encrypting with gpg ...")
    createGPG()
    file_size = os.path.getsize(encryptedTar)
    if ( file_size > 1610612736 ):
        print("Encrypted tar file Size is bigger than 1.5G spliting to 1G files") 
        splitFile()
        dir_files = os.listdir()
        for file in dir_files:
            if file.endswith(".split"):
                print("Sending file", file)
                await bot.send_file(chat_id, file)
    else:
        print("Sending file", encryptedTar)
        await bot.send_file(chat_id, encryptedTar)
    deleteTmpFiles()

with bot:
    bot.loop.run_until_complete(main())
