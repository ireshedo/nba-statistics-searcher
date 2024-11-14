from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import sys
def main():
    if len(sys.argv) == 2:
        nba_season = sys.argv[1]
        yr1, yr2 = nba_season.split("-")
        yr1_last2 = yr1[-2:]
        yr1 = int(yr1)
        yr2 = int(yr2)
        yr1_last2 = int(yr1_last2)
        yr1_last2 = yr1_last2 + 1
        while True:
            if 1949 <= yr1 <= 2024 and yr1_last2 == yr2:
                break
            else:
                sys.exit("Please insert current or past NBA season in correct format (xxxx-xx)")

    if len(sys.argv) == 1:
        nba_season = str("2024-25")
    print(f"""
        Please enter player name then type 'stats' for season stats,
        
        'career' for career stats,
        
        or for single-stat averages, ensure the following stat options below are typed after entering the players name.
        PTS, REB, AST, STL, GP, BLK, MIN, GP, GS, FGM, FGA, FTA, FT_PCT, OREB, DREB, TOV, PF
        
        for post-season statistics, type 'playoff' in between the players name and the stat mode you are looking for
        
        Example for regular season stats: Lebron James stats
        Example for post-season stats: Lebron James playoff stats
        
        The Default season is set to the {nba_season} NBA Season.
        If you want to change the season then type CTRL + C and enter the season in xxxx-xx format in the command line prompt.
        Example: python project.py 1996-97
        
        Enjoy the NBA Statistic Searcher!""")

    while True:
        try:
            player_name = input("NBA stats prompt: ")
            player_name = player_name.upper()
        except KeyboardInterrupt:
            print("\n")
            sys.exit("Program terminated.")
        try:
            mode_type = mode_finder(player_name)
        except ValueError:
            continue
        if mode_type == '1':
            stat_str = stat_mode(player_name, nba_season)
            if stat_str == 1:
                continue
            else:
                print(stat_str)
                break
        if mode_type == '2':
            stat_str = full_stats_mode(player_name, nba_season)
            if stat_str == 1:
                continue
            else:
                print(stat_str)
                break
        if mode_type == '3':
            stat_str = career_mode(player_name)
            if stat_str == 1:
                continue
            else:
                print(stat_str)
                break


def mode_finder(p):
    stat_types = ('PTS', 'REB', 'AST', 'STL', 'GP', 'BLK', 'MIN', 'GP', 'GS', 'FGM', 'FGA', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'TOV', 'PF')
    if p.endswith(stat_types):
        return str("1")
    if p.endswith('STATS'):
        return str("2")
    if p.endswith('CAREER'):
        return str('3')
    else:
        print("Player could not be found.\n"
            "For single-stat averages, ensure the following stat options below are typed after entering the players name.\n"
            "PTS, REB, AST, STL, GP, BLK, MIN, GP, GS, FGM, FGA, FTA, FT_PCT, OREB, DREB, TOV, PF")
        raise ValueError

def stat_mode(s,y):
    plyf_str = 0
    stat_type = s.split()[-1]
    s1 = s.replace('PLAYOFFS', '')
    s2 = s1.replace('PLAYOFF', '')
    player_name = s2.rsplit(' ', 1)[0]
    player_name = player_name.strip()
    player_id_is = players.find_players_by_full_name(player_name)
    if  0 < len(player_id_is) <= 2:
        player_id_is = players.find_players_by_full_name(player_name)[0]["id"]
    else:
        print("Player could not be found. Try to make sure spelling is correct for the player(s)")
        return 1
    if 'PLAYOFF' in s or 'PLAYOFFS' in s:
        career = playercareerstats.PlayerCareerStats(player_id=player_id_is, per_mode36='PerGame')
        p_career = career.season_totals_post_season
        p_career = p_career.get_data_frame()
        plyf_str = 1
    else:
        career = playercareerstats.PlayerCareerStats(player_id=player_id_is, per_mode36='PerGame')
        p_career = career.get_data_frames()[0]

    col = p_career[stat_type]
    yr_col = p_career['SEASON_ID']
    for i in yr_col:
        if i == y:
            indx = p_career[p_career['SEASON_ID']== i].index.values
            break
    try:
        if len(indx) >= 2:
            indx = list(indx)
            indx = str(indx.pop())
        else:
            indx = list(indx)
            indx = str(indx.pop())
    except UnboundLocalError:
        print(f"Player could not be found. Ensure the player was active in the selected season. \n"
              f"Selected Season: {y} \n"
              "If you want to select a season, end the program with Ctrl-C then type the season in the command-line argument in xxxx-xx format (ex: 2022-23)")
        return 1
    indx = int(indx)
    stat_avg = col[indx]
    non_avg_stats = ('GP', 'GS', 'FT_PCT')
    for stat in non_avg_stats:
        if stat == stat_type:
            if stat_type == 'FT_PCT':
                stat_avg = stat_avg * 100
                if plyf_str == 1:
                    return str(f"{player_name} shot {stat_avg}% from the line in the {y} NBA Playoffs.")
                if plyf_str == 0:
                    return str(f"{player_name} shot {stat_avg}% from the line in the {y} NBA Regular Season.")
            if stat_type == 'GP':
                if plyf_str == 1:
                    return str(f"{player_name} played in {stat_avg} games in the {y} NBA Playoffs.")
                if plyf_str == 0:
                    return str(f"{player_name} played in {stat_avg} games in the {y} NBA Regular Season.")
            if stat_type == 'GS':
                if plyf_str == 1:
                    return str(f"{player_name} started in {stat_avg} games in the {y} NBA Playoffs.")
                if plyf_str == 0:
                    return str(f"{player_name} started in {stat_avg} games in the {y} NBA Regular Season.")
    if plyf_str == 1:
        return str(f"{player_name} averaged {stat_avg} {stat_type} per game in the {y} NBA Playoffs.")
    if plyf_str == 0:
        return str(f"{player_name} averaged {stat_avg} {stat_type} per game in the {y} NBA Regular Season.")




