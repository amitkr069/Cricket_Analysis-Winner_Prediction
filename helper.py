import pandas as pd
import streamlit as st
from datetime import datetime
import preprocess, helper2
import plotly.express as px


def series(test_match_df):
    series_test = test_match_df['Series Name'].unique().tolist()
    series_test.sort()
    series_test.insert(0, "Overall")
    return series_test
def selection(test_match_df, series):
    if (series == "Overall"):
        return test_match_df
    else:
        test_match_df = test_match_df[test_match_df["Series Name"] == series]
        return test_match_df

def selection1(select_match_df, selected_series):
    select_match_df = select_match_df[select_match_df["Series Name"] == selected_series]
    return select_match_df
def teams(test_match_df):
    team1_test = test_match_df['Team1 Name'].unique().tolist()
    team1_test.sort()

    team2_test = test_match_df['Team2 Name'].unique().tolist()
    team2_test.sort()
    return team1_test, team2_test
def matches(series_selected_match):
    matches = series_selected_match["Match Name"].unique().tolist()
    matches.sort()
    return matches
def select_match(series_selected_match, match):
    match_selected = series_selected_match[series_selected_match["Match Name"] == match]
    return match_selected

def select_match_overall(test_match_df, team1, team2):
  if (team1 == team2):
    return pd.DataFrame()
  else:
    test_match_df = test_match_df[((test_match_df['Team1 Name'] == team1) & (test_match_df['Team2 Name'] == team2)) | ((test_match_df['Team1 Name'] == team2) & (test_match_df['Team2 Name'] == team1))]
    if test_match_df.empty:
      return pd.DataFrame()
    else:
      return test_match_df


def results(specific_match, test_match_df, test_partnership_df, test_fow_df,test_bowling_df, test_player_df, test_batting_df):
    st.title("Series - "+specific_match.iloc[0]["Series Name"])
    st.title("Match - "+specific_match.iloc[0]["Match Name"])
    a = specific_match.iloc[0]["Match Start Date"] + "-" + specific_match.iloc[0]["Match End Date"]
    st.markdown("<h6>{}</h6>".format(a), unsafe_allow_html=True)
    match_id = specific_match.iloc[0][0]
    new_fow_df = preprocess.fow_pre(test_fow_df, match_id)
    sorted_batting_df = preprocess.batting_pre(test_batting_df, new_fow_df, test_player_df, match_id)
    sorted_batting_df = preprocess.bowler_pre(test_bowling_df, test_player_df, sorted_batting_df, match_id)
    new_bowling_df = preprocess.main_bowling_pre(test_bowling_df, test_player_df,  match_id)
    partnership_df = preprocess.partnership(match_id, test_partnership_df,test_player_df)
    fall_of_wickets_df = preprocess.fall_of_wickets(match_id,test_fow_df,test_player_df)
    innings = sorted_batting_df["innings"].unique()

    # for the score of each match and more
    test_match_result_df = preprocess.match_score(test_player_df, test_match_df, match_id)

    # venue
    venue = test_match_result_df.iloc[0]["Match Venue (Stadium)"]+ "," + test_match_result_df.iloc[0]["Match Venue (City)"] + "," + test_match_result_df.iloc[0]["Match Venue (Country)"]
    st.markdown("<h5>Venue-{}</h5>".format(venue), unsafe_allow_html=True)
    toss = test_match_result_df.iloc[0]["Toss Winner"] + " won the toss and Choose to " + test_match_result_df.iloc[0]["Toss Winner Choice"]
    st.markdown("<h4>{}</h4>".format(toss), unsafe_allow_html=True)


    for i in innings:
        globals()[f'inning_bat_{i}'] = sorted_batting_df[sorted_batting_df["innings"] == i]
        globals()[f'inning_bowl_{i}'] = new_bowling_df[new_bowling_df["innings"] == i]
        globals()[f'inning_partner_{i}'] = partnership_df[partnership_df["innings"] == i]
        globals()[f'inning_fow_{i}'] = fall_of_wickets_df[fall_of_wickets_df["innings"] == i]

    a = test_match_result_df.iloc[0]
    winner = a["Match Result Text"]
    st.markdown("<h3>Match result - {}</h3>".format(winner), unsafe_allow_html=True)
    mom = a["player_name"]
    st.markdown("<h3>Man of the Match - {}</h3>".format(mom), unsafe_allow_html=True)
    helper2.header(inning_bat_1)
    score1 = "Score - "+str(a["Innings1 Runs Scored"]) + "-" + str(a["Innings1 Wickets Fell"])
    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score1), unsafe_allow_html=True)
    helper2.match_results(inning_bat_1, inning_bowl_1, inning_partner_1,inning_fow_1)

    helper2.header(inning_bat_2)
    score2 = "Score - "+str(round(a["Innings2 Runs Scored"])) + "-" + str(round(a["Innings2 Wickets Fell"]))
    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score2), unsafe_allow_html=True)
    helper2.match_results(inning_bat_2, inning_bowl_2,inning_partner_2,inning_fow_2)
    try:
        helper2.header(inning_bat_3)
        if pd.isna(test_match_result_df.iloc[0]["Innings3 Runs Scored"]):
            score4 = "Score - "+str(a["Innings4 Runs Scored"]) + "-" + str(a["Innings4 Wickets Fell"])
            st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score4), unsafe_allow_html=True)
        else:
            score3 = "Score - "+str(round(a["Innings3 Runs Scored"])) + "-" + str(round(a["Innings3 Wickets Fell"]))
            st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score3), unsafe_allow_html=True)

        helper2.match_results(inning_bat_3, inning_bowl_3,inning_partner_3,inning_fow_3)
    except NameError:
        print("Did not bat")
    try:
        helper2.header(inning_bat_4)
        if pd.isna(test_match_result_df.iloc[0]["Innings4 Runs Scored"]) == False:
            score4 = "Score - "+str(round(a["Innings4 Runs Scored"])) + "-" + str(round(a["Innings4 Wickets Fell"]))
            st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score4), unsafe_allow_html=True)
        helper2.match_results(inning_bat_4, inning_bowl_4,inning_partner_4,inning_fow_4)
    except NameError:
        print("Did not bat")



