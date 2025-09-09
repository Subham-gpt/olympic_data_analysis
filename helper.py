import numpy as np

def medals(df):
    medals = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medals = medals.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medals['Total'] = medals['Gold'] + medals['Silver'] + medals['Bronze']

    return medals

def fetch_medals(df, year, country):
    medals_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medals_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medals_df[medals_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medals_df[medals_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medals_df[(medals_df['Year'] == int(year)) & (medals_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Gold').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

def country_year(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    countries = np.unique(df['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0,'Overall')
    
    return years,countries

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().sort_values().reset_index()
    nations_over_time.columns = ['Year',col]
    return nations_over_time

def most_succcessful(df,sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,how='left',on='Name')[['Name','count','Sport','region']].drop_duplicates('Name')
    x.rename(columns={'count':'Medals'},inplace=True)
    
    return x

def most_succcessful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]
    
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.columns = ['Name','Medals','Sport']
    
    return x

def yearwise_medals(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')

    return pt

def weight_vs_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    male = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = male.merge(female, on='Year', how='left')
    final.columns = ['Year','Male','Female']
    final.fillna(0,inplace=True)

    return final