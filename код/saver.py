from telethon.tl.types import PeerChannel
from telethon import TelegramClient, events
from telethon import functions, types
from telethon.tl.functions.messages import SendReactionRequest
from telethon.sync import TelegramClient
import re
import sys

import shutil
import os
# Открытия папки numb.txt
f = open("Channels/chat.txt", "r")
user = open("you_user.txt", "r")

conf = f.read().split("\n")

cchennal = conf[0:-1]
print(f"Каналы которые я пройду: {cchennal}")

conf = user.read().split("\n")
api_id = conf[0]
api_hash = conf[1]
phone_number = conf[2]
lem_mes = int(conf[3])


client = TelegramClient(phone_number, api_id, api_hash,
                        system_version='4.16.30-vxCUSTOM')

async def main():
    await client.start(phone_number)
    print("Подключено к Telegram")

    for i in range(1, len(cchennal)+1):
        channel_id = cchennal[i - 1]
        channel = await client.get_entity(int(channel_id))
        s = 1
        numb_mes = re.findall(r'\d+', str(channel.title))
        lemit = int(numb_mes[-1])
        async for message in client.iter_messages(PeerChannel(channel_id=int(cchennal[i-1])), limit=lem_mes, reverse=True):
            if lemit != 0:
                if isinstance(message.text, str):
                    s = 1
                    text_m = message.text
                    if not message.reactions == None:

                        if str(message.reactions).find('results=[]') == -1:
                            s = 0

                if s == 1:
                    if message.media:
                        def progress(current, total):
                            percent = current * 100 / total
                            sys.stdout.write(f"\r Загрузка: {percent:.2f}%")
                            sys.stdout.flush()

                        channel = await client.get_entity(int(channel_id))
                        print('Начало скачивания')
                        downloaded_file = await message.download_media(f"Channels/{channel.title}/{text_m}", progress_callback=progress)
                        print(f"✅ Файл скачан в: {downloaded_file,}")

                        shutil.copy('a1.exe', f"Channels/{channel.title}/")

                        # Реакция
                        await client(SendReactionRequest(
                            peer=PeerChannel(channel_id=int(cchennal[i - 1])),
                            msg_id=message.id,
                            reaction=[types.ReactionEmoji(
                                emoticon='❤️'
                            )]
                        ))

                        # Уменьшение лимита
                        lemit-=1

    await client.disconnect()
    print("Отключено от Telegram")
    print("Готово!")


with client:
    client.loop.run_until_complete(main())