#jhn jhn test likha hua h whn odi hoga bs variable ka naam change nii kiye hai
def results_odi(specific_match, test_match_df, test_partnership_df, test_fow_df,test_bowling_df, test_player_df, test_batting_df):
    st.title("Series - "+specific_match.iloc[0]["Series Name"])
    st.title("Match - "+specific_match.iloc[0]["Match Name"])
    a = specific_match.iloc[0]["Match Date"]
    st.markdown("<h6>{}</h6>".format(a), unsafe_allow_html=True)
    match_id = specific_match.iloc[0][0]
    new_fow_df = preprocess.fow_pre(test_fow_df, match_id)
    sorted_batting_df = preprocess.batting_pre(test_batting_df, new_fow_df, test_player_df, match_id)
    sorted_batting_df = preprocess.bowler_pre(test_bowling_df, test_player_df, sorted_batting_df, match_id)
    new_bowling_df = preprocess.main_bowling_pre(test_bowling_df, test_player_df,  match_id)
    partnership_df = preprocess.partnership(match_id, test_partnership_df,test_player_df)
    fall_of_wickets_df = preprocess.fall_of_wickets(match_id,test_fow_df,test_player_df)
    innings = sorted_batting_df["innings"].unique()

    # for the score of each match and more
    test_match_result_df = preprocess.match_score_odi(test_player_df, test_match_df, match_id)

    # venue
    venue = test_match_result_df.iloc[0]["Match Venue (Stadium)"]+ "," + test_match_result_df.iloc[0]["Match Venue (City)"] + "," + test_match_result_df.iloc[0]["Match Venue (Country)"]
    st.markdown("<h5>Venue-{}</h5>".format(venue), unsafe_allow_html=True)
    toss = test_match_result_df.iloc[0]["Toss Winner"] + " won the toss and Choose to " + test_match_result_df.iloc[0]["Toss Winner Choice"]
    st.markdown("<h4>{}</h4>".format(toss), unsafe_allow_html=True)


    for i in innings:
        globals()[f'inning_bat_{i}'] = sorted_batting_df[sorted_batting_df["innings"] == i]
        globals()[f'inning_bowl_{i}'] = new_bowling_df[new_bowling_df["innings"] == i]
        globals()[f'inning_partner_{i}'] = partnership_df[partnership_df["innings"] == i]
        globals()[f'inning_fow_{i}'] = fall_of_wickets_df[fall_of_wickets_df["innings"] == i]

    a = test_match_result_df.iloc[0]
    winner = a["Match Result Text"]
    st.markdown("<h3>Match result - {}</h3>".format(winner), unsafe_allow_html=True)
    mom = a["player_name"]
    st.markdown("<h3>Man of the Match - {}</h3>".format(mom), unsafe_allow_html=True)
    helper2.header(inning_bat_1)
    score1 = "Score - "+str(round(a["Innings1 Runs Scored"])) + "-" + str(round(a["Innings1 Wickets Fell"]))
    st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score1), unsafe_allow_html=True)
    helper2.match_results(inning_bat_1, inning_bowl_1, inning_partner_1,inning_fow_1)

    try:
        helper2.header(inning_bat_2)
        if pd.isna(test_match_result_df.iloc[0]["Innings2 Runs Scored"]) == False:
            score2 = "Score - "+str(round(a["Innings2 Runs Scored"])) + "-" + str(round(a["Innings2 Wickets Fell"]))
            st.markdown("<h3 style='text-align: center;'>{}</h3>".format(score2), unsafe_allow_html=True)
        helper2.match_results(inning_bat_2, inning_bowl_2,inning_partner_2,inning_fow_2)
    except NameError:
        print("Did not bat")

