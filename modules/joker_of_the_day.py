import random
import discord
import asyncio
from datetime import datetime, timezone, timedelta
from modules import jokers, database

def get_id():
    random.seed(
        datetime.now(timezone.utc).year +
        datetime.now(timezone.utc).day +
        datetime.now(timezone.utc).month
    )
    random_num = random.randrange(0, len(jokers.jokers_list))
    return random_num

async def send_all(bot):
    joker_id = get_id()
    joker_element = jokers.jokers_list[joker_id]

    def get_mention_type(mention_type : int):
        if mention_type == 1:
            return '@everyone '
        elif mention_type == 2:
            return '@here '
        else:
            return ''

    embed = discord.Embed(
        title = f'{joker_element['Name']}',
        description = f'{joker_element['Effect']}',
        color = discord.Colour.dark_red()
    )
    embed.add_field(name="Price", value=f'{joker_element['Price']}', inline=True)
    embed.add_field(name="Rarity", value=f'{joker_element['Rarity']}', inline=True)
    embed.add_field(name="Unlock Requirement", value=f'{joker_element['Unlock_Requirement']}', inline=False)
    embed.set_image(url=joker_element['Picture'])

    for guild in database.data:
        if 'mention_type' not in database.data[guild]:
            database.data[guild]['mention_type'] = 3

        channel = bot.get_channel(database.data[guild]['jotd_channel_id'])
        await channel.send(f'{get_mention_type(database.data[guild]['mention_type'])}Joker of the day is...', embed=embed)

        database.save()

        print(f'Joker of the day is: {joker_element['Name']}')

async def loop(bot):
    while True:
        # hours = (datetime.now(timezone.utc) - timedelta(hours=11)).hour
        hours = datetime.now(timezone.utc).hour
        if hours == 0:
            await send_all(bot)

            print(f'{datetime.now(timezone.utc)} | ' +
                  f'Joker of the day is: {jokers.jokers_list[get_id()]['Name']}')
            await asyncio.sleep(120*60)
        else:
            print(f'{datetime.now(timezone.utc)} | ' +
                  "It's not 0:XX! " + f'Joker of the day is: {jokers.jokers_list[get_id()]['Name']}')
            await asyncio.sleep(60)