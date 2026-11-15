import pandas as pd

df = pd.read_csv('dati/data.csv') # reading data.csv and storing it in variable so we can use it easier in future (Creating new DataFrame by default, so it wont affect original dataset). df standing for DataFrame


'''
Code i used to check if there is any duplcates to delete (There is no duplicates in this dataset):
df_duplicated = df.duplicated()
for x in df_duplicated.index:
    if df_duplicated.loc[x]:
        print(df_duplicated.loc[x])
'''
'''We are gonna predict best position column, so we dont need columns that doesnt have connection with it.
   The answer is storing in "Best Poistion" column.
   Dataset is also containing "Positions" columns, that doesnt have the answer directly, but its prolly will give massive boost to model accuracy, so im gonna do with it, and without it
'''
#---------------------------------------------------------------------------------------------------------------------------------
def cleanData(df):
    df.to_csv('dati/tirs.csv')
    deleteNull(df)
    formatCheck(df)
    newdf.to_csv('dati/tirs.csv')
def deleteNull(df):
    lenBefore = len(df.index)
    df.dropna(inplace = True) # Deleting all rows that contains null values. "inplace = true" making dropna edit current dataframe w/o making new one
    lenAfter = len(df.index)
    deletedRows = lenBefore - lenAfter
    print(f"{deletedRows} rows deleted because they contain null value")

def formatCheck(df): # Data format check. Most columns just contains numbers so we check if there is nothing else but numbers and check numbers on possibility of fake data by setting up boundaries for legal values with mediana 
    return
#---------------------------------------------------------------------------------------------------------------------------------

#Deleting columns that doesnt contains any info that can be used to predict best position
newdf = df.drop(columns=["LongName", "photoUrl", "playerUrl", "Nationality", "Age", "↓OVA", "POT", "Club", "Contract", "Height", "Weight", "Preferred Foot", "BOV", "Best Position", "Joined", "Loan Date End", "Value", "Wage", "Release Clause", "Skill", "Mentality", "Aggression", "Interceptions", "Composure", "Total Stats", "Base Stats", "W/F", "IR"], axis="columns")
#columns=list(newdf.columns.values)
cleanData(newdf)




