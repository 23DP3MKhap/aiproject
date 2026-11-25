import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("tirs.csv") #reading clean csv data

#we are gonna predict Best Position
# grouping by positions in only 4 groups instead of 15 cus there is no reason to keep all 15 positions
group = {
    "GK": "Vartsargs",
    "CB": "Aizsargs", "LB": "Aizsargs", "RB": "Aizsargs", "LWB": "Aizsargs", "RWB": "Aizsargs",
    "CDM": "Pussargs", "CM": "Pussargs", "CAM": "Pussargs", "LM": "Pussargs", "RM": "Pussargs",
    "ST": "Uzbrucejs", "CF": "Uzbrucejs", "LW": "Uzbrucejs", "RW": "Uzbrucejs",
}
df["Asnwer"] = df["Best Position"].map(group)

# ---------------------------------------------------------------

# we are gonna predict with the most informative stats 
# we wont take Attacking, Total Stats etc. cus its sum of all other stats (just repeat all previous stats)
# we wont take PAC/SHO/PAS/DRI/DEF/PHY because we got more accurate stats for goalkeeper
# we wont take "Positions", cus its dataleak (contains Best Position in it)
stats = [ "Crossing", "Finishing", "Heading Accuracy", "Short Passing", "Dribbling", "Sprint Speed", "Interceptions", "Standing Tackle", "Sliding Tackle", "GK Diving", "GK Reflexes", "Height", "Weight",]

X = df[stats]      # Input
y = df["Asnwer"]      # right answer


# divide data on 80% for learning and 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=67, stratify=y 
) #strartify=y making both group proportions equal
#random_state=67 making result always the same (seed)


# model trainig
modelis = RandomForestClassifier(random_state=67)
modelis.fit(X_train, y_train)

predict = modelis.predict(X_test)
model_accuracy = accuracy_score(y_test, predict)


#base line (bazes linija)
most_often_group = y_train.value_counts().idxmax()
base_predict = [most_often_group] * len(y_test)
bazes_precizitate = accuracy_score(y_test, base_predict)


print(f"Modeļa precizitāte:   {model_accuracy:.1%}")
print(f"Bāzes līnija:         {bazes_precizitate:.1%}  (vienmēr saka '{most_often_group}')")

if model_accuracy > bazes_precizitate:
    print("Modelis pārspēj bāzes līniju.")
else:
    print("Modelis NEpārspēj bāzes līniju.")

#most important columns
importance = pd.Series(modelis.feature_importances_, index=stats)
importance = importance.sort_values(ascending=False)

print("\nDivas svarīgākās kolonnas:")
print(importance.head(2))
