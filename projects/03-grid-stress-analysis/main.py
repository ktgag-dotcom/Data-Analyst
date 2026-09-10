import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('data/grid.csv',parse_dates=['timestamp']).sort_values('timestamp')
df['net_load']=df['demand_mw']-df['renewable_mw']
df['rolling_mean']=df.net_load.rolling(24,min_periods=12).mean()
df['rolling_std']=df.net_load.rolling(24,min_periods=12).std()
df['z_stress']=(df.net_load-df.rolling_mean)/df.rolling_std
df['stress_flag']=df.z_stress>2
df['hour']=df.timestamp.dt.hour
print(df.groupby('hour').agg(avg_demand=('demand_mw','mean'),stress_hours=('stress_flag','sum')))
df.plot(x='timestamp',y=['demand_mw','renewable_mw'],title='Demand vs Renewable Generation')
plt.tight_layout(); plt.savefig('grid_profile.png',dpi=160)
