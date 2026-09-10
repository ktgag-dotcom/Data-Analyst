import re, pandas as pd
from rapidfuzz.fuzz import ratio

def clean_name(x): return re.sub(r'[^a-z ]','',str(x).lower()).strip()
def clean_email(x): return str(x).strip().lower()
def clean_phone(x): return re.sub(r'\D','',str(x))[-10:]
frames=[]
for source in ['crm','sales','marketing']:
    x=pd.read_csv(f'data/{source}.csv'); x['source']=source; frames.append(x)
df=pd.concat(frames,ignore_index=True)
df['name_clean']=df.name.map(clean_name); df['email_clean']=df.email.map(clean_email); df['phone_clean']=df.phone.map(clean_phone)
# deterministic master key: email, then phone, then normalized name+city
fallback=df.name_clean+'|'+df.city.fillna('').str.lower()
df['match_key']=df.email_clean.where(df.email_clean.ne(''),df.phone_clean.where(df.phone_clean.ne(''),fallback))
df['master_hcp_id']=pd.factorize(df.match_key)[0]+1
master=df.sort_values('source').groupby('master_hcp_id',as_index=False).first()
df[['source','source_id','master_hcp_id']].to_csv('hcp_crosswalk.csv',index=False); master.to_csv('master_hcp.csv',index=False)
print('Source rows:',len(df),'Golden records:',len(master))
