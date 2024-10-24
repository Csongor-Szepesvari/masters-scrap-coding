import csv
import pandas as pd

csv_file = 'mean_dict.csv'

nested_dict = {}

# reading the csv file 
df = pd.read_csv(csv_file) 
  
# updating the column value/data 
#df.loc[5, 'Name'] = 'SHIV CHANDRA'
# update column values where column%2==1, name=str(column//2+1)+"th largest"
for col in range(0,250,2):
    name = str(col//2+1)+"th largest"
    df.loc[col, name] = 0
  
# writing into the file 
df.to_csv("mean_dict_modified.csv", index=False) 
  
print(df) 