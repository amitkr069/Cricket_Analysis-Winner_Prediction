import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import  seaborn as sns
import preprocess, helper, helper2
import plotly.figure_factory as ff
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(layout="wide")

test_match_df = pd.read_csv("test_Matches_Data.csv")
test_player_df = pd.read_csv("players_info.csv")
test_batting_df = pd.read_csv("test_Batting_Card.csv")
test_bowling_df = pd.read_csv("test_Bowling_Card.csv")
test_fow_df = pd.read_csv("test_Fow_Card.csv")
test_partnership_df = pd.read_csv("test_Partnership_Card.csv")

test_batting_df = preprocess.preprocessor_test_batting(test_batting_df)
test_match_df = preprocess.preprocessor_test_match(test_match_df)


#ODI data
odi_match_df = pd.read_csv("odi_Matches_Data.csv")
odi_player_df = pd.read_csv("odi_players_info.csv")
odi_batting_df = pd.read_csv("odi_Batting_Card.csv")
odi_bowling_df = pd.read_csv("odi_Bowling_Card.csv")
odi_fow_df = pd.read_csv("odi_Fow_Card.csv")
odi_partnership_df = pd.read_csv("odi_Partnership_Card.csv")

odi_match_df = preprocess.preprocessor_odi_match(odi_match_df)
odi_batting_df = preprocess.preprocessor_odi_batting(odi_batting_df)


#T20 data
t20_match_df = pd.read_csv("t20i_Matches_Data.csv")
t20_player_df = pd.read_csv("t20i_players_info.csv")
t20_batting_df = pd.read_csv("t20i_Batting_Card.csv")
t20_bowling_df = pd.read_csv("t20i_Bowling_Card.csv")
t20_fow_df = pd.read_csv("t20i_Fow_Card.csv")
t20_partnership_df = pd.read_csv("t20i_Partnership_Card.csv")

#work of function is same thats why same function is given
t20_batting_df = preprocess.preprocessor_odi_batting(t20_batting_df)

t20_match_df = preprocess.preprocessor_t20_match(t20_match_df)

st.markdown("<h1 style='text-align: center;'>Cricket Analysis</h1>", unsafe_allow_html=True)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Test Matches', 'ODI Matches', 'T20 Matches', "Player wise Analysis")
)

if user_menu == 'Test Matches':
    series = helper.series(test_match_df)
    selected_series = st.selectbox("select the series", series)

    test_match_df = helper.selection(test_match_df, selected_series)

    team1, team2 = helper.teams(test_match_df)
    if (selected_series == "Overall"):
        selected_team1 = st.selectbox("select team1", team1)
        selected_team2 = st.selectbox("select team2", team2)

        # dataframe

        select_match_df = helper.select_match_overall(test_match_df, selected_team1, selected_team2)
        if (select_match_df.empty):
            st.header("No matches")
        else:
            #select series
            series_test_overall = select_match_df['Series Name'].unique().tolist()
            series_test_overall.sort()
            selected_series = st.selectbox("Select the series", series_test_overall)

            series1 = helper.selection1(select_match_df, selected_series)
            match = helper.matches(series1)
            selected_match = st.selectbox("select the match", match)
            specific_match = helper.select_match(series1, selected_match)
            # a = specific_match.iloc[0]["Match Result Text"]
            # st.markdown("<h1 style='text-align: center;'>{}</h1>".format(a), unsafe_allow_html=True)
            helper.results(specific_match, test_match_df, test_partnership_df, test_fow_df,test_bowling_df, test_player_df, test_batting_df)
            # st.header(results)
    else:
        series_selected_match = test_match_df
        match = helper.matches(series_selected_match)
        selected_match = st.selectbox("select the match", match)
        specific_match = helper.select_match(series_selected_match, selected_match)
        # a = specific_match.iloc[0]["Match Result Text"]
        # st.markdown("<h1 style='text-align: center;'>{}</h1>".format(a), unsafe_allow_html=True)
        helper.results(specific_match, test_match_df, test_partnership_df, test_fow_df,test_bowling_df, test_player_df, test_batting_df)
        # st.header(results.iloc[0])

