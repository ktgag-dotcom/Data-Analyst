import pandas as pd

df=pd.read_csv('data/markets.csv')
cols=['population_growth','disease_burden','access_gap','income']
for c in cols:
    df[c+'_pct']=df[c].rank(pct=True)
df['market_score']=.30*df.population_growth_pct+.30*df.disease_burden_pct+.25*df.access_gap_pct+.15*df.income_pct
print(df.sort_values('market_score',ascending=False)[['market','market_score']].head(15))
