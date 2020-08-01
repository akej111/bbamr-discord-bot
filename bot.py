# bot.py
import os
import random
import json


from helpers import *
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
db = load_players()

teamA = []
spymaster_A = ''
teamB = []
spymaster_B = ''
game_live = False


bot = commands.Bot(command_prefix='^')

@bot.command(name='start', help='Start a game of codenames, give players in space seperated list')
async def start_game(ctx, arg):
    if game_live:
        await ctx.send("Game still live, cancel or give winner with !finish")

    players = arg.split(' ')
    random.shuffle(players)

    teamA = players[:len(players)/2]
    teamB = players[len(players/2):]

    teamA_spymaster = get_team_spymaster(teamA, db)
    teamB_spymaster = get_team_spymaster(teamB, db)


    response = "Starting game...\nTeam A: {} Spymaster: {}\n Team B: Spymaster: {}"
    response.format(', '.join(teamA), teamA_spymaster, ', '.join(teamB), teamB_spymaster)
    game_live = True
    await ctx.send(response)

@bot.command(name='finish', help='End the current game of codenames, give winner "A" or "B" or "cancel"')
async def start_game(ctx, arg):
    if not game_live:
        await ctx.send("No game live, nothing done")
    if arg == 'cancel':
        game_live = False
        response = "Current game cancelled. Game details\n Team A: {} Spymaster: {}\n Team B: Spymaster: {}"
        response.format(', '.join(teamA), teamA_spymaster, ', '.join(teamB), teamB_spymaster)
        await ctx.send(response)
    else:
        if arg == A:
            finish_game(teamA, teamA_spymaster, teamB, teamB_spymaster, db)
        else:
            finish_game(teamB, teamB_spymaster, teamA, teamA_spymaster, db)
        with open('data.json', 'w') as outfile:
            json.dump(db, outfile)
        game_live = False
        response = "Congrats to Team {}, scores have been updated"
        response.format(arg)
        await ctx.send(response)

bot.run(TOKEN)

