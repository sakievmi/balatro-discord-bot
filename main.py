import discord
import os
import dotenv
from modules import joker_of_the_day, database

env = dotenv.load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

# Main function
def start_bot():
    @bot.event
    async def on_ready():
        print(f'{bot.user} is ready!')
        await joker_of_the_day.loop(bot)

    # noinspection PyTypeChecker
    @bot.command(description="Set up Joker Of The Day")
    async def jotd_setup(
        ctx,
        channel: discord.Option(discord.SlashCommandOptionType.channel)
    ):
        # CHECKING FOR GUILD OWNER !!!
        if ctx.author == ctx.guild.owner:
            try:
                guild_id = str(ctx.guild.id)
                if guild_id not in database.data:
                    database.data[guild_id] = {}
                database.data[guild_id]['jotd_channel_id'] = channel.id

                database.save()
            except NameError:
                await ctx.respond(f'Something went wrong! Send this to bot creator: {NameError}', ephemeral=True)
            finally:
                await ctx.respond(f'The Joker of the Day will now go to this channel: {channel.mention}', ephemeral=True)
        else:
            await ctx.respond("You're not the server owner!", ephemeral=True)

    @bot.command(description="Force Joker Of The Day message", ephemeral=True)
    async def force_jotd(
        ctx
    ):
        # CHECKING FOR BOT OWNER !!!
        if ctx.author.id == 821747325679698021:
            try:
                await joker_of_the_day.send_all(bot)
            except NameError:
                await ctx.respond(f'Something went wrong! Send this to bot creator: {NameError}', ephemeral=True)
            finally:
                await ctx.respond(f'Command executed!', ephemeral=True)
        else:
            await ctx.respond("You're not the bot owner!", ephemeral=True)

    # noinspection PyTypeChecker
    @bot.command(description="Mentions settings. Use numbers from 1-3 where 1 = everyone, 2 = here, 3 = do not ping anyone")
    async def jotd_mentions(
        ctx,
        mention_type: discord.Option(discord.SlashCommandOptionType.number, description='1 = everyone, 2 = here, 3 = do not ping anyone')
    ):
        # CHECKING FOR GUILD OWNER !!!
        if ctx.author == ctx.guild.owner:
            try:
                guild_id = str(ctx.guild.id)
                if guild_id not in database.data:
                    database.data[guild_id] = {}

                def set_mention_settings():
                    database.data[guild_id]['mention_type'] = mention_type

                    database.save()

                argument = int(mention_type)
                if argument > 3:
                    await ctx.respond(f'Wrong argument!', ephemeral=True)
                elif argument == 3:
                    set_mention_settings()
                    await ctx.respond(f'Jotd will not mention anyone', ephemeral=True)
                elif argument == 2:
                    set_mention_settings()
                    await ctx.respond(f'Jotd will mention everyone online', ephemeral=True)
                elif argument == 1:
                    set_mention_settings()
                    await ctx.respond(f'Jotd will mention everyone', ephemeral=True)
            except NameError:
                await ctx.respond(f'Something went wrong! Send this to bot creator: {NameError}', ephemeral=True)
        else:
            await ctx.respond("You're not the server owner!", ephemeral=True)

    bot.run(token)

if __name__ == '__main__':
    start_bot()