import pandas as pd 
import numpy as np

dems = ['User ID','Age','Gender','Height','Ethnicity','LanguagesSpoken','Handedness','Major/Minor']
 #accepts the dems arg which is simply a list of demographics you want to pull, important*** also include the column with your user id's first
def givedems(dems,dems_csv):
    df = pd.read_csv(rf'raw-data/{dems_csv}.csv')
    df = pd.DataFrame(df,columns =dems )
    for i in range (1,len(dems)-1):
        demholder = df.groupby(dems[i])
        print(demholder.groups)


loc = "Demographics"
givedems(dems,loc)
        
