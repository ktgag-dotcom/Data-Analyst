import pandas as pd
import matplotlib.pyplot as plt

DATA='data/movies.csv'
df=pd.read_csv(DATA)
for c in ['budget','revenue','popularity','vote_average']:
    df[c]=pd.to_numeric(df[c],errors='coerce')
df=df[(df.budget>=0)&(df.revenue>=0)].copy()
df['profit']=df.revenue-df.budget
df['roi']=df['profit']/df.budget.replace(0,pd.NA)
summary=df.groupby('genre').agg(movies=('title','count'),median_budget=('budget','median'),median_revenue=('revenue','median'),median_roi=('roi','median')).sort_values('median_roi',ascending=False)
print(summary.head(15))
summary.head(10)['median_roi'].sort_values().plot.barh(title='Median ROI by Genre')
plt.tight_layout(); plt.savefig('genre_roi.png',dpi=160)
