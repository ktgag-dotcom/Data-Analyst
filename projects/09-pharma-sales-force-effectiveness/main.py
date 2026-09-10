import numpy as np, pandas as pd
np.random.seed(42); n=2500
calls=np.random.poisson(4,n); territory=np.random.choice(['North','South','East','West'],n)
baseline=np.random.gamma(4,20,n); uplift=45*(1-np.exp(-0.35*calls)); rx=baseline+uplift+np.random.normal(0,10,n)
df=pd.DataFrame({'hcp_id':range(1,n+1),'territory':territory,'calls':calls,'baseline_rx':baseline,'post_rx':rx})
df['rx_change']=df.post_rx-df.baseline_rx
df['call_band']=pd.cut(df.calls,[-1,1,3,5,8,99],labels=['0-1','2-3','4-5','6-8','9+'])
print(df.groupby('call_band',observed=True).rx_change.agg(['count','mean','median']))
