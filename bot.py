# bot.py
import os
import random
import json

from pprint import pprint as print
from helpers import *
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='^')
bot.db = load_players()

bot.teamA = []
bot.spymaster_A = ''
bot.teamB = []
bot.spymaster_B = ''
bot.game_live = False

@bot.command(name='start', help='Start a game of codenames, give players in space seperated list')
async def start_game(ctx, arg):
    print("Starting a new game")
    print(bot.db)
    if bot.game_live:
        await ctx.send("Game still live, cancel or give winner with !finish")

    players = arg.split(' ')
    for p in players:
        if p not in bot.db:
            await ctx.send("Player {} does not exist. Please add them.".format(p))

    random.shuffle(players)

    bot.teamA = players[:len(players)//2]
    bot.teamB = players[len(players)//2:]

    bot.spymaster_A = get_team_spymaster(bot.teamA, bot.db)
    bot.spymaster_B = get_team_spymaster(bot.teamB, bot.db)


    response = "Starting game...\nTeam A: {} Spymaster: {}\n Team B: Spymaster: {}"
    response.format(', '.join(bot.teamA), bot.spymaster_A, ', '.join(bot.teamB), bot.spymaster_B)
    bot.game_live = True
    await ctx.send(response)

@bot.command(name='finish', help='End the current game of codenames, give winner "A" or "B" or "cancel"')
async def start_game(ctx, arg):
    if not bot.game_live:
        await ctx.send("No game live, nothing done")
    if arg == 'cancel':
        bot.game_live = False
        response = "Current game cancelled. Game details\n Team A: {} Spymaster: {}\n Team B: Spymaster: {}"
        response.format(', '.join(bot.teamA), bot.spymaster_A, ', '.join(bot.teamB), bot.spymaster_B)
        await ctx.send(response)
    else:
        if arg == A:
            finish_game(bot.teamA, bot.spymaster_A, bot.teamB, bot.teamB_spymaster, bot.db)
        else:
            finish_game(bot.teamB, bot.spymaster_B, bot.teamA, bot.teamA_spymaster, bot.db)
        with open('data.json', 'w') as outfile:
            json.dump(bot.db, outfile)
        bot.game_live = False
        response = "Congrats to Team {}, scores have been updated"
        response.format(arg)
        await ctx.send(response)

bot.run(TOKEN)

