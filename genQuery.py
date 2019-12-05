import pandas as pd
import random 
count = 3

data=pd.read_excel('zen.xlsx', index_col=None)
data['single']=data['Q'].map(lambda x: len(x.split(" "))<=2)
single = data[data['single']]
single['familarity'] = single['familarity'].fillna(0)
single = single.sort_values('familarity')

query = []
totnum = len(single['ID'])
for i in range(0,count):
    qq = random.randint(0,totnum-1)
    query.append(single.iloc[qq,1])
print(" OR ".join(query))
