import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbs

# Load_data
df = pd.read_csv("KC_house_data.csv")
dfOriginal = df.copy()

dfCleaned = df[df["bedrooms"] <= 10]

#firs_boxplot
plt.subplot(1, 2, 1)
sbs.boxplot(x=dfOriginal["bedrooms"])
plt.title("Vorher: bedrooms mit Ausreißer")
plt.xlabel("Anzahl Schlafzimmer")

#sec_boxplot
plt.subplot(1, 2, 2)
sbs.boxplot(x=dfCleaned["bedrooms"])
plt.title(" Nachher: bedrooms bereinigt ")
plt.xlabel(" Anzahl Schlafzimmer ")

#title_boxplots
plt.suptitle("Ausreißerbehandlung bei bedrooms")
plt.tight_layout()
plt.show()

#resuults
print("Maximale Schlafzimmeranzahl vorher:", dfOriginal["bedrooms"].max())
print("Maximale Schlafzimmeranzahl nachher:", dfCleaned["bedrooms"].max())
print("Anzahl Immobilien vorher:", dfOriginal.shape[0])
print("Anzahl Immobilien nachher:", dfCleaned.shape[0])