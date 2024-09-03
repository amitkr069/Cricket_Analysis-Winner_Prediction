import streamlit as st
# import pickle
# from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
# st.set_page_config(layout="wide")

def predict(odi_match_df, odi_fow_df, format):
    team_df = odi_fow_df[odi_fow_df['team'].isnull() == False]
    teams = team_df['team'].unique().tolist()

    cities = odi_match_df['Match Venue (City)'].unique().tolist()

    if format == 'ODI':
        # with open('pipe1.pkl', 'rb') as file:
        #     pipe = pickle.load(file)
        pipe = joblib.load('model_odi.joblib')

    if format == 'T20i':
        # with open('pipe_t20.pkl', 'rb') as file:
        #     pipe = pickle.load(file)
        pipe = joblib.load('model_t20.joblib')

    # print(type(pipe))

    st.title("{} win predictor".format(format))

    col1, col2 = st.columns(2)
    with col1:
        batting_team = st.selectbox('Select the batting team', sorted(teams))
    with col2:
        bowling_team = st.selectbox('Select the bowling team', sorted(teams))

    if (batting_team == bowling_team):
        st.header("Same teams cannot be selected")
    else:
        col1, col2 = st.columns(2)
        with col1:
            toss_winner = st.selectbox("Toss Winner", (batting_team, bowling_team))
        with col2:
            selected_city = st.selectbox('Select host city', sorted(cities))

        target = st.number_input('Target')
        col3, col4, col5 = st.columns(3)
        with col3:
            score = st.number_input('Current Score')
        with col4:
            overs = st.number_input('Overs completed')
        with col5:
            wickets = st.number_input('Wickets Fallen')

        if st.button('Predict Probability'):
            runs_left = round(target - score)
            if format == 'ODI':
                balls_left = round(300 - (overs*6))
            if format == 'T20i':
                balls_left = round(120 - (overs * 6))
            wickets = round(10 - wickets)

            if overs == 0:
                crr = 0
            else:
                crr = score/overs
            # print("fds",balls_left)
            if balls_left == 0:
                rrr = runs_left
                print(runs_left, rrr)
            else:
                rrr = (runs_left*6)/balls_left
            dict1 = {'team':[batting_team], 'bowling_team':[bowling_team], 'Match Venue (City)':[selected_city], 'Toss Winner':[toss_winner], 'runs left':[runs_left], 'balls left':[balls_left], 'wickets left':[wickets], 'target':[round(target)], 'crr':[crr],'rrr':[rrr]}
            input_df = pd.DataFrame(dict1)
            st.table(input_df)

            result = pipe.predict_proba(input_df)
            if balls_left == 0 and runs_left > 0:
                loss = 1
                win = 0
            elif runs_left <= 0 and balls_left >= 0:
                win = 1
                loss = 0
            else:
                loss = result[0][0]
                win = result[0][1]
            st.header(batting_team + "- " + str(round(win*100))+ '%')
            st.header(bowling_team + '- ' + str(round(loss*100)) + '%')
