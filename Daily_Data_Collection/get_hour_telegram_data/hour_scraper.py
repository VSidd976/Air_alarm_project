import os
import json
import asyncio
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
import sys
import pandas as pd
from pathlib import Path


current_dir = Path(__file__).parent
STATE_FILE = current_dir.parent.parent / 'Data_Collection' / 'telegram-scraper' / 'state.json'
session_database = current_dir.parent.parent / 'Data_Collection' / 'telegram-scraper' / 'session.session'


def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        'api_id': None,
        'api_hash': None,
        'phone': None,
        'channels': {},
        'scrape_media': True,
    }


state = load_state()
client = TelegramClient(session_database, state['api_id'], state['api_hash'])


async def scrape_channel(client, channel, offset_id, df, state):
    try:
        if channel.startswith('-'):
            entity = await client.get_entity(PeerChannel(int(channel)))
        else:
            entity = await client.get_entity(channel)

        total_messages = 0

        async for message in client.iter_messages(entity, offset_id=offset_id, reverse=True):
            total_messages += 1

        if total_messages == 0:
            print(f"No messages found in channel {channel}.")
            return df

        processed_messages = 0

        async for message in client.iter_messages(entity, offset_id=offset_id, reverse=True):
            try:
                new_row = pd.DataFrame({'date': [message.date.strftime('%Y-%m-%d %H:%M:%S')], 'message': [message.text if message.text else ""]})

                df = pd.concat([df, new_row], ignore_index=True)

                last_message_id = message.id
                processed_messages += 1

                progress = (processed_messages / total_messages) * 100
                sys.stdout.write(f"\rScraping channel: {channel} - Progress: {progress:.2f}%")
                sys.stdout.flush()

                state['channels'][channel] = last_message_id
                save_state(state)
            except Exception as e:
                print(f"Error processing message {message.id}: {e}")
        print()
    except ValueError as e:
        print(f"Error with channel {channel}: {e}")

    return df


async def main():
    try:
        await client.start()
        df = pd.DataFrame(columns=['date', 'message'])
        print("Hour scraping began")
        for channel in state['channels']:
            df = await scrape_channel(client,channel, state['channels'][channel], df, state)
        df.to_csv('hour_telegram_data.csv', index=False)
    finally:
        await client.disconnect()
        print("Hour scraping ended")


if __name__ == '__main__':
    asyncio.run(main())
