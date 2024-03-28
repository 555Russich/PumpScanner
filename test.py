import logging
import re
from datetime import datetime, timezone

from telethon import TelegramClient, events

from config import cfg, FILEPATH_LOGGER
from my_logging import get_logger
from enums import UN

client = TelegramClient(cfg.session_filepath, cfg.api_id, cfg.api_hash,  system_version="4.16.30-vxCUSTOM_qwe")


# @client.on(events.NewMessage(chats=UN.andryunin_chat))
async def handle_test(event):
    delta = (datetime.now(timezone.utc) - event.message.date).seconds
    logging.info(f'{delta=} | {event.message.message}')
    # sender = await event.get_sender()
    # logging.info(f'{event.message.message} | sender={sender}')


async def main():
    chat = await client.get_entity(UN.andryunin_chat)
    event = events.NewMessage(chats=chat, incoming=True)
    client.add_event_handler(callback=handle_test, event=event)


if __name__ == '__main__':
    get_logger(FILEPATH_LOGGER)

    client.start(phone=cfg.phone, password=cfg.password)
    logging.info(f'{client.is_connected()=}')

    with client:
        try:
            client.loop.run_until_complete(main())
            client.run_until_disconnected()
        finally:
            logging.info(f'{client.is_connected()=}')
            client.session.save()
