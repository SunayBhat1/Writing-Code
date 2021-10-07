from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

def getTeamData():
    teamDict = {'New Orleans Saints':'NO',
        'Arizona Cardinals':'ARI',
        'Baltimore Ravens': 'BAL',
        'Las Vegas Raiders':'LV',
        'Buffalo Bills':'BUF',
        'Carolina Panthers':'CAR',
        'New England Patriots':'NE',
        'Los Angeles Chargers':'LAC',
        'Philadelphia Eagles':'PHI',
        'Denver Broncos':'DEN',
        'Green Bay Packers':'GB',
        'Seattle Seahawks':'SEA',
        'Minnesota Vikings':'MIN',
        'Pittsburgh Steelers':'PIT',
        'Indianapolis Colts':'IND',
        'New York Jets':'NYJ',
        'Miami Dolphins':'MIA',
        'Houston Texans':'HOU',
        'Cleveland Browns':'CLE',
        'Cincinnati Bengals':'CIN',
        'Tennessee Titans':'TEN',
        'New York Giants':'NYG',
        'Washington':'WSH',
        'San Francisco 49ers':'SF',
        'Dallas Cowboys':'DAL',
        'Atlanta Falcons':'ATL',
        'Detroit Lions':'DET',
        'Jacksonville Jaguars':'JAX',
        'Tampa Bay Buccaneers':'TB',
        'Kansas City Chiefs':'KC',
        'Los Angeles Rams':'LAR',
        'Chicago Bears':'CHI'}

    teamData_offense = pd.DataFrame(columns=['GP','Total YDS','YPG','Passing YDS','Passing YPG','Rushing YDS','Rushing YPG','Total Points','PPG'], index = list(teamDict.values()))
    teamData_defense = pd.DataFrame(columns=['GP','Total YDS','YPG','Passing YDS','Passing YPG','Rushing YDS','Rushing YPG','Total Points','PPG'], index = list(teamDict.values()))

    url = 'https://www.espn.com/nfl/stats/team/_/view/defense/table'
    # Open URL and pass to BeautifulSoup
    html = urlopen(url)
    defense_page = BeautifulSoup(html,features='lxml')

    url = 'https://www.espn.com/nfl/stats/team/_/view/offense/table'
    # Open URL and pass to BeautifulSoup
    html = urlopen(url)
    offsense_page = BeautifulSoup(html,features='lxml')

        # Populate Team Data table from ESPN Web
    for i in range (2,34):
        team = teamDict[defense_page.findAll('tr')[i].findAll('td')[0].getText()]
        teamData_defense.at[team,'GP'] = int(defense_page.findAll('tr')[i+34].findAll('td')[0].getText())
        teamData_defense.at[team,'Total YDS'] = int(defense_page.findAll('tr')[i+34].findAll('td')[1].getText().replace(',', ''))
        teamData_defense.at[team,'YPG'] = float(defense_page.findAll('tr')[i+34].findAll('td')[2].getText().replace(',', ''))
        teamData_defense.at[team,'Passing YDS'] = int(defense_page.findAll('tr')[i+34].findAll('td')[3].getText().replace(',', ''))
        teamData_defense.at[team,'Passing YPG'] = float(defense_page.findAll('tr')[i+34].findAll('td')[4].getText().replace(',', ''))
        teamData_defense.at[team,'Rushing YDS'] = int(defense_page.findAll('tr')[i+34].findAll('td')[5].getText().replace(',', ''))
        teamData_defense.at[team,'Rushing YPG'] = float(defense_page.findAll('tr')[i+34].findAll('td')[6].getText().replace(',', ''))
        teamData_defense.at[team,'Total Points'] = int(defense_page.findAll('tr')[i+34].findAll('td')[7].getText().replace(',', ''))
        teamData_defense.at[team,'PPG'] = float(defense_page.findAll('tr')[i+34].findAll('td')[8].getText().replace(',', ''))

        team = teamDict[offsense_page.findAll('tr')[i].findAll('td')[0].getText()]
        teamData_offense.at[team,'GP'] = int(offsense_page.findAll('tr')[i+34].findAll('td')[0].getText().replace(',', ''))
        teamData_offense.at[team,'Total YDS'] = int(offsense_page.findAll('tr')[i+34].findAll('td')[1].getText().replace(',', ''))
        teamData_offense.at[team,'YPG'] = float(offsense_page.findAll('tr')[i+34].findAll('td')[2].getText())
        teamData_offense.at[team,'Passing YDS'] = int(offsense_page.findAll('tr')[i+34].findAll('td')[3].getText().replace(',', ''))
        teamData_offense.at[team,'Passing YPG'] = float(offsense_page.findAll('tr')[i+34].findAll('td')[4].getText().replace(',', ''))
        teamData_offense.at[team,'Rushing YDS'] = int(offsense_page.findAll('tr')[i+34].findAll('td')[5].getText().replace(',', ''))
        teamData_offense.at[team,'Rushing YPG'] = float(offsense_page.findAll('tr')[i+34].findAll('td')[6].getText().replace(',', ''))
        teamData_offense.at[team,'Total Points'] = int(offsense_page.findAll('tr')[i+34].findAll('td')[7].getText().replace(',', ''))
        teamData_offense.at[team,'PPG'] = float(offsense_page.findAll('tr')[i+34].findAll('td')[8].getText().replace(',', ''))

    return teamData_defense,teamData_offense

