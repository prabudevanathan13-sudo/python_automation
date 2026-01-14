#dict to excel
import pandas as pd
#dict
data={
    "name":["raja","pinki","raju"],
    "age":[22,34,45],
    "city":["delhi", "pondicherry","madaras"]
    }
#convert dict to dataframe      
df=pd.DataFrame(data)
#export dataframe to excel
df.to_excel("data.xlsx", index=False)
