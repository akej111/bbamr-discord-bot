# bot.py
import os
import random
import json

from pprint import pprint
from helpers import *
from discord.ext import commands
from dotenv import load_dotenv
from prettytable import PrettyTable


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
async def start_game(ctx, *args):
    print("Starting a new game")
    print(bot.db)
    if bot.game_live:
        await ctx.send("Game still live, cancel or give winner with !finish")

    players = list(args)
    for p in players:
        if p not in bot.db:
            await ctx.send("Player {} does not exist. Please add them.".format(p))

    random.shuffle(players)

    bot.teamA = players[:len(players)//2]
    bot.teamB = players[len(players)//2:]

    testA = players[:len(players)//2]
    testB = players[len(players)//2:]

    testspymaster_A = get_team_spymaster(bot.teamA, bot.db)
    testspymaster_B = get_team_spymaster(bot.teamB, bot.db)

    bot.spymaster_A = get_team_spymaster(bot.teamA, bot.db)
    bot.spymaster_B = get_team_spymaster(bot.teamB, bot.db)

    print(bot.teamA,  bot.teamB, bot.spymaster_A, bot.spymaster_B)
    print(testA,  testB, testspymaster_A, testspymaster_B)

    response = "Starting game\n----------------\nTeam A: {}\n\tSpymaster: {}\nTeam B: {}\n\tSpymaster: {}"
    response = response.format(', '.join(bot.teamA), bot.spymaster_A, ', '.join(bot.teamB), bot.spymaster_B)
    bot.game_live = True
    await ctx.send(response)

@bot.command(name='finish', help='End the current game of codenames, give winner "A" or "B" or "cancel"')
async def start_game(ctx, arg):
    if not bot.game_live:
        await ctx.send("No game live, nothing done")
    if arg == 'cancel':
        bot.game_live = False
        response = "Current game cancelled. Game details\n ----------------\n Team A: {}\n\tSpymaster: {}\nTeam B {}\n\tSpymaster: {}"
        response = response.format(', '.join(bot.teamA), bot.spymaster_A, ', '.join(bot.teamB), bot.spymaster_B)
        await ctx.send(response)
    else:
        if arg == 'A':
            finish_game(bot.teamA, bot.spymaster_A, bot.teamB, bot.spymaster_B, bot.db)
        else:
            finish_game(bot.teamB, bot.spymaster_B, bot.teamA, bot.spymaster_A, bot.db)
        with open('data.json', 'w') as outfile:
            json.dump(bot.db, outfile)
        bot.game_live = False
        response = "Congrats to Team {}, scores have been updated"
        response = response.format(arg)
        await ctx.send(response)

@bot.command(name='leaderboards', help='Show the leaderboards wp to sort by win percentage, wins to sort by number of wins')
async def leaderboards(ctx, arg):
    entries = get_all_players(bot.db)
    if arg == 'wp':
        entries =  sorted(entries, key = lambda i: (i[1]['wp'], i[1]['w']), reverse=True) 
    elif arg == 'wins':
        entries =  sorted(entries, key = lambda i: (i[1]['w'], i[1]['wp']), reverse=True) 
    else:
        await ctx.send("Argumemt does not exist, put 'wp' for win percentage or 'wins' for wins")
    response = PrettyTable(['Name', "Wins", "Loses", "Win %"])
    for entry in entries:
        response.add_row([entry[0], entry[1]['w'], entry[1]['l'], entry[1]['wp']])
    
    response = "```\n" + response + "```\n"
    await ctx.send(response)

bot.run(TOKEN)

