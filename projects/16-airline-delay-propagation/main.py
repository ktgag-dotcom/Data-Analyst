import pandas as pd

df=pd.read_csv('data/flights.csv',parse_dates=['scheduled_departure']).sort_values(['tail_num','scheduled_departure'])
g=df.groupby('tail_num')
df['previous_arrival_delay']=g.arrival_delay.shift(1)
df['previous_destination']=g.destination.shift(1)
df['turn_delay_change']=df.departure_delay-df.previous_arrival_delay
df['propagated']=((df.previous_arrival_delay>15)&(df.departure_delay>15)).astype(int)
print(df.groupby('origin').agg(flights=('flight_id','count'),propagation_rate=('propagated','mean'),median_recovery=('turn_delay_change','median')).sort_values('propagation_rate',ascending=False).head(20))
