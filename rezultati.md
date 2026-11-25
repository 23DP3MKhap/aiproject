# Results

## 1. What the data is and where it comes from

FIFA 21 player data from the EA Sports game FIFA 21, scraped from sofifa.com and published on Kaggle by the user *yagunnersya*. The link and license are in `dati/AVOTS.txt`.

The dataset has **18,979 players and 77 columns**: name, club, height, weight, market value, wage, contract and about 40 skill ratings on a scale from 0 to 99.

## 2. What was wrong with the data and what I did

### Rows

| Check | Rows removed |
|---|---|
| Fully identical rows | 0 |
| Duplicate player IDs | 0 |
| Rows without `Best Position` | 0 |

**0 rows removed in total** (18,979 at the start, 18,979 at the end). The problems in this dataset are in the format, not in the rows.

Names in the `Name` column repeat 1,059 times, but these are different players with the same short name, and their IDs are different. That's why I didn't remove anything by name.

### Format

| Column | Problem | What I did | Rows |
|---|---|---|---|
| `Club` | The name starts with `\n\n\n\n`, so searching `df[df["Club"] == "FC Barcelona"]` finds no rows | Removed with `strip()` | 18,742 |
| `Height` | Height is given both as `170cm` and in feet and inches (`6'2"`) | Converted everything to centimeters: feet × 30.48 + inches × 2.54 | 40 converted |
| `Weight` | Weight is given both as `72kg` and in pounds (`172lbs`) | Converted everything to kilograms: pounds × 0.4536 | 40 converted |
| `W/F`, `SM`, `IR` | Text with a star: `4 ★` or `4★` | Removed ★ and spaces, converted to a number | All |
| `Value`, `Wage`, `Release Clause` | Text with currency and abbreviations: `€103.5M`, `€560K` | Converted to a number in euros (M × 1,000,000, K × 1,000) | All |
| `Joined` | Date stored as text: `Jul 1, 2004` | Converted to a date | All |
| `↓OVA` | Arrow in the column name | Renamed to `OVA` | – |

For the model, this cleaning mattered for height and weight, because they are model features. Without the conversion, 40 players would have a height of `6` and a weight of `172`, and the model would accept these numbers without any error.

### Removed and untouched columns

- **Removed:**
  - `photoUrl`, `playerUrl`: links;
  - `LongName`: the data already has `Name`;
  - `Hits`: 2,595 missing values, and it isn't related to position;
  - `Contract`, `Loan Date End`: three different formats in one column, and they aren't needed to predict position.
- **The missing values in `Loan Date End`** (17,966) are not an error: an end date only exists for players on loan.
- **The other columns** were already in the correct format (numbers or consistently formatted text), so I didn't change them.

### Does fixing the format remove rows?

No. The functions `int()`, `float()` and `pd.to_datetime()` with an explicit format raise an error on an unknown format instead of silently inserting an empty value. The script runs to the end, so there were no unknown formats in the data. After cleaning, the number of missing values is **0**.

## 3. What the model predicts and how well

**Target:** the player's position group: goalkeeper (`Vartsargs`), defender (`Aizsargs`), midfielder (`Pussargs`) or attacker (`Uzbrucejs`). I merged the 15 positions into 4 groups because some positions have very few players (for example, `CF` has only 78), and neighboring positions (for example, `LB` and `LWB`) have almost the same skills.

**Features (13):** `Crossing`, `Finishing`, `Heading Accuracy`, `Short Passing`, `Dribbling`, `Sprint Speed`, `Interceptions`, `Standing Tackle`, `Sliding Tackle`, `GK Diving`, `GK Reflexes`, `Height`, `Weight`.

What I didn't use and why:
- **Sums** (`Attacking`, `Total Stats`, etc.): they just repeat the same skills;
- **`PAC`/`SHO`/`PAS`/`DRI`/`DEF`/`PHY`**: for goalkeepers, these columns hold different, goalkeeper skills under the same names;
- **`Positions`**: it's a data leak, because it often directly contains the correct answer.

**Model:** `RandomForestClassifier`. The data is split into 80% for training and 20% for testing (3,796 players), `random_state=67`.

| | Accuracy |
|---|---|
| Model | **90.6%** |
| Baseline (always says "Pussargs") | **38.3%** |

The model beats the baseline by ~52 percentage points. This is not luck: the test set has almost 3,800 players, and with a different `random_state` (42) the accuracy is 91.4%, so the result is stable.

**Where the model makes mistakes:** 357 mistakes out of 3,796. All of them are between **neighboring groups**:
- attacker ↔ midfielder: 140 + 61;
- midfielder ↔ defender: 88 + 68.

The model never makes a mistake with goalkeepers, and it never confuses a defender with an attacker.

## 4. The two most important columns

1. `Sliding Tackle` (0.156)
2. `Finishing` (0.152)

This makes sense. In the test data, the average `Sliding Tackle` is 64 for defenders and 24 for attackers. `Finishing` is the opposite: 67 for attackers, 35 for defenders. One column separates defenders, the other separates attackers, and midfielders are in between.

## 5. A row where the model is wrong

| Name | Best Position | Correct group | Prediction | Finishing | Crossing | Short Passing | Sliding Tackle |
|---|---|---|---|---|---|---|---|
| Neymar Jr | LW | Uzbrucejs | Pussargs | 87 | 85 | 87 | 29 |

Neymar plays on the left wing, but his skills look like a playmaker's: very high passing and crossing, just like an attacking midfielder. His `Positions` column also includes `CAM` (attacking midfielder). The difference between a winger and an attacking midfielder is more about tactics than skills, and the model can't see that from the numbers.

This isn't a random mistake. Of the 140 attackers the model called midfielders, **99 are wingers** (`RW` 61, `LW` 38). Similarly, of the 88 midfielders the model called defenders, **60 are defensive midfielders** (`CDM`), whose skills are close to defenders'.

## 6. What this model must not be used for

It must not be used to **decide which position a real player should play at a real football club**, or to scout young players.

The reason: the model was trained on FIFA 21 game ratings, not on real match data. The skill numbers were made up by the game developers, and they set them already knowing each player's position. So the model basically repeats EA Sports' opinion instead of measuring how the player actually plays. On top of that, it only knows 4 rough groups and often calls wingers midfielders.

## Self-assessment

I managed to find and fix the data format problems with a reason for each step, and the model clearly beats the baseline. I didn't find any row-level problems, because this data doesn't have any, and the model often confuses wingers with midfielders. Next time I would try more precise position groups, for example wingers as a separate group, and compare the model with more and with fewer features.
