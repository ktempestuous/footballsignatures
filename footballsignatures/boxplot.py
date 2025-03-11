import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load JSON data
with open("output_file.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# extract and clean price data
for item in data:
    item["price"] = float(item["price"].replace("\u00a3", "").replace(",", "")) 

# convert to DataFrame
df = pd.DataFrame(data)

# calculate quantiles
q1 = df["price"].quantile(0.25)
median = df["price"].median()
q3 = df["price"].quantile(0.75)
min_price = df["price"].min()
max_price = df["price"].max()

# create box plot
plt.figure(figsize=(8, 6))
ax = sns.boxplot(x=[0] * len(df), y=df["price"], hue=[0] * len(df), palette="YlOrBr", width=0.3, legend=False)
plt.title("Price range is large, spanning > £1,000",fontsize=14)
plt.ylabel("Price (£)",fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_xticks([])  
ax.set_xticklabels([])  

# annotate quantiles
for quantile, label in zip([min_price, q1, median, q3, max_price], ["Min", "Q1", "Median", "Q3", "Max"]):
    plt.text(0, quantile, f"{label}: £{quantile:.2f}", ha='center', va='bottom', fontsize=10, color='black',weight='bold')

# show plot
plt.tight_layout()
plt.savefig("figures/boxplot.pdf",format="pdf")
#plt.show()
#print('Plot saved as "boxplot.pdf" in "figures" directory')
