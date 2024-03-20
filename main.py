import logging
import re

from telethon import TelegramClient, events

from config import cfg, FILEPATH_LOGGER
from my_logging import get_logger

PATTERN_DEXSCREENER = re.compile(r'https:\/\/dexscreener\.com\/solana\/\S+')

urls_dexscreener = []
client = TelegramClient(cfg.session_filepath, cfg.api_id, cfg.api_hash,  system_version="4.16.30-vxCUSTOM_qwe")


@client.on(events.NewMessage(chats=['https://t.me/TradingFoundersLoungebyGotbit'],
                             pattern=PATTERN_DEXSCREENER.search,
                             from_users=['Russich555', cfg.username_andrynin]
                             ))
async def handle_message_with_urls(event):
    url = PATTERN_DEXSCREENER.search(event.raw_text).group(0)
    if url not in urls_dexscreener:
        logging.info(f'TRIGGER!!! New {url=}')
        urls_dexscreener.append(url)

        await client.send_message('solana_unibot', url)
        await client.send_message('hello_friend_hello_friend', f'Buying {url=}')
    else:
        logging.info(f'Already seen this {url=}')


async def collect_seen_urls():
    # This part is IMPORTANT, because it fills the entity cache.
    dialogs = await client.get_dialogs()

    chat_trading_founders = await client.get_entity('https://t.me/TradingFoundersLoungebyGotbit')
    user_andrynin = await client.get_entity(cfg.username_andrynin)

    async for message in client.iter_messages(
            chat_trading_founders,
            from_user=user_andrynin,
            search='https://dexscreener.com/solana',
    ):
        search_res = PATTERN_DEXSCREENER.search(message.raw_text)
        if search_res:
            url = search_res.group(0)
            urls_dexscreener.append(url)
        else:
            logging.info(f'Url was not found....')
    logging.info(f'Collected {len(urls_dexscreener)} dexscreener urls')


async def main():
    await collect_seen_urls()

    # me = await client.get_me()
    # print(me.stringify())
    #
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)


if __name__ == '__main__':
    get_logger(FILEPATH_LOGGER)

    client.start(phone=cfg.phone, password=cfg.password)
    with client:
        try:
            client.loop.run_until_complete(main())
            client.loop.run_forever()
        finally:
            logging.info(f'{client.is_connected()=}')
            client.session.save()
