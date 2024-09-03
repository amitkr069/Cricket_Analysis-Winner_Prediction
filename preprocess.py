import pandas as pd

def preprocessor_test_batting(test_batting_df):
    test_batting_df["fielders"] = test_batting_df["fielders"].fillna("-")
    test_batting_df['fielders'] = test_batting_df['fielders'].replace("['-']", '-')
    test_batting_df["bowler"] = test_batting_df["bowler"].fillna("-")

    return test_batting_df
def preprocessor_test_match(test_match_df):
    test_match_df.drop(["TEST Match No", "Match Format", "Umpire 1", "Umpire 2", "Match Referee", "Debut Players"],
                       axis=1, inplace=True)
    return test_match_df

def fow_pre(test_fow_df, match_id):
    new_fow_df = test_fow_df[test_fow_df["Match ID"] == match_id]
    new_fow_df = new_fow_df[["Match ID", "innings", "player", "wicket"]]
    new_fow_df.rename(columns={"player": "batsman"}, inplace=True)
    new_fow_df["batsman"] = new_fow_df["batsman"].astype('int64')
    return new_fow_df

def batting_pre(test_batting_df, new_fow_df,test_player_df, match_id):
    new_batting_df = test_batting_df[test_batting_df["Match ID"] == match_id]
    new_batting_df = new_batting_df.fillna("-")
    new_batting_df = new_batting_df.merge(new_fow_df, on=["Match ID", "innings", "batsman"], how="left")
    new_batting_df = new_batting_df[new_batting_df["wicketType"] != "DNB"]
    sorted_batting_df = new_batting_df.sort_values(by=['innings', 'wicket'], ascending=[True, True], na_position='last')
    test_player_df_new = test_player_df[["player_id", "player_name"]]
    test_player_df_new.rename(columns={"player_id": "batsman"}, inplace=True)
    sorted_batting_df = sorted_batting_df.merge(test_player_df_new, on=["batsman"], how="left")
    return sorted_batting_df

def bowler_pre(test_bowling_df, test_player_df, sorted_batting_df, match_id):
    new_bowling_df = test_bowling_df[test_bowling_df["Match ID"] == match_id]
    new_bowling_df['bowler id'] = new_bowling_df["bowler id"].astype('float64')
    test_player_df_new = test_player_df[["player_id", "player_name"]]
    test_player_df_new.rename(columns={"player_id": "bowler id"}, inplace=True)
    new_bowling_df = new_bowling_df.merge(test_player_df_new, on=["bowler id"], how="left")
    new_bowling_df_bat = new_bowling_df
    new_bowling_df_bat = new_bowling_df_bat[["bowler id", "player_name"]]
    new_bowling_df_bat.rename(columns={"bowler id": "bowler"}, inplace=True)
    sorted_batting_df["bowler"] = sorted_batting_df["bowler"].astype(str)
    new_bowling_df_bat["bowler"] = new_bowling_df_bat["bowler"].astype(str)
    sorted_batting_df = sorted_batting_df.merge(new_bowling_df_bat, on=["bowler"], how="left")
    sorted_batting_df.rename(columns={"player_name_x": "Batsman Name", "player_name_y": "Bowler Name"}, inplace=True)
    sorted_batting_df['Bowler Name'] = sorted_batting_df["Bowler Name"].fillna("-")
    sorted_batting_df = sorted_batting_df.drop_duplicates(subset=['Batsman Name','Bowler Name'])
    return sorted_batting_df

def main_bowling_pre(test_bowling_df, test_player_df,  match_id):
    new_bowling_df = test_bowling_df[test_bowling_df["Match ID"] == match_id]
    new_bowling_df['bowler id'] = new_bowling_df["bowler id"].astype('float64')
    test_player_df_new = test_player_df[["player_id", "player_name"]]
    test_player_df_new.rename(columns={"player_id": "bowler id", "player_name": "Bowler"}, inplace=True)
    new_bowling_df = new_bowling_df.merge(test_player_df_new, on=["bowler id"], how="left")
    new_bowling_df = new_bowling_df.fillna("No Data")
    return new_bowling_df

