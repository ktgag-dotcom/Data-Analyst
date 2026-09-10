import pandas as pd
from sklearn.cluster import KMeans

df=pd.read_csv('data/charts.csv',parse_dates=['chart_date'])
df['song_id']=df.artist.str.lower().str.strip()+'|'+df.song.str.lower().str.strip()
df=df.sort_values(['song_id','chart_date'])
g=df.groupby('song_id')
df['previous_rank']=g['rank'].shift(1)
df['momentum']=df.previous_rank-df['rank']
df['acceleration']=df.momentum-g.momentum.shift(1)
df['week_number']=g.cumcount()+1
first8=df[df.week_number<=8].pivot(index='song_id',columns='week_number',values='rank').dropna()
if len(first8)>=4:
    first8['trajectory_cluster']=KMeans(n_clusters=min(4,len(first8)),random_state=42,n_init=10).fit_predict(first8)
    print(first8.trajectory_cluster.value_counts().sort_index())
print(df[['song','artist','chart_date','rank','momentum','acceleration']].head(20))
