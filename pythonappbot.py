import coc
import traceback
import json
import time
import discord

from riotwatcher import LolWatcher
from discord.ext import commands

with open("pythonappbot_food.txt") as f:
	auth = f.readlines()
auth = [x.strip() for x in auth]

coc_client = coc.login(auth[2], auth[3], key_count = 1, key_names = "discord_bot_key", client = coc.EventsClient,)
clan_tag = auth[4]

bot = commands.Bot(command_prefix="!")
CHANNEL_ID = int(auth[1])

@coc_client.event
async def on_clan_member_versus_trophies_change(old_trophies, new_trophies, player):
	await bot.get_channel(CHANNEL_ID).send(
		"{0.name}-nek jelenleg {1} versus trófeája van.".format(player, new_trophies))

@bot.command()
async def szia(ctx):
	await ctx.send("Szia!")

@bot.command()
async def hosok(ctx, player_tag):
	player = await coc_client.get_player(player_tag)
	to_send = ""
	for hero in player.heroes:
		to_send += "{}: level {}/{}\n".format(str(hero), hero.level, hero.max_level)
	await ctx.send(to_send)

@bot.command()
async def lollevel(ctx, playername):
	watcher = LolWatcher(auth[5])
	stats = watcher.summoner.by_name("EUN1", playername)
	json_str = json.dumps(stats)
	json_stripped = json.loads(json_str)
	to_print = "{}'s level: {}"
	await ctx.send(to_print.format(playername, json_stripped["summonerLevel"]))

coc_client.add_clan_update(
	[clan_tag], retry_interval=60
	)

coc_client.start_updates()

bot.run(auth[0])