def getPlayerData(myLeague,teamData_defense,teamData_offense):
    PRO_TEAM_MAP = {0 : 'None',1 : 'ATL',2 : 'BUF',3 : 'CHI',4 : 'CIN',5 : 'CLE',6 : 'DAL',7 : 'DEN',8 : 'DET',
        9 : 'GB',10: 'TEN',11: 'IND',12: 'KC',13: 'LV',14: 'LAR',15: 'MIA',16: 'MIN',17: 'NE',18: 'NO',19: 'NYG',
        20: 'NYJ',21: 'PHI',22: 'ARI',23: 'PIT',24: 'LAC',25: 'SF',26: 'SEA',27: 'TB',28: 'WSH',29: 'CAR',30: 'JAX',
        31: 'BAL',32: 'HOU',33: 'BAL',34: 'HOU'}

    playerData = {}
    playerData['QB'] = pd.DataFrame(columns=['Name','PlayerID','Week','Position Rank','Projected Points','Season Projected Points','Off YPG/OppDef YPG','Off PPG/OppDef PPG','Off PYPG/OppDef PYPG','Points'])
    playerData['RB'] = pd.DataFrame(columns=['Name','PlayerID','Week','Position Rank','Projected Points','Season Projected Points','Off YPG/OppDef YPG','Off PPG/OppDef PPG','Off RYPG/OppDef RYPG','Points'])
    playerData['WR'] = pd.DataFrame(columns=['Name','PlayerID','Week','Position Rank','Projected Points','Season Projected Points','Off YPG/OppDef YPG','Off PPG/OppDef PPG','Off PYPG/OppDef PYPG','Points'])
    playerData['TE'] = pd.DataFrame(columns=['Name','PlayerID','Week','Position Rank','Projected Points','Season Projected Points','Off YPG/OppDef YPG','Off PPG/OppDef PPG','Off PYPG/OppDef PYPG','Off RYPG/OppDef RYPG','Points'])
    playerData['D/ST'] = pd.DataFrame(columns=['Name','PlayerID','Week','Position Rank','Projected Points','Season Projected Points','Off YPG/OppDef YPG','Off PPG/OppDef PPG','Off PYPG/OppDef PYPG','Off RYPG/OppDef RYPG','Points'])
    playerData['K'] = pd.DataFrame(columns=['Name','PlayerID','Week','Position Rank','Projected Points','Season Projected Points','Off YPG/OppDef YPG','Off PPG/OppDef PPG','Points'])

    pro_schedule = myLeague._get_pro_schedule(myLeague.nfl_week)
    pro_schedule[31] = pro_schedule[33]
    pro_schedule[32] = pro_schedule[34]
    for team in myLeague.teams:
        for player in team.roster:

            if player.injured: continue

            playerDict = {}
            playerDict['Name'] = player.name
            playerDict['PlayerID'] = player.playerId
            playerDict['Week'] = myLeague.nfl_week
            playerDict['Position Rank'] = player.posRank
            playerDict['Season Projected Points'] = player.projected_total_points
            try: 
                playerDict['Projected Points'] = player.stats[myLeague.nfl_week]['projected_points']
                playerDict['Points'] = player.stats[myLeague.nfl_week-1]['points']
            except: 
                playerDict['Projected Points'] = float('NaN')
                playerDict['Points'] = float('NaN')
            

            if player.proTeam == 'OAK': player.proTeam = 'LV'
            player.pro_opponent = PRO_TEAM_MAP[pro_schedule[list(PRO_TEAM_MAP.values()).index(player.proTeam)][0]]
            try:
                playerDict['Off YPG/OppDef YPG'] = teamData_offense.at[player.proTeam,'YPG']/teamData_defense.at[player.pro_opponent,'YPG']
                playerDict['Off PPG/OppDef PPG'] = teamData_offense.at[player.proTeam,'PPG']/teamData_defense.at[player.pro_opponent,'PPG']
            except: print(player.proTeam)

            if player.position in ['QB','WR','TE','D/ST']: 
                playerDict['Off PYPG/OppDef PYPG'] = teamData_offense.at[player.proTeam,'Passing YPG']/teamData_defense.at[player.pro_opponent,'Passing YPG']
            if player.position in ['RB','TE','D/ST']:
                playerDict['Off RYPG/OppDef RYPG'] = teamData_offense.at[player.proTeam,'Rushing YPG']/teamData_defense.at[player.pro_opponent,'Rushing YPG']
            
            playerData[player.position] = playerData[player.position].append(playerDict, ignore_index = True)

    for player in myLeague.free_agents():

        if player.injured: continue

        playerDict = {}
        playerDict['Name'] = player.name
        playerDict['PlayerID'] = player.playerId
        playerDict['Week'] = myLeague.nfl_week
        playerDict['Position Rank'] = player.posRank
        playerDict['Season Projected Points'] = player.projected_total_points
        try: 
            playerDict['Projected Points'] = player.stats[myLeague.nfl_week]['projected_points']
            playerDict['Points'] = player.stats[myLeague.nfl_week-2]['points']
        except: 
            playerDict['Projected Points'] = float('NaN')
            playerDict['Points'] = float('NaN')

        if player.proTeam == 'OAK': player.proTeam = 'LV'
        player.pro_opponent = PRO_TEAM_MAP[pro_schedule[list(PRO_TEAM_MAP.values()).index(player.proTeam)][0]]
        playerDict['Off YPG/OppDef YPG'] = teamData_offense.at[player.proTeam,'YPG']/teamData_defense.at[player.pro_opponent,'YPG']
        playerDict['Off PPG/OppDef PPG'] = teamData_offense.at[player.proTeam,'PPG']/teamData_defense.at[player.pro_opponent,'PPG']
        if player.position in ['QB','WR','TE','D/ST']: 
            playerDict['Off PYPG/OppDef PYPG'] = teamData_offense.at[player.proTeam,'Passing YPG']/teamData_defense.at[player.pro_opponent,'Passing YPG']
        if player.position in ['RB','TE','D/ST']:
            playerDict['Off RYPG/OppDef RYPG'] = teamData_offense.at[player.proTeam,'Rushing YPG']/teamData_defense.at[player.pro_opponent,'Rushing YPG']
        
        playerData[player.position] = playerData[player.position].append(playerDict, ignore_index = True)

    return playerData
