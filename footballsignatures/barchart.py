import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load JSON data
with open("output_file.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# extract & clean price data
for item in data:
    item["price"] = float(item["price"].replace("\u00a3", "").replace(",", ""))  # convert to float
    item["surname"] = item["last_name"]  # extract surname

# convert to DataFrame
df = pd.DataFrame(data)

# sort by price in descending order
df = df.sort_values(by="price", ascending=False)

# define color palette (red to yellow)
colors = sns.color_palette("YlOrRd", len(df))[::-1]

# find maximum price
max_price = df["price"].max()

# create mask for bars with max price
highlight = df["price"] == max_price

# apply highlight colours for bars with max price
for i, is_max in enumerate(highlight):
    if is_max:
        colors[i] = (1, 0, 0) 

# create bar chart
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=df["surname"], y=df["price"], hue=df["surname"], palette=colors, legend=False)
plt.title("Maximum pricetag of £1,100 achieved by four footballers",fontsize=14)
plt.xlabel("Footballer",fontsize=10)
plt.ylabel("Price (£)",fontsize=10)
plt.xticks(rotation=45)

# show plot
plt.tight_layout()
plt.savefig("figures/barchart.pdf",format="pdf")
#plt.show()
#print('Plot saved as "barchart.pdf" in "figures" directory')
