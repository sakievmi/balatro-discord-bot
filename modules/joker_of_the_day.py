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

def get_embed(joker):
    embed = discord.Embed(
        title = f'{joker['Name']}',
        description = f'{joker['Effect']}',
        color = discord.Colour.dark_red()
    )
    embed.add_field(name="Price", value=f'{joker['Price']}', inline=True)
    embed.add_field(name="Rarity", value=f'{joker['Rarity']}', inline=True)
    embed.add_field(name="Unlock Requirement", value=f'{joker['Unlock_Requirement']}', inline=False)
    embed.set_image(url=joker['Picture'])

    return embed

async def send_all(bot):
    def get_mention_type(mention_type : int):
        if mention_type == 1:
            return '@everyone '
        elif mention_type == 2:
            return '@here '
        else:
            return ''

    embed = get_embed(
        jokers.jokers_list[get_id()]
    )

    for guild in database.data:
        if 'mention_type' not in database.data[guild]:
            database.data[guild]['mention_type'] = 3

        channel = bot.get_channel(database.data[guild]['jotd_channel_id'])
        await channel.send(f'{get_mention_type(database.data[guild]['mention_type'])}Joker of the day is...', embed=embed)

        database.save()

        print(f'Joker of the day is: {jokers.jokers_list[get_id()]['Name']}')

async def send_private(bot, ctx):
    embed = get_embed(
        jokers.jokers_list[get_id()]
    )

    await ctx.respond(f'Joker of the day is...', embed=embed, ephemeral=True)

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