if user_menu == 'ODI Matches':
    series = helper.series(odi_match_df)
    selected_series = st.selectbox("select the series", series)
    team1_odi = odi_match_df['Team1 Name'].unique().tolist()
    team1_odi.sort()

    team2_odi = odi_match_df['Team2 Name'].unique().tolist()
    team2_odi.sort()
    odi_match_df = helper.selection(odi_match_df, selected_series)

    if (selected_series == "Overall"):
        selected_team1 = st.selectbox("select team1", team1_odi)
        selected_team2 = st.selectbox("select team2", team2_odi)

        #selection of match
        #used same function as test wala
        select_match_df_odi = helper.select_match_overall(odi_match_df, selected_team1, selected_team2)
        if (select_match_df_odi.empty):
            st.header("No matches")
        else:
            series_test_overall_odi = select_match_df_odi['Series Name'].unique().tolist()
            series_test_overall_odi.sort()
            selected_series_odi = st.selectbox("Select the series", series_test_overall_odi)

            series1_odi = helper.selection1(select_match_df_odi, selected_series_odi)
            #using same function as test wala
            match_odi = helper.matches(series1_odi)

            selected_match_odi = st.selectbox("select the match", match_odi)
            specific_match_odi = helper.select_match(series1_odi, selected_match_odi)

            helper.results_odi(specific_match_odi, odi_match_df, odi_partnership_df, odi_fow_df, odi_bowling_df, odi_player_df, odi_batting_df)



    else:
        series_selected_match_odi = odi_match_df

        match_odi = helper.matches(series_selected_match_odi)
        selected_match_odi = st.selectbox("select the match", match_odi)
        specific_match_odi = helper.select_match(series_selected_match_odi, selected_match_odi)
        helper.results_odi(specific_match_odi, odi_match_df, odi_partnership_df, odi_fow_df, odi_bowling_df, odi_player_df, odi_batting_df)


if user_menu == 'T20 Matches':
    series = helper.series(t20_match_df)
    selected_series = st.selectbox("select the series", series)
    team1_t20 = t20_match_df['Team1 Name'].unique().tolist()
    team1_t20.sort()

    team2_t20 = t20_match_df['Team2 Name'].unique().tolist()
    team2_t20.sort()
    t20_match_df = helper.selection(t20_match_df, selected_series)

    if (selected_series == "Overall"):
        selected_team1 = st.selectbox("select team1", team1_t20)
        selected_team2 = st.selectbox("select team2", team2_t20)

        #selection of match
        #used same function as test wala
        select_match_df_t20 = helper.select_match_overall(t20_match_df, selected_team1, selected_team2)
        if (select_match_df_t20.empty):
            st.header("No matches")
        else:
            series_test_overall_t20 = select_match_df_t20['Series Name'].unique().tolist()
            series_test_overall_t20.sort()
            selected_series_t20 = st.selectbox("Select the series", series_test_overall_t20)

            series1_t20 = helper.selection1(select_match_df_t20, selected_series_t20)
            #using same function as test wala
            match_t20 = helper.matches(series1_t20)

            selected_match_t20 = st.selectbox("select the match", match_t20)
            specific_match_t20 = helper.select_match(series1_t20, selected_match_t20)

            helper.results_odi(specific_match_t20, t20_match_df, t20_partnership_df, t20_fow_df, t20_bowling_df, t20_player_df, t20_batting_df)



    else:
        series_selected_match_t20 = t20_match_df

        match_t20 = helper.matches(series_selected_match_t20)
        selected_match_t20 = st.selectbox("select the match", match_t20)
        specific_match_t20 = helper.select_match(series_selected_match_t20, selected_match_t20)
        helper.results_odi(specific_match_t20, t20_match_df, t20_partnership_df, t20_fow_df, t20_bowling_df, t20_player_df, t20_batting_df)