def image(t20_player_df, t20_match_df, selected_player):
    country_df = t20_match_df[["Team1 ID", "Team1 Name"]]
    country_df.rename(columns={"Team1 ID": "country_id"}, inplace=True)
    t20_player_df = t20_player_df.merge(country_df, on=["country_id"], how="left")
    t20_player_df.rename(columns={"Team1 Name": "Country"}, inplace=True)

    image_df = t20_player_df[t20_player_df["player_name"] == selected_player]

    image_df["image_url"] = image_df["image_url"].fillna("https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image(image_df.iloc[0]["image_url"], width=100)
    with col2:
        st.markdown("<h5>Name</h5>", unsafe_allow_html=True)
        st.write(image_df.iloc[0]["player_name"])
        st.markdown("<h5>Country</h5>", unsafe_allow_html=True)
        st.write(image_df.iloc[0]["Country"])

    with col3:
        st.markdown("<h5>Born</h5>", unsafe_allow_html=True)
        st.write(image_df.iloc[0]["dob"])
        st.markdown("<h5>Batting Style</h5>", unsafe_allow_html=True)
        st.write(image_df.iloc[0]["batting_style"])
    with col4:
        image_df['dob'] = pd.to_datetime(image_df['dob'])

        # Function to calculate age
        def calculate_age(born):
            today = datetime.today()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            return age

        # Apply the function to the date_of_birth column
        image_df['age'] = image_df['dob'].apply(calculate_age)
        if pd.isna(image_df.iloc[0]["dod"]) == True:
            st.markdown("<h5>Age</h5>", unsafe_allow_html=True)
            st.markdown("<p>{}</p>".format(image_df.iloc[0]["age"]), unsafe_allow_html=True)
        else:
            st.markdown("<h5>DoD</h5>", unsafe_allow_html=True)
            st.markdown("<p>{}</p>".format(image_df.iloc[0]["dod"]), unsafe_allow_html=True)
        st.markdown("<h5>Bowling Style</h5>", unsafe_allow_html=True)
        st.write(image_df.iloc[0]["bowling_style"])

def radar(player1_test_df, player2_test_df, selected_player1, selected_player2):
    a = player1_test_df.iloc[0]
    df1 = pd.DataFrame({
        'Metric': ['Average', 'Strike Rate', '100', '4s','6s'],
        'Value': [a['Average']*2, a['Strike Rate'], a['100']*5,a['4s']/10, a['6s']]
    })

    b = player2_test_df.iloc[0]
    df2 = pd.DataFrame({
        'Metric': ['Average', 'Strike Rate', '100','4s', '6s'],
        'Value': [b['Average']*2, b['Strike Rate'], b['100']*5,b['4s']/10, b['6s']]
    })

    df1['DataFrame'] = '{}'.format(selected_player1)
    df2['DataFrame'] = '{}'.format(selected_player2)

    # Concatenate dataframes
    df_concat = pd.concat([df1, df2])

    custom_colors = ['#636EFA', '#EF553B'] # to set custom colours
    # Create radar chart
    fig = px.line_polar(df_concat, r='Value', theta='Metric', color='DataFrame', line_close=True, color_discrete_sequence=custom_colors)

    fig.update_traces(fill='toself')

    # to hide axis values
    fig.update_layout(
        polar=dict(
            radialaxis=dict(showticklabels=False),
            # angularaxis=dict(showticklabels=False)
        )
    )
    # st.title('Radar Chart Comparison')
    st.plotly_chart(fig)

def player_charts_test(test_player_df, test_batting_df,test_match_df, selected_player, odi_player_df, odi_batting_df,odi_match_df, t20_player_df, t20_batting_df,t20_match_df):
    test_df = preprocess.player_chart(test_player_df, test_batting_df,test_match_df, selected_player)
    odi_df = preprocess.player_chart_odi(odi_player_df, odi_batting_df,odi_match_df, selected_player)
    t20_df = preprocess.player_chart_odi(t20_player_df, t20_batting_df,t20_match_df, selected_player)

    strike_rate_df = test_df[['year', 'strikeRate']]
    strike_rate_df = strike_rate_df.merge(odi_df[['year', 'strikeRate']], on=['year'], how='left')
    strike_rate_df = strike_rate_df.merge(t20_df[['year', 'strikeRate']], on=['year'], how='left')
    strike_rate_df = strike_rate_df.fillna(0)
    strike_rate_df.rename(columns={"strikeRate_x": "Test", "strikeRate_y":"ODI", "strikeRate":"T20i"}, inplace=True)


    average_df = test_df[['year','Average']]
    average_df = average_df.merge(odi_df[['year', 'Average']], on=['year'], how='left')
    average_df = average_df.merge(t20_df[['year', 'Average']], on=['year'], how='left')
    average_df = average_df.fillna(0)
    average_df.rename(columns={"Average_x": "Test", "Average_y": "ODI", "Average": "T20i"}, inplace=True)

    # st.dataframe(average_df)


    a = "Strike Rate"
    helper2.charts(strike_rate_df, a)
    b = "Average"
    helper2.charts(average_df, b)
    runs = "runs"
    helper2.pre_chart(test_df, odi_df, t20_df, runs)
    fours = 'fours'
    sixes = 'sixes'
    helper2.pre_chart(test_df, odi_df, t20_df, fours)
    helper2.pre_chart(test_df, odi_df, t20_df, sixes)




# def player_charts_odi(test_player_df, test_batting_df,test_match_df, selected_player):

def player_charts_test_bowl(test_player_df, test_bowling_df, test_match_df, selected_player, odi_player_df,
                                      odi_bowling_df, odi_match_df, t20_player_df, t20_bowling_df, t20_match_df):
    test_df_bowl, test_df_bowl_country = preprocess.player_chart_bowl(test_player_df, test_bowling_df, test_match_df, selected_player)
    odi_df_bowl, odi_df_bowl_country = preprocess.player_chart_bowl_odi(odi_player_df, odi_bowling_df, odi_match_df, selected_player)
    t20_df_bowl, t20_df_bowl_country = preprocess.player_chart_bowl_odi(t20_player_df, t20_bowling_df, t20_match_df, selected_player)


    #first charts of year wise
    index = "year"
    chart1 = "line"
    value1 = "StrikeRate"
    helper2.pre_chart_bowl(test_df_bowl, odi_df_bowl, t20_df_bowl, index, value1, chart1)

    value2 = "Average"
    helper2.pre_chart_bowl(test_df_bowl, odi_df_bowl, t20_df_bowl, index, value2, chart1)

    value3 = "economy"
    helper2.pre_chart_bowl(test_df_bowl, odi_df_bowl, t20_df_bowl, index, value3, chart1)

    index2 = "Country"
    chart2 = "bar"
    value4 = "Matches"
    helper2.pre_chart_bowl(test_df_bowl_country, odi_df_bowl_country, t20_df_bowl_country, index2, value4, chart2)
    value5 = "Runs conceded"
    helper2.pre_chart_bowl(test_df_bowl_country, odi_df_bowl_country, t20_df_bowl_country, index2, value5, chart2)
    value6 = "wickets"
    helper2.pre_chart_bowl(test_df_bowl_country, odi_df_bowl_country, t20_df_bowl_country, index2, value6, chart2)









