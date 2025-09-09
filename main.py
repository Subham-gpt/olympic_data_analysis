import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = preprocessor.preprocess()

st.sidebar.title('Olympics Analysis')

st.sidebar.image('https://media.designrush.com/inspiration_images/320953/conversions/Olympics_logo_design1_1c79022838e5-desktop.jpg')

user_menu = st.sidebar.radio('Select an Option',('Medals','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis'))

if user_menu == 'Medals':
    st.sidebar.header('Medals')
    years,countries = helper.country_year(df)
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',countries)

    medals = helper.fetch_medals(df,selected_year,selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Performance')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medals in ' + str(selected_year) + ' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_year) + ' Olympics')

    st.dataframe(medals)


if user_menu == 'Overall Analysis':
    st.title('Overall Analysis')
    editions = df['Year'].unique().shape[0] - 1 # 1906 Olympics was held but not taken into consideration
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Editions',editions)
    with col2:
        st.metric('Hosts',cities)
    with col3:
        st.metric('Sports',sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Events',events)
    with col2:
        st.metric('Athletes',athletes)
    with col3:
        st.metric('Nations',nations)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Year', y='region', title='Participating Nations Over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df,'Event')
    fig = px.line(events_over_time, x='Year', y='Event', title='Events Over the Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df,'Name')
    fig = px.line(athletes_over_time, x='Year', y='Name', title='Athletes Over the Years')
    st.plotly_chart(fig)

    st.title('No. of Events over years')
    fig, axes = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    axes = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)

    x = helper.most_succcessful(df,selected_sport)
    st.dataframe(x)

if user_menu == 'Country-wise Analysis':

    st.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    st.header(selected_country + ' Medals Over the Years')

    country_df = helper.yearwise_medals(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df,selected_country)
    st.title(selected_country + ' excels in the following Sports')
    fig, axes = plt.subplots(figsize=(20,20))
    axes = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country)
    player_df = helper.most_succcessful_countrywise(df,selected_country)
    st.dataframe(player_df)

if user_menu == 'Athlete-wise Analysis':
    st.title('Athlete-wise Analysis')

    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    st.header('Age Distribution')
    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball','Judo','Football','Athletics','Swimming','Badminton',
                     'Sailing','Gymnastics','Art Competitions','Handball','Weightlifting','Wrestling',
                     'Hockey','Rowing','Fencing','Shooting','Boxing','Cycling','Diving','Canoeing','Tennis',
                     'Volleyball','Golf','Softball','Archery','Triathlon','Rugby','Polo','Ice Hockey','Taekwondo']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    st.header('Age Distribution Across Sports (Gold Medalist)')
    st.plotly_chart(fig)

    st.header('Height vs Weight Comparison')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)

    temp_df = helper.weight_vs_height(df,selected_sport)
    fig, axes = plt.subplots(figsize=(10,10))
    axes = sns.scatterplot(x='Weight', y='Height', hue='Medal', data=temp_df, style='Sex', s=80)
    st.pyplot(fig)

    st.header("Men vs Women Comparison")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male','Female'])
    st.plotly_chart(fig)