# now searching for a specific player
if user_menu == "Player wise Analysis":
    player_menu = st.radio(
        'Select an Option',
        ('Player info', 'Players Comparison', 'Face to Face')
    )
    if player_menu == 'Player info':

        players_list_test = test_player_df["player_name"].unique().tolist()
        players_list_test.sort()
        selected_player = st.selectbox("select a player", players_list_test)
        # image_df = test_player_df[test_player_df["player_name"] == selected_player]
        helper.image(t20_player_df, t20_match_df, selected_player)
        # col1, col2 = st.columns(2)
        # with col1:
        #     st.image(image_df.iloc[0]["image_url"], width=100)
        # with col2:
        #     st.header("")

        # option to choose stats type
        stats_menu = st.radio(
            '',
            ('Batting Stats', 'Bowling Stats')
        )

        selected_player_df_test = preprocess.player_info(test_player_df, test_batting_df, selected_player, 0)
        selected_player_df_odi = preprocess.player_info(odi_player_df, odi_batting_df, selected_player, 1)
        selected_player_df_t20 = preprocess.player_info(t20_player_df, t20_batting_df, selected_player, 2)

        frames = [selected_player_df_test, selected_player_df_odi, selected_player_df_t20]

        batting_df = pd.concat(frames)
        batting_df = batting_df.fillna(0)
        batting_df.rename(index={0:"Test", 1:"ODI", 2:"T20i"}, inplace=True)
        if stats_menu == 'Batting Stats':
            st.markdown("<h6>Batting Stats</h6>", unsafe_allow_html=True)
            st.dataframe(batting_df)
            helper.player_charts_test(test_player_df, test_batting_df,test_match_df, selected_player, odi_player_df, odi_batting_df,odi_match_df, t20_player_df, t20_batting_df,t20_match_df)



        selected_player_df_test_bowl = preprocess.player_bowl_info(test_player_df, test_bowling_df, selected_player, 0)
        selected_player_df_odi_bowl = preprocess.player_bowl_info(odi_player_df, odi_bowling_df, selected_player, 1)
        selected_player_df_t20_bowl = preprocess.player_bowl_info(t20_player_df, t20_bowling_df, selected_player, 2)

        frames_bowl = [selected_player_df_test_bowl, selected_player_df_odi_bowl, selected_player_df_t20_bowl]

        bowling_df = pd.concat(frames_bowl)
        bowling_df = bowling_df.fillna(0)
        bowling_df.rename(index={0: "Test", 1: "ODI", 2: "T20i"}, inplace=True)
        if stats_menu == 'Bowling Stats':
            st.markdown("<h6>Bowling Stats</h6>", unsafe_allow_html=True)
            st.dataframe(bowling_df)
            helper.player_charts_test_bowl(test_player_df, test_bowling_df, test_match_df, selected_player,
                                           odi_player_df,
                                           odi_bowling_df, odi_match_df, t20_player_df, t20_bowling_df, t20_match_df)

    if player_menu == 'Players Comparison':
        players_list_test = test_player_df["player_name"].unique().tolist()
        players_list_test.sort()
        selected_player1 = st.selectbox("select player1", players_list_test)
        selected_player2 = st.selectbox("select player2", players_list_test)
        if (selected_player1 == selected_player2):
            st.header("No Comparison btw same players")
        else:
            player1_df = helper2.player_comparison(test_player_df, test_batting_df, selected_player1, odi_player_df, odi_batting_df, t20_player_df, t20_batting_df)
            player2_df = helper2.player_comparison(test_player_df, test_batting_df, selected_player2, odi_player_df, odi_batting_df, t20_player_df, t20_batting_df)

            st.markdown("<h6>{}</h6>".format(selected_player1), unsafe_allow_html=True)
            st.dataframe(player1_df)

            st.markdown("<h6>{}</h6>".format(selected_player2), unsafe_allow_html=True)
            st.dataframe(player2_df)

            player1_test_df = player1_df[0:1]
            player1_odi_df = player1_df[1:2]
            player1_t20_df = player1_df[2:]

            player2_test_df = player2_df[0:1]
            player2_odi_df = player2_df[1:2]
            player2_t20_df = player2_df[2:]

            col1, col2 = st.columns(2)
            with col1:
                st.header("Test Match Comparison")
                helper.radar(player1_test_df, player2_test_df, selected_player1 ,selected_player2)
            with col2:
                st.header("ODI Match Comparison")
                helper.radar(player1_odi_df, player2_odi_df, selected_player1, selected_player2)

            col1, col2 = st.columns(2)
            with col1:
                st.header("T20i Match Comparison")
                helper.radar(player1_t20_df, player2_t20_df, selected_player1, selected_player2)

            # Normalizing the values
            # scaler = MinMaxScaler()
            #
            # df1['Normalized_Value'] = scaler.fit_transform(df1[['Value']])
            # df2['Normalized_Value'] = scaler.fit_transform(df2[['Value']])
            #
            # # Add an identifier column to each dataframe
            # df1['DataFrame'] = 'df1'
            # df2['DataFrame'] = 'df2'
            #
            # # Concatenate dataframes
            # df_concat = pd.concat(
            #     [df1[['Metric', 'Normalized_Value', 'DataFrame']], df2[['Metric', 'Normalized_Value', 'DataFrame']]])
            #
            # # Create radar chart
            # fig = px.line_polar(df_concat, r='Normalized_Value', theta='Metric', color='DataFrame', line_close=True)
            #
            # fig.update_traces(fill='toself')
            #
            # # Display the radar chart in Streamlit
            # st.title('Radar Chart Comparison')
            # st.plotly_chart(fig)

            # Normalize each row individually

            # Initialize Scaler
            # scaler = MinMaxScaler()
            #
            #
            # # Normalize each row individually
            # def normalize_rows(df):
            #     df_normalized = df.copy()
            #     values = df[['Value']].values.reshape(-1, 1)  # Extract values for normalization
            #     df_normalized[['Value']] = scaler.fit_transform(values)  # Normalize values
            #     return df_normalized
            #
            #
            # df1_normalized = normalize_rows(df1)
            # df2_normalized = normalize_rows(df2)
            #
            # # Melt the dataframes to long format for Plotly
            # df1_melted = df1_normalized.melt(id_vars=['Metric'], value_vars=['Value'], var_name='Metric_Type',
            #                                  value_name='Normalized_Value')
            # df2_melted = df2_normalized.melt(id_vars=['Metric'], value_vars=['Value'], var_name='Metric_Type',
            #                                  value_name='Normalized_Value')
            #
            # # Add identifier column
            # df1_melted['DataFrame'] = 'df1'
            # df2_melted['DataFrame'] = 'df2'
            #
            # # Concatenate dataframes
            # df_concat = pd.concat([df1_melted, df2_melted])
            #
            # # Create radar chart
            # fig = px.line_polar(df_concat, r='Normalized_Value', theta='Metric', color='DataFrame', line_close=True)
            #
            # fig.update_traces(fill='toself')
            #
            # # Display the radar chart in Streamlit
            # st.title('Radar Chart Comparison')
            # st.plotly_chart(fig)




            # df1 = pd.DataFrame({
            #     'Metric': ['A', 'B', 'C', 'D'],
            #     'Value': [4, 3, 2, 5]
            # })
            #
            # df2 = pd.DataFrame({
            #     'Metric': ['A', 'B', 'C', 'D'],
            #     'Value': [2, 4, 1, 3]
            # })
            #
            # # Add an identifier column to each dataframe
            # df1['DataFrame'] = 'a'
            # df2['DataFrame'] = 'b'
            #
            # # Concatenate dataframes
            # df_concat = pd.concat([df1, df2])
            #
            # # Create radar chart
            # fig = px.line_polar(df_concat, r='Value', theta='Metric', color='DataFrame', line_close=True)
            #
            # fig.update_traces(fill='toself')
            #
            # # Display the radar chart in Streamlit
            # st.title('Radar Chart Comparison')
            # st.plotly_chart(fig)
            #
            # # Display the DataFrames
            # st.subheader('DataFrame 1')
            # st.dataframe(df1)
            #
            # st.subheader('DataFrame 2')
            # st.dataframe(df2)