def full_stats_mode(s,y):
    plyf_str = 0
    s1 = s.replace('PLAYOFFS', '')
    s2 = s1.replace('PLAYOFF', '')
    player_name = s2.rsplit(' ', 1)[0]
    player_name = player_name.strip()
    player_id_is = players.find_players_by_full_name(player_name)
    if  0 < len(player_id_is) <= 2:
        player_id_is = players.find_players_by_full_name(player_name)[0]["id"]
    else:
        print("Player could not be found. Try to make sure spelling is correct for the player(s)")
        return 1
    if 'PLAYOFF' in s or 'PLAYOFFS' in s:
        career = playercareerstats.PlayerCareerStats(player_id=player_id_is, per_mode36='PerGame')
        p_career = career.season_totals_post_season
        p_career = p_career.get_data_frame()
        plyf_str = 1
    else:
        career = playercareerstats.PlayerCareerStats(player_id=player_id_is, per_mode36='PerGame')
        p_career = career.get_data_frames()[0]

    yr_col = p_career['SEASON_ID']
    for i in yr_col:
        if i == y:
            indx = p_career[p_career['SEASON_ID']== i].index.values
            break
    try:
        if len(indx) >= 2:
            indx = list(indx)
            indx = str(indx.pop())
        else:
            indx = list(indx)
            indx = str(indx.pop())
    except UnboundLocalError:
        print(f"Player could not be found. Ensure the player was active in the selected season. \n"
              f"Selected Season: {y} \n"
              "If you want to select a season, end the program with Ctrl-C then type the season in the command-line argument in xxxx-xx format (ex: 2022-23)")
        return 1
    pts = p_career['PTS']
    reb = p_career['REB']
    ast = p_career['AST']
    indx = int(indx)
    pts= pts[indx]
    reb= reb[indx]
    ast= ast[indx]
    if plyf_str == 1:
        return str(f"{player_name} averaged {pts} PTS, {reb} REBS, and {ast} ASTS in the {y} NBA Playoffs.")
    if plyf_str == 0:
        return str(f"{player_name} averaged {pts} PTS, {reb} REBS, and {ast} ASTS in the {y} NBA Regular Season.")


def career_mode(s):
    plyf_str = 0
    s1 = s.replace('PLAYOFFS', '')
    s2 = s1.replace('PLAYOFF', '')
    player_name = s2.rsplit(' ', 1)[0]
    player_name = player_name.strip()
    player_id_is = players.find_players_by_full_name(player_name)
    if  0 < len(player_id_is) <= 2:
        player_id_is = players.find_players_by_full_name(player_name)[0]["id"]
    else:
        print("Player could not be found. Try to make sure spelling is correct for the player(s)")
        return 1
    if 'PLAYOFF' in s or 'PLAYOFFS' in s:
        career = playercareerstats.PlayerCareerStats(player_id=player_id_is, per_mode36='PerGame')
        p_career1 = career.career_totals_post_season
        career_data = p_career1.get_data_frame()
        plyf_str = 1
    else:
        career = playercareerstats.PlayerCareerStats(player_id=player_id_is, per_mode36='PerGame')
        p_career1 = career.career_totals_regular_season
        career_data = p_career1.get_data_frame()
    pts = career_data['PTS']
    reb = career_data['REB']
    ast = career_data['AST']
    pts = pts[0]
    reb = reb[0]
    ast = ast[0]
    gp_col = career_data['GP']
    gp_total = gp_col[0]
    if plyf_str == 1:
        return str(f"{player_name} career averages in the playoffs are {pts} PTS, {reb} REBS, and {ast} ASTS in {gp_total} games.")
    else:
        return str(f"{player_name} career averages are {pts} PTS, {reb} REBS, and {ast} ASTS in {gp_total} games.")





if __name__ == "__main__":
    main()