def partnership(match_id, test_partnership_df, test_player_df):
    test_player_df_partner = test_player_df[["player_id", "player_name"]]
    test_player_df_partner.rename(columns={"player_id": "player1", "player_name": "player1_name"}, inplace=True)
    test_partnership_df_new = test_partnership_df
    test_partnership_df_new = test_partnership_df_new[test_partnership_df_new["Match ID"] == match_id]
    test_partnership_df_new = test_partnership_df_new.merge(test_player_df_partner, on=["player1"], how="left")
    test_player_df_partner.rename(columns={"player1": "player2", "player1_name": "player2_name"}, inplace=True)
    test_partnership_df_new = test_partnership_df_new.merge(test_player_df_partner, on=["player2"], how="left")
    test_partnership_df_new = test_partnership_df_new[test_partnership_df_new["Match ID"] == match_id]
    return test_partnership_df_new

def fall_of_wickets(match_id, test_fow_df, test_player_df):
    test_player_fow_df = test_player_df[["player_id", "player_name"]]
    test_player_fow_df.rename(columns={"player_id": "player"}, inplace=True)
    test_player_fow_df["player"] = test_player_fow_df["player"].astype('float64')
    test_fow_df = test_fow_df[test_fow_df["Match ID"] == match_id]
    test_fow_df = test_fow_df.merge(test_player_fow_df, on=["player"], how="left")
    test_fow_df.rename(columns={"player_name":"Batsman"}, inplace=True)
    return test_fow_df

def match_score(test_player_df, test_match_df, match_id):
    test_player_result_df = test_player_df[["player_id", "player_name"]]
    test_player_result_df.rename(columns={"player_id": "MOM Player"}, inplace=True)
    test_player_result_df["MOM Player"] = test_player_result_df["MOM Player"].astype('float64')
    test_match_result_df = test_match_df

    test_match_result_df["MOM Player"] = test_match_result_df["MOM Player"].astype(str)
    test_player_result_df["MOM Player"] = test_player_result_df["MOM Player"].astype(str)

    test_match_result_df = test_match_result_df.merge(test_player_result_df, on=["MOM Player"], how="left")
    test_match_result_df = test_match_result_df[test_match_result_df["Match ID"] == match_id]
    test_match_result_df.rename(columns={"Innings1 Team1 Runs Scored": "Innings1 Runs Scored",
                                         "Innings1 Team1 Wickets Fell": "Innings1 Wickets Fell",
                                         "Innings2 Team1 Runs Scored": "Innings3 Runs Scored",
                                         "Innings2 Team1 Wickets Fell": "Innings3 Wickets Fell",
                                         "Innings1 Team2 Runs Scored": "Innings2 Runs Scored",
                                         "Innings1 Team2 Wickets Fell": "Innings2 Wickets Fell",
                                         "Innings2 Team2 Runs Scored": "Innings4 Runs Scored",
                                         "Innings2 Team2 Wickets Fell": "Innings4 Wickets Fell"}, inplace=True)
    return test_match_result_df


#odi
def preprocessor_odi_match(odi_match_df):
    odi_match_df = odi_match_df[odi_match_df["Series Name"] != "  -  ()"]
    odi_match_df.drop(["ODI Match No", "Match Format", "Umpire 1", "Umpire 2", "Match Referee", "Debut Players"],
                       axis=1, inplace=True)
    return odi_match_df


def preprocessor_odi_batting(odi_batting_df):
    odi_batting_df["bowler"] = odi_batting_df["bowler"].fillna("-")
    return odi_batting_df

def match_score_odi(test_player_df, test_match_df, match_id):
    test_player_result_df = test_player_df[["player_id", "player_name"]]
    test_player_result_df.rename(columns={"player_id": "MOM Player"}, inplace=True)
    test_player_result_df["MOM Player"] = test_player_result_df["MOM Player"].astype('float64')
    test_match_result_df = test_match_df

    test_match_result_df["MOM Player"] = test_match_result_df["MOM Player"].astype(str)
    test_player_result_df["MOM Player"] = test_player_result_df["MOM Player"].astype(str)

    test_match_result_df = test_match_result_df.merge(test_player_result_df, on=["MOM Player"], how="left")
    test_match_result_df = test_match_result_df[test_match_result_df["Match ID"] == match_id]
    test_match_result_df.rename(columns={"Team1 Runs Scored": "Innings1 Runs Scored",
                                         "Team1 Wickets Fell": "Innings1 Wickets Fell",
                                         "Team2 Runs Scored": "Innings2 Runs Scored",
                                         "Team2 Wickets Fell": "Innings2 Wickets Fell",
                                         }, inplace=True)
    return test_match_result_df


#T20
def preprocessor_t20_match(t20_match_df):
    t20_match_df = t20_match_df.fillna("-")
    t20_match_df.drop(["T20I Match No", "Match Format", "Umpire 1", "Umpire 2", "Match Referee", "Debut Players"],
                       axis=1, inplace=True)
    return t20_match_df

def player_info(test_player_df, test_batting_df, specific_player, i):
    test_player_stats_df = test_player_df[["player_id", "player_name"]]
    test_player_stats_df.rename(columns={"player_id": "batsman"}, inplace=True)
    test_batting_stats_df = test_batting_df
    test_batting_stats_df = test_batting_stats_df.merge(test_player_stats_df, on=["batsman"], how="left")
    specific_player_df = test_batting_stats_df[test_batting_stats_df["player_name"] == specific_player]

    matches_played = specific_player_df.drop_duplicates(subset=['Match ID']).reset_index(drop=True).shape[0]

    specific_player_df = specific_player_df[specific_player_df["wicketType"] != "DNB"]
    specific_player_df["runs"] = specific_player_df["runs"].astype('int64')
    # if not specific_player_df[specific_player_df["fours"] == "-"].empty:
    #     specific_player_df.loc[specific_player_df["fours"] == "-", "fours"] = 0.0
    # specific_player_df["fours"] = specific_player_df["fours"].astype('int64')
    # if not specific_player_df[specific_player_df["sixes"] == "-"].empty:
    #     specific_player_df.loc[specific_player_df["sixes"] == "-", "sixes"] = 0.0
    # specific_player_df["sixes"] = specific_player_df["sixes"].astype('int64')

    specific_player_df["fours"] = specific_player_df["fours"].replace("-", 0).fillna(0).astype('int64')
    specific_player_df["sixes"] = specific_player_df["sixes"].replace("-", 0).fillna(0).astype('int64')

    specific_player_runs = specific_player_df["runs"].sum()

    specific_player_fours = specific_player_df["fours"].sum()

    specific_player_sixes = specific_player_df["sixes"].sum()

    innings_played = specific_player_df.shape[0]

    specific_player_df_notout = specific_player_df[specific_player_df["wicketType"] != "not out"]

    player_average = round(specific_player_runs / specific_player_df_notout.shape[0], 2)

    centuries = specific_player_df[specific_player_df["runs"] >= 100].shape[0]

    double_centuries = specific_player_df[specific_player_df["runs"] >= 200].shape[0]

    half_centuries = specific_player_df[(specific_player_df["runs"] >= 50) & (specific_player_df["runs"] < 100)].shape[0]

    highest_runs = specific_player_df["runs"].max()

    not_out = specific_player_df[specific_player_df["wicketType"] == "not out"].shape[0]

    strike_rate = round(specific_player_df["strikeRate"].sum() / specific_player_df.shape[0],2)

    data = {'Matches': [matches_played],
            'Innings': [innings_played],
            'Not Out': [not_out],
            'Runs':[specific_player_runs],
            'Highest':[highest_runs],
            'Average':[player_average],
            'Strike Rate':[strike_rate],
            '100':[centuries],
            '200':[double_centuries],
            '50':[half_centuries],
            '4s':[specific_player_fours],
            '6s':[specific_player_sixes]
            }

    # Create DataFrame
    df = pd.DataFrame(data, index = [i])

    return df


