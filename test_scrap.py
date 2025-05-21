import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import csv

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

# Read already processed players
processed_players = set()
with open('active_players.csv', 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        processed_players.add((row['player'], row['team']))

active_players = []

with open('active_players.csv', 'a', newline='') as csvfile:
    fieldnames = ['player', 'position', 'age', 'team', 'points_per_game', 'rebounds_per_game', 'assists_per_game']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    for abbr, team in teams_dict.items():
        player_info_url = f'https://www.basketball-reference.com/teams/{abbr}/2025.html#all_roster'
        print(player_info_url)
        player_info_r = requests.get(player_info_url)
        # time.sleep(random.uniform(10, 30))

        soup = BeautifulSoup(player_info_r.text, 'html.parser')
        players = soup.find_all('td', attrs={'data-stat': 'player'})
        for player in players:
            a_tag = player.find('a')
            if a_tag:
                if (player.text.strip(), team) in processed_players:
                    continue  # Skip already processed
                player_link = a_tag['href']
                print(player_link)
                row = player.parent
                pos_td = row.find('td', attrs={'data-stat': 'pos'})
                position = pos_td.text.strip() if pos_td else ''
                birth_td = row.find('td', attrs={'data-stat': 'birth_date'})
                birth_date = birth_td.text.strip() if birth_td else ''
                age = ''
                if birth_date:
                    for fmt in ('%Y-%m-%d', '%B %d, %Y'):
                        try:
                            bday = datetime.strptime(birth_date, fmt)
                            today = datetime.today()
                            age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
                            break
                        except ValueError:
                            continue
                player_stats_url = f'https://www.basketball-reference.com{player_link}'
                player_stats_r = requests.get(player_stats_url)
                soup = BeautifulSoup(player_stats_r.text, 'html.parser')
                def get_stat(span_tip):
                    span = soup.find('span', attrs={'data-tip': span_tip})
                    p = span.find_next('p') if span else None
                    return float(p.text.strip()) if p and p.text.strip() else 0.0

                points = get_stat('Points')
                rebounds = get_stat('Total Rebounds')
                assists = get_stat('Assists')
                
                player_dict = {
                    'player': player.text.strip(),
                    'position': position,
                    'age': age,
                    'team': teams_dict[abbr],
                    'points_per_game': float(points),
                    'rebounds_per_game': float(rebounds),
                    'assists_per_game': float(assists)
                }
                active_players.append(player_dict)
                writer.writerow(player_dict)
                csvfile.flush()
                time.sleep(random.uniform(10, 30))  # Sleep to prevent rate limiting