import logging
import re

from telethon import TelegramClient, events

from config import cfg, FILEPATH_LOGGER
from my_logging import get_logger
from enums import UN

PATTERN_DEXSCREENER = re.compile(r'https:\/\/dexscreener\.com\/solana\/\S+')

urls_dexscreener = []
client = TelegramClient(cfg.session_filepath, cfg.api_id, cfg.api_hash,  system_version="4.16.30-vxCUSTOM_qwe")
datas = [
    {'entity': UN.TradingFoundersLoungebyGotbit, 'from_user': UN.aaandryunin},
    {'entity': UN.andryuningotbit, 'from_user': None},
    {'entity': UN.andryunin_chat, 'from_user': UN.andryunin_chat}
]
chats_event_filter = [d['entity'] for d in datas]
users_filter = [d['from_user'] for d in datas if d['from_user']]


@client.on(events.NewMessage(
    chats=chats_event_filter,
    pattern=PATTERN_DEXSCREENER.search,
    from_users=users_filter
))
async def handle_message_with_urls(event):
    url = PATTERN_DEXSCREENER.search(event.raw_text).group(0)
    if url not in urls_dexscreener:
        logging.info(f'TRIGGER!!! New {url=}')
        urls_dexscreener.append(url)
        await client.send_message(UN.solana_unibot, url)
        await client.send_message(UN.hello_friend_hello_friend, f'Buying {url=}')
    else:
        logging.info(f'Already seen this {url=}')


@client.on(events.NewMessage(chats=UN.andryunin_chat))
async def handle_test(event):
    sender = await event.get_sender()
    logging.info(f'{event.message.message} | sender={sender}')


async def collect_seen_urls(data: dict[str, str]) -> None:
    async for message in client.iter_messages(**data, search='https://dexscreener.com/solana'):
        search_res = PATTERN_DEXSCREENER.search(message.raw_text)
        if search_res:
            url = search_res.group(0)
            urls_dexscreener.append(url)
        else:
            logging.info(f'Url was not found....')
    logging.info(f'Collected {len(urls_dexscreener)} dexscreener urls by {data=}')


async def main():
    # This part is IMPORTANT, because it fills the entity cache.
    await client.get_dialogs()

    for data in datas:
        await collect_seen_urls(data)


if __name__ == '__main__':
    get_logger(FILEPATH_LOGGER)
    logging.info(f"{chats_event_filter=}")
    logging.info(f'{users_filter=}')

    client.start(phone=cfg.phone, password=cfg.password)
    with client:
        try:
            client.loop.run_until_complete(main())
            client.run_until_disconnected()
        finally:
            logging.info(f'{client.is_connected()=}')
            client.session.save()