def player_bowl_info(test_player_df, test_bowling_df, specific_player, i):
    test_player_stats_df = test_player_df[["player_id", "player_name"]]
    test_player_stats_df.rename(columns={"player_id": "bowler id"}, inplace=True)
    test_bowling_stats_df = test_bowling_df
    test_bowling_stats_df = test_bowling_stats_df.merge(test_player_stats_df, on=["bowler id"], how="left")
    specific_player_bowl_df = test_bowling_stats_df[test_bowling_stats_df["player_name"] == specific_player]

    matches = specific_player_bowl_df.drop_duplicates(subset=['Match ID']).reset_index(drop=True).shape[0]

    innings = specific_player_bowl_df.drop_duplicates(subset=['innings', 'Match ID']).reset_index(drop=True).shape[0]

    total_wickets = specific_player_bowl_df["wickets"].sum()

    total_balls = specific_player_bowl_df["balls"].sum()

    total_runs = specific_player_bowl_df["conceded"].sum()

    best_bowling_inmatch_df = specific_player_bowl_df.groupby("Match ID").sum([['wickets']]).sort_values(
        ['wickets', 'conceded'], ascending=(False, True)).reset_index()

    # BBM_run = best_bowling_inmatch_df.iloc[0]['conceded']
    # BBM_wic = best_bowling_inmatch_df.iloc[0]['wickets']
    if not best_bowling_inmatch_df.empty:
        BBM_run = round(best_bowling_inmatch_df.iloc[0]['conceded'])
        BBM_wic = round(best_bowling_inmatch_df.iloc[0]['wickets'])
    else:
        BBM_run = 0
        BBM_wic = 0



    best_bowling_innings_df = specific_player_bowl_df.groupby(["Match ID", "innings"]).sum([['wickets']]).sort_values(
        ['wickets', 'conceded'], ascending=(False, True)).reset_index()
    # BBI_run = best_bowling_innings_df.iloc[0]['conceded']
    # BBI_wic = best_bowling_innings_df.iloc[0]['wickets']

    if not best_bowling_innings_df.empty:
        BBI_run = round(best_bowling_innings_df.iloc[0]['conceded'])
        BBI_wic = round(best_bowling_innings_df.iloc[0]['wickets'])
    else:
        BBI_run = 0
        BBI_wic = 0

    bowling_average = round(total_runs / total_wickets, 2) if total_wickets > 0 else 0

    overs = total_balls / 6
    economy = round(total_runs / overs, 2)

    strike_rate = round(total_balls / total_wickets, 2) if total_wickets > 0 else 0

    four_wickets = specific_player_bowl_df[specific_player_bowl_df["wickets"] == 4].shape[0]

    fifer = specific_player_bowl_df[
        (specific_player_bowl_df["wickets"] >= 5) & (specific_player_bowl_df["wickets"] < 10)].shape[0]

    ten_wickets = best_bowling_inmatch_df[best_bowling_inmatch_df["wickets"] >= 10].shape[0]

    data = {
        'Matches':[matches],
        'Innings':[innings],
        'Balls': [total_balls],
        'Runs': [total_runs],
        'Wickets': [total_wickets],
        'BBI': [str(BBI_wic)+"/"+str(BBI_run)],
        'BBM': [str(BBM_wic)+"/"+str(BBM_run)],
        'Average' : [bowling_average],
        'Economy':[economy],
        'Strike Rate':[strike_rate],
        '4W': [four_wickets],
        '5W': [fifer],
        '10W': [ten_wickets]
    }

    df = pd.DataFrame(data, index=[i])

    return df

def player_chart(test_player_df, test_batting_df,test_match_df, selected_player):
    test_batting_stats_df = test_batting_df
    test_player_stats_df = test_player_df[["player_id", "player_name"]]
    test_player_stats_df.rename(columns={"player_id": "batsman"}, inplace=True)
    test_batting_stats_df = test_batting_stats_df.merge(test_player_stats_df, on=["batsman"], how="left")
    specific_player_df = test_batting_stats_df[test_batting_stats_df["player_name"] == selected_player]
    # test_match_df["Match Start Date"] = pd.to_datetime(test_match_df["Match Start Date"])

    test_match_df["Match Start Date"] = pd.to_datetime(test_match_df["Match Start Date"], errors='coerce',
                                                       dayfirst=True)
    # Drop rows with NaT in "Match Start Date"
    test_match_df = test_match_df.dropna(subset=["Match Start Date"])

    test_match_df['year'] = test_match_df['Match Start Date'].dt.year
    test_match_charts_df = test_match_df[["Match ID", "year"]]
    specific_player_df = specific_player_df.merge(test_match_charts_df, on=["Match ID"], how="left")
    grouped_df = specific_player_df.groupby('year').agg({
        'Match ID': 'count',
        'runs': 'sum',
        'strikeRate': 'mean',
        'fours': 'sum',
        'sixes': 'sum'
    }).reset_index()
    grouped_df['Average'] = grouped_df['runs'] / grouped_df['Match ID']

    specific_player_df_country = specific_player_df.merge(test_match_df[["Match ID", "Team1 Name", "Team2 Name"]],
                                                          on=["Match ID"], how="left")

    def determine_opposition(row):
        if row['team'] == row['Team1 Name']:
            return row['Team2 Name']
        elif row['team'] == row['Team2 Name']:
            return row['Team1 Name']
        else:
            return None

    specific_player_df_country['opposition'] = specific_player_df_country.apply(determine_opposition, axis=1)
    specific_player_df_country = specific_player_df_country.drop(columns=['Team1 Name', 'Team2 Name'])

    grouped_bat_country = specific_player_df_country.groupby('opposition').agg({
        'Match ID': 'count',
        'runs': 'sum',
        'strikeRate': 'mean',
        'fours': 'sum',
        'sixes': 'sum'
    }).reset_index()

    grouped_bat_country['Average'] = grouped_bat_country['runs'] / grouped_bat_country['Match ID']
    grouped_bat_country.rename(columns={'opposition':'Country',"Match ID":"Matches"}, inplace=True)
    return grouped_df, grouped_bat_country

