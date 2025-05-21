import requests
from bs4 import BeautifulSoup
import random
import time

teams_dict = {
    'PHI': 'Philadelphia 76ers',
    'BOS': 'Boston Celtics',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'NYK': 'New York Knicks',
    'TOR': 'Toronto Raptors',
    'BRK': 'Brooklyn Nets',
    'ORL': 'Orlando Magic',
    'WAS': 'Washington Wizards',
    'IND': 'Indiana Pacers',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DET': 'Detroit Pistons',
    'ATL': 'Atlanta Hawks',
    'CHA': 'Charlotte Hornets',
    'NOP': 'New Orleans Pelicans',
    'DAL': 'Dallas Mavericks',
    'HOU': 'Houston Rockets',
    'SAS': 'San Antonio Spurs',
    'DEN': 'Denver Nuggets',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'PHO': 'Phoenix Suns',
    'SAC': 'Sacramento Kings',
    'POR': 'Portland Trail Blazers',
    'UTA': 'Utah Jazz',
    'OKC': 'Oklahoma City Thunder',
    'MIN': 'Minnesota Timberwolves',
    'GSW': 'Golden State Warriors',
    'MEM': 'Memphis Grizzlies',
}

active_players = []

for abbr, team in teams_dict.items():
    url = f'https://www.basketball-reference.com/teams/{abbr}/2025.html#all_roster'
    print(url)
    r = requests.get(url)
    time.sleep(random.uniform(10, 30))  # Sleep for a random time between 10 and 30 seconds to prevent rate limiting
    if r.status_code != 200:
        print(f'Error: {r.status_code}')
        continue
    soup = BeautifulSoup(r.text, 'html.parser')
    # Active players have a link to their player page
    players = soup.find_all('td', attrs={'data-stat': 'player'})
    for player in players:
        if player.find('a'):
            active_players.append(player.text.strip())
        

active_players = list(set(active_players))  # Remove duplicates
with open('active_players.csv', 'w') as f:
    for player in active_players:
        f.write(f'{player}\n')