import json
import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand

from dotenv import load_dotenv

load_dotenv()
if os.name == 'nt':
    data_directory = 'json\\'
else:
    data_directory = 'json/'


class Mybot(commands.Bot):
    def __init__(self, command_prefix, **options):
        self.command_prefix = command_prefix
        prefix = commands.when_mentioned_or(command_prefix)
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)  # 個人のメンションのみ反応
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=prefix,
            intents=intents,
            allowed_mentions=allowed_mentions,
            **options
        )
        self.remove_command('help')
        self.data_directory = data_directory
        with open(f'{self.data_directory}guild_open.json') as f:
            self.guild_open = json.load(f)
        with open(f'{self.data_directory}embed_type.json') as f:
            self.emnbed_type = json.load(f)
        self.slash_client = SlashCommand(self, sync_commands=True)
        self.log_ch_id = 830359131713175572

    async def on_ready(self):
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    self.reload_extension(f"cogs.{cog[:-3]}")
                except discord.ext.commands.errors.ExtensionFailed:
                    continue
        print('ready')
        await self.change_presence(activity=discord.Game(name=f"/help | {len(self.guilds)}guilds"))

    async def on_guild_join(self, _):
        await self.change_presence(activity=discord.Game(name=f"/help | {len(self.guilds)}guilds"))

    async def on_guild_remove(self, _):
        await self.change_presence(activity=discord.Game(name=f"/help | {len(self.guilds)}guilds"))


if __name__ == '__main__':
    bot = Mybot(command_prefix="e:")
    bot.run(os.environ['TOKEN'])