def player_chart_odi(test_player_df, test_batting_df,test_match_df, selected_player):
    # test ke jgh odi ya t20 hoga
    test_batting_stats_df = test_batting_df
    test_player_stats_df = test_player_df[["player_id", "player_name"]]
    test_player_stats_df.rename(columns={"player_id": "batsman"}, inplace=True)
    test_batting_stats_df = test_batting_stats_df.merge(test_player_stats_df, on=["batsman"], how="left")
    specific_player_df = test_batting_stats_df[test_batting_stats_df["player_name"] == selected_player]
    # test_match_df["Match Date"] = pd.to_datetime(test_match_df["Match Date"])

    test_match_df["Match Date"] = pd.to_datetime(test_match_df["Match Date"], errors='coerce',
                                                       dayfirst=True)
    # Drop rows with NaT in "Match Start Date"
    test_match_df = test_match_df.dropna(subset=["Match Date"])

    test_match_df['year'] = test_match_df['Match Date'].dt.year
    test_match_charts_df = test_match_df[["Match ID", "year"]]
    specific_player_df = specific_player_df.merge(test_match_charts_df, on=["Match ID"], how="left")
    grouped_df_odi = specific_player_df.groupby('year').agg({
        'Match ID': 'count',
        'runs': 'sum',
        'strikeRate': 'mean',
        'fours': 'sum',
        'sixes': 'sum'
    }).reset_index()
    grouped_df_odi['Average'] = grouped_df_odi['runs'] / grouped_df_odi['Match ID']

    specific_player_df_country = specific_player_df.merge(test_match_df[["Match ID", "Team1 Name", "Team2 Name"]],
                                                          on=["Match ID"], how="left")

    def determine_opposition(row):
        if row['team'] == row['Team1 Name']:
            return row['Team2 Name']
        elif row['team'] == row['Team2 Name']:
            return row['Team1 Name']
        else:
            return None

    specific_player_df_country['opposition'] = specific_player_df_country.apply(determine_opposition, axis=1)
    specific_player_df_country = specific_player_df_country.drop(columns=['Team1 Name', 'Team2 Name'])

    grouped_bat_country = specific_player_df_country.groupby('opposition').agg({
        'Match ID': 'count',
        'runs': 'sum',
        'strikeRate': 'mean',
        'fours': 'sum',
        'sixes': 'sum'
    }).reset_index()

    grouped_bat_country['Average'] = grouped_bat_country['runs'] / grouped_bat_country['Match ID']
    grouped_bat_country.rename(columns={'opposition':'Country',"Match ID":"Matches"}, inplace=True)

    return grouped_df_odi, grouped_bat_country



