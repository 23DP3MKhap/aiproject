import pandas as pd
# removes print limits in console
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)


# df stands for DataFrame
df = pd.read_csv('dati/data.csv', low_memory=False) # reading data.csv and storing it in variable so we can use it easier in future (Creating new DataFrame by default, so it wont affect original dataset)

#We are gonna predict best position column, so we doesnt need columns that doesnt have connection with it.
# The answer is storing in "Best Poistion" column.
# Dataset is also containing "Positions" columns, that doesnt have the answer directly, but its prolly will give massive boost to model accuracy, so it can be data leak


#---------------------------------------------------------------------------------------------------------------------------------
def cleanData(df):
    print(f"Rows at the start: {len(df.index)}")
    df = deleteDuplcates(df)
    df = deleteNull(df)
    df = formatFix(df)
    print(f"Rows at the end: {len(df.index)}")
    df.to_csv('tirs.csv', index=False) # create csv

def deleteDuplcates(df):
    lenBefore = len(df.index)
    df = df.drop_duplicates() # Removes full identical data rows. "inplace = true" is rule to edit current dataframe w/o making new one
    print(f"{lenBefore - len(df.index)} rows deleted because they are full duplicates")

    lenBefore = len(df.index)
    df = df.drop_duplicates(subset = "ID") # Removes rows with identical IDs
    print(f"{lenBefore - len(df.index)} rows deleted because they have duplicate ID")
    return df

def deleteNull(df): # df.dropna(inplace = True) # Deleting all rows that contains null values. Cant be used in this dataset cus there is null values that have meaning
    lenBefore = len(df.index)
    df = df.dropna(subset = "Best Position") # Deleting all rows where Best Position column is null
    lenAfter = len(df.index)
    deletedRows = lenBefore - lenAfter
    print(f"{deletedRows} rows deleted because Best Position is null")
    return df

def formatFix(df): # Data format fix to one predictable format
    df = df.rename(columns={"↓OVA" : "OVA"}) # So i dont have to write this stupid arrow

    #--------------------------CLUB----------------------------------
    # Club format fix: club is stored in dataset with \n at the beggining. For example: \n\n\n\nFC Barcelona.
    # This leads to error when trying to find any club name. For example: print(df[df["Club"] == "FC Barcelona"]) result is zero cus there is \n\n\n\n at the begginig that does count in request

    print(f"{(df["Club"] != df["Club"].str.strip()).sum()} rows is corrupted with line breaks at the start") # How much rows is corrupted witn \n
    for i in df.index:
        df.loc[i, "Club"] = df.loc[i, "Club"].strip()
    #----------------------------------------------------------------


    #--------------------------HEIGHT--------------------------------
    # Height format fix: Some rows containig height info not in cm but in feet. For example: 6'2" instead of normal 188cm
    # https://www.geeksforgeeks.org/utilities/feet-to-centimeters-converter/

    print(f"{(~df["Height"].str.endswith("cm")).sum()} rows is corrupted with feet") # How much rows is corrupted with feet
    df["Height"] = df["Height"].apply(height_to_cm) #.apply is applying function to all rows in Height column
    #----------------------------------------------------------------

    #---------------------------Weight-------------------------------
    # Weight format fix: Some rows containig weight info not in kg but in lbs. For example: 179lbs instead of normal 81kg
    # https://www.unitconverters.net/weight-and-mass/lbs-to-kg.htm
    print(f"{df["Weight"].str.endswith("lbs").sum()} rows is corrupted with lbs") # How much rows is corrupted with lbs
    df["Weight"] = df["Weight"].apply(weight_to_kg)
    #----------------------------------------------------------------


    #-------------------------W/F, SM, IR----------------------------
    # W/F, SM, IR format fix (all columns got the same problem): every row containing ★ symbol and random space
    starColumns = ["W/F", "SM", "IR"]
    for i in starColumns:
        # .str.replace("★", "") # removes star
        # .str.strip() # removes spaces
        # .astype(int) # changing column type from string to integer
        df[i] = df[i].str.replace("★", "").str.strip().astype(int) # "4 ★" -> "4 " -> "4" -> 4
        print(f"all {i} column rows was fixed")
    #----------------------------------------------------------------


    #--------------------Value, Wage, Release Clause-----------------
    # Value, Wage, Release Clause format fix: rows  is containing sum with M (millions) or K (thousands) in it
    # euros_to_int() )
    euroColumns = ["Value", "Wage", "Release Clause"]
    for i in euroColumns:
        print(f"{i} have {df[i].str.endswith("M").sum()} rows with M")
        print(f"{i} have {df[i].str.endswith("K").sum()} rows with K")
        df[i] = df[i].apply(euros_to_int)
    #----------------------------------------------------------------


    #-------------------------------Joined---------------------------
    # Joined format fix: from string to date format
    df["Joined"] = pd.to_datetime(df["Joined"], format = "%b %d, %Y")
    #----------------------------------------------------------------
    return df

def height_to_cm(value): # https://www.geeksforgeeks.org/utilities/feet-to-centimeters-converter/
    if value.endswith("cm"):
        return int(value.replace("cm", "")) # "170cm" -> 170
    feet = value.split("'")[0] # "6'2\"" -> "6"
    inches = value.split("'")[1].replace('"', "") # "6'2\"" -> "2\"" -> "2"
    return round(int(feet) * 30.48 + int(inches) * 2.54) # 6 * 30.48 + 2 * 2.54 = 188

def weight_to_kg(value): # https://www.unitconverters.net/weight-and-mass/lbs-to-kg.htm
    if value.endswith("kg"):
        return int(value.replace("kg", "")) # "72kg" -> 72
    return round(int(value.replace("lbs", "")) * 0.45359237) # "172lbs" -> 78

def euros_to_int(value):
    value = value.replace("€", "") # "€103.5M" -> "103.5M"
    if value.endswith("M"):
        return float(value.replace("M", "")) * 1000000 # "103.5" -> 103500000.0
    if value.endswith("K"):
        return float(value.replace("K", "")) * 1_000 # "560" -> 560000.0
    return float(value) # "550" -> 550.0, "0" -> 0.0

#---------------------------------------------------------------------------------------------------------------------------------


#columns=list(newdf.columns.values) - columns list
#cleanData(newdf)
#print(df["height"].head().T)  Check for dataset format by eyes. T is flipping columns and rows for 90 degrees
#print(df["Weight"])

# Deleting columns that we dont need at all:
# photoUrl, playerUrl - links
# LongName - we already got "name" and dont have any connection with position
# Hits - alot of null values and dont have any connection with position
# Contract, Loan Date end - 3 formats in one column and dont have any connection with position
newdf = df.drop(columns=["photoUrl", "playerUrl", "LongName", "Hits", "Contract", "Loan Date End"], axis="columns")
cleanData(newdf)

"""
Fat cat to celebrate 1 step
    /\_____/\
   /  o   o  \
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)
"""