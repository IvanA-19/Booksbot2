from telethon import TelegramClient
import time
# Вставляем api_id и api_hash
api_id = 25953491
api_hash = '0dcfded0957fadec3183fdba02d088b3'

client = TelegramClient('test', api_id, api_hash)
async def main():
    await client.send_message('DjohnT_bot', '/Start')

client.start()
