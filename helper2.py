import pandas as pd
import streamlit as st
import preprocess
import preprocess, helper
import plotly.express as px
import matplotlib.pyplot as plt

def header(inning):
    st.header("Inning"+str(inning.iloc[0]["innings"]) +" " +inning.iloc[0]["team"])
def match_results(inning_bat, inning_bowl,inning_partner,inning_fow):
    col1, col2= st.columns(2)
    with col1:
        st.markdown("<h6>Score card</h6>", unsafe_allow_html=True)
        inning_bat = inning_bat[["Batsman Name", "runs", "balls", "strikeRate", "fours", "sixes", "wicketType", "Bowler Name"]]
        st.dataframe(inning_bat)
    with col2:
        st.markdown("<h6>Bowling Stats</h6>", unsafe_allow_html=True)
        inning_bowl = inning_bowl[["Bowler","overs","maidens","conceded", "wickets", "economy","dots","fours","sixes" ]]
        st.dataframe(inning_bowl)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<h6>Partnership Stats</h6>", unsafe_allow_html=True)
        inning_partner = inning_partner[["for wicket","player1_name", "player2_name", "partnership runs", "partnership balls", "player1 runs", "player1 balls", "player2 runs", "player2 balls"]]
        st.dataframe(inning_partner)
    with col2:
        st.markdown("<h6>Fall of Wickets</h6>", unsafe_allow_html=True)
        inning_fow = inning_fow[["wicket", "runs", "over", "Batsman"]]
        st.dataframe(inning_fow)

# this was giving error
# def score_wicket(Innings, test_match_result_df):
#     score = str(test_match_result_df.iloc[0]["{} Runs Scored"].format(Innings)) + "-" + str(test_match_result_df.iloc[0]["{} Wickets Fell"].format(Innings))
#     st.markdown("<h4 style='text-align: center;'>{}</h4>".format(score), unsafe_allow_html=True)

def player_comparison(test_player_df, test_batting_df, selected_player, odi_player_df, odi_batting_df,t20_player_df, t20_batting_df):
    selected_player_df_test = preprocess.player_info(test_player_df, test_batting_df, selected_player, 0)
    selected_player_df_odi = preprocess.player_info(odi_player_df, odi_batting_df, selected_player, 1)
    selected_player_df_t20 = preprocess.player_info(t20_player_df, t20_batting_df, selected_player, 2)

    frames = [selected_player_df_test, selected_player_df_odi, selected_player_df_t20]

    batting_df = pd.concat(frames)
    batting_df = batting_df.fillna(0)
    # batting_df.rename(index={0: "Test", 1: "ODI", 2: "T20i"}, inplace=True)
    # st.markdown("<h6>Batting Stats</h6>", unsafe_allow_html=True)

    #innings, runs, average, strike rate, 100, 6s
    # batting_df = batting_df[["Innings", "Runs", "Average","Strike Rate", "100","4s","6s"]]
    return batting_df

def charts(strike_rate_df, a):
    fig1 = px.line(strike_rate_df, x='year', y=['Test', 'ODI', 'T20i'])
    fig1.update_layout(
        title={
            'text': '{} over the years'.format(a),
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    st.plotly_chart(fig1)

def pre_chart(test_df, odi_df, t20_df, runs):
    average_df = test_df[['year', '{}'.format(runs)]]
    average_df = average_df.merge(odi_df[['year', '{}'.format(runs)]], on=['year'], how='left')
    average_df = average_df.merge(t20_df[['year', '{}'.format(runs)]], on=['year'], how='left')
    average_df = average_df.fillna(0)
    average_df.rename(columns={"{}_x".format(runs): "Test", "{}_y".format(runs): "ODI", "{}".format(runs): "T20i"}, inplace=True)

    # average_df[['year', 'Test', 'ODI', 'T20i']].set_index('year').plot(kind='bar', figsize=(12, 6))
    # plt.title('{} over the years'.format(runs))
    # plt.ylabel('Count')
    # plt.show()
    # was not working in streamlit

    if average_df.empty:
        st.header("")
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        average_df[['year', 'Test', 'ODI', 'T20i']].set_index('year').plot(kind='bar', ax=ax)
        ax.set_title('{} over the years'.format(runs))
        ax.set_ylabel('Count')
        st.pyplot(fig)


def pre_chart_bat(test_df, odi_df, t20_df,index, runs, chart):
    strike_rate_df = test_df[['{}'.format(index), '{}'.format(runs)]]
    strike_rate_df = strike_rate_df.merge(odi_df[['{}'.format(index), '{}'.format(runs)]], on=['{}'.format(index)], how='left')
    strike_rate_df = strike_rate_df.merge(t20_df[['{}'.format(index), '{}'.format(runs)]], on=['{}'.format(index)], how='left')
    strike_rate_df = strike_rate_df.fillna(0)
    strike_rate_df.rename(columns={"{}_x".format(runs): "Test", "{}_y".format(runs): "ODI", "{}".format(runs): "T20i"}, inplace=True)

    if strike_rate_df.empty:
        st.header("")
    else:
        if chart == "line":
            fig1 = px.line(strike_rate_df, x='{}'.format(index), y=['Test', 'ODI', 'T20i'])
            fig1.update_layout(
                title={
                    'text': '{} over the years'.format(runs),
                    'x': 0.5,
                    'xanchor': 'center'
                }
            )
            st.plotly_chart(fig1)

        if chart == "bar" and index == "Country":
            fig, ax = plt.subplots(figsize=(12, 4))
            strike_rate_df[['{}'.format(index), 'Test', 'ODI', 'T20i']].set_index('{}'.format(index)).plot(kind='bar', ax=ax)
            ax.set_title('{} over different countries'.format(runs))
            ax.set_ylabel('Count')
            st.pyplot(fig)

        if chart == "bar" and index == "year":
            fig, ax = plt.subplots(figsize=(12, 4))
            strike_rate_df[['{}'.format(index), 'Test', 'ODI', 'T20i']].set_index('{}'.format(index)).plot(kind='bar',
                                                                                                           ax=ax)
            ax.set_title('{} over the Years'.format(runs))
            ax.set_ylabel('Count')
            st.pyplot(fig)

def pre_chart_bowl(test_df, odi_df, t20_df,index, runs, chart):
    strike_rate_df = test_df[['{}'.format(index), '{}'.format(runs)]]
    strike_rate_df = strike_rate_df.merge(odi_df[['{}'.format(index), '{}'.format(runs)]], on=['{}'.format(index)], how='left')
    strike_rate_df = strike_rate_df.merge(t20_df[['{}'.format(index), '{}'.format(runs)]], on=['{}'.format(index)], how='left')
    strike_rate_df = strike_rate_df.fillna(0)
    strike_rate_df.rename(columns={"{}_x".format(runs): "Test", "{}_y".format(runs): "ODI", "{}".format(runs): "T20i"}, inplace=True)

    if strike_rate_df.empty:
        st.header("")
    else:
        if chart == "line":
            fig1 = px.line(strike_rate_df, x='{}'.format(index), y=['Test', 'ODI', 'T20i'])
            fig1.update_layout(
                title={
                    'text': '{} over the years'.format(runs),
                    'x': 0.5,
                    'xanchor': 'center'
                }
            )
            st.plotly_chart(fig1)

        if chart == "bar":
            fig, ax = plt.subplots(figsize=(12, 4))
            strike_rate_df[['{}'.format(index), 'Test', 'ODI', 'T20i']].set_index('{}'.format(index)).plot(kind='bar', ax=ax)
            ax.set_title('{} over different countries'.format(runs))
            ax.set_ylabel('Count')
            st.pyplot(fig)
