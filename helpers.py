import json

def load_players():
    with open('data.json') as f:
        return json.load(f)

def get_team_spymaster(team, db):
    current_spymaster = ""
    games_since = -1
    for player in team:
        if db[player]['spymaster'] > games_since:
            current_spymaster = player
            games_since = db[player]['spymaster']
    return current_spymaster

def finish_game(winner, winner_spy, loser, loser_spy, db):
    for player in winner:
        db[player]['w'] += 1
        if player == winner_spy:
            db[player]['spymaster'] = 0
        else:
            db[player]['spymaster'] += 1
        db[player]['wp'] = calc_win_percent(db[player]['w'], db[player]['l'])
    for player in loser:
        db[player]['l'] += 1
        if player == loser_spy:
            db[player]['spymaster'] = 0
        else:
            db[player]['spymaster'] += 1
        db[player]['wp'] = calc_win_percent(db[player]['w'], db[player]['l'])


def calc_win_percent(wins, loses):
    return round((wins / (wins + loses)), 3)

def get_all_players(db):
    player_list = []
    for key, pair in db.items():
        player_list.append((key, pair))
    return player_list
