import pandas as pd
import numpy as np

data=pd.read_excel('zen.xlsx', index_col=None)
out = pd.read_excel('output.xlsx',index_col=None)

# print(len(out))
for i in range(len(out)):
    query = out.iloc[i,1]
    tmp = np.array([data['Q']==query])
    # print(np.sum(tmp))
    # print(data.loc[data['Q']==query].iloc[0,6])
    # print(out.iloc[i,6])
    if np.sum(tmp) == 1:
        aa = list(tmp[0]).index(True)
        data.iloc[aa,6] = out.iloc[i,6]
    else:
        continue
    # print(data.loc[data['Q']==query].iloc[0,6])
    # aa=1
data.to_excel("output2.xlsx",index=False)