#bowling charts
def player_chart_bowl(test_player_df, test_bowling_df,test_match_df, selected_player):
    test_bowling_stats_df = test_bowling_df
    test_player_stats_df = test_player_df[["player_id", "player_name"]]
    test_player_stats_df.rename(columns={"player_id": "bowler id"}, inplace=True)
    test_bowling_stats_df = test_bowling_stats_df.merge(test_player_stats_df, on=["bowler id"], how="left")
    specific_player_df = test_bowling_stats_df[test_bowling_stats_df["player_name"] == selected_player]
    # test_match_df["Match Start Date"] = pd.to_datetime(test_match_df["Match Start Date"])

    test_match_df["Match Start Date"] = pd.to_datetime(test_match_df["Match Start Date"], errors='coerce',
                                                       dayfirst=True)
    # Drop rows with NaT in "Match Start Date"
    test_match_df = test_match_df.dropna(subset=["Match Start Date"])

    test_match_df['year'] = test_match_df['Match Start Date'].dt.year
    test_match_charts_df = test_match_df[["Match ID", "year"]]
    specific_player_df = specific_player_df.merge(test_match_charts_df, on=["Match ID"], how="left")
    grouped_bowl = specific_player_df.groupby('year').agg({
        'Match ID': 'count',
        'conceded': 'sum',
        'economy': 'mean',
        'wickets': 'sum',
        'balls': 'sum'
    }).reset_index()
    grouped_bowl['Average'] = grouped_bowl['conceded'] / grouped_bowl['wickets']
    grouped_bowl['StrikeRate'] = grouped_bowl['balls'] / grouped_bowl['wickets']
    grouped_bowl.rename(columns={'conceded':'Runs conceded', "Match ID":"Matches"}, inplace=True)


    grouped_bowl_country = specific_player_df.groupby('opposition').agg({
        'Match ID': 'count',
        'conceded': 'sum',
        'economy': 'mean',
        'wickets': 'sum',
        'balls': 'sum'
    }).reset_index()

    grouped_bowl_country['Average'] = grouped_bowl_country['conceded'] / grouped_bowl_country['wickets']
    grouped_bowl_country['StrikeRate'] = grouped_bowl_country['balls'] / grouped_bowl_country['wickets']
    grouped_bowl_country.rename(columns={'opposition':'Country',"Match ID":"Matches", 'conceded':'Runs conceded'}, inplace=True)

    return grouped_bowl, grouped_bowl_country


def player_chart_bowl_odi(test_player_df, test_bowling_df,test_match_df, selected_player):
    test_bowling_stats_df = test_bowling_df
    test_player_stats_df = test_player_df[["player_id", "player_name"]]
    test_player_stats_df.rename(columns={"player_id": "bowler id"}, inplace=True)
    test_bowling_stats_df = test_bowling_stats_df.merge(test_player_stats_df, on=["bowler id"], how="left")
    specific_player_df = test_bowling_stats_df[test_bowling_stats_df["player_name"] == selected_player]
    # test_match_df["Match Start Date"] = pd.to_datetime(test_match_df["Match Start Date"])

    test_match_df["Match Date"] = pd.to_datetime(test_match_df["Match Date"], errors='coerce',
                                                       dayfirst=True)
    # Drop rows with NaT in "Match Start Date"
    test_match_df = test_match_df.dropna(subset=["Match Date"])

    test_match_df['year'] = test_match_df['Match Date'].dt.year
    test_match_charts_df = test_match_df[["Match ID", "year"]]
    specific_player_df = specific_player_df.merge(test_match_charts_df, on=["Match ID"], how="left")
    grouped_bowl = specific_player_df.groupby('year').agg({
        'Match ID': 'count',
        'conceded': 'sum',
        'economy': 'mean',
        'wickets': 'sum',
        'balls': 'sum'
    }).reset_index()
    grouped_bowl['Average'] = grouped_bowl['conceded'] / grouped_bowl['wickets']
    grouped_bowl['StrikeRate'] = grouped_bowl['balls'] / grouped_bowl['wickets']
    grouped_bowl.rename(columns={'conceded':'Runs conceded', "Match ID":"Matches"}, inplace=True)


    grouped_bowl_country = specific_player_df.groupby('opposition').agg({
        'Match ID': 'count',
        'conceded': 'sum',
        'economy': 'mean',
        'wickets': 'sum',
        'balls': 'sum'
    }).reset_index()

    grouped_bowl_country['Average'] = grouped_bowl_country['conceded'] / grouped_bowl_country['wickets']
    grouped_bowl_country['StrikeRate'] = grouped_bowl_country['balls'] / grouped_bowl_country['wickets']
    grouped_bowl_country.rename(columns={'opposition':'Country',"Match ID":"Matches", 'conceded':'Runs conceded'}, inplace=True)

    return grouped_bowl, grouped_bowl_country
