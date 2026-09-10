import pandas as pd

df=pd.read_csv('data/titles.csv')
metrics={'engagement':.35,'rating':.20,'completion_rate':.25,'cost_efficiency':.20}
for c in metrics:
    lo,hi=df[c].min(),df[c].max(); df[c+'_norm']=(df[c]-lo)/(hi-lo) if hi>lo else 0
df['content_value']=sum(df[c+'_norm']*w for c,w in metrics.items())
df['decision']=pd.qcut(df.content_value,3,labels=['Review/Drop','Monitor','Renew/Prioritize'])
print(df.sort_values('content_value',ascending=False)[['title','content_value','decision']].head(20))
