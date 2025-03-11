import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# load data from JSON file
with open('output_file.json', 'r') as file:
    data = json.load(file)

# create DataFrame
df = pd.DataFrame(data)

# convert 'price' column to numeric & remove currency symbol
df['price'] = df['price'].replace({'£': '', ',': ''}, regex=True).astype(float)

# group data by 'presentation' and 'product_type' to get average price and count of items
grouped = df.groupby(['presentation', 'product_type']).agg(
    avg_price=('price', 'mean'),
    item_count=('price', 'size')
).reset_index()

# pivot data
heatmap_data = grouped.pivot(index='presentation', columns='product_type', values='avg_price')
count_data = grouped.pivot(index='presentation', columns='product_type', values='item_count')

# create new annotation matrix combining average price & item count
annotations = heatmap_data.copy().astype(object)

# format annotations
for i in range(annotations.shape[0]):
    for j in range(annotations.shape[1]):
        count = count_data.iloc[i, j]
        avg_price = heatmap_data.iloc[i, j]
        if pd.notna(avg_price):  # if there're items, show average price and item count
            annotations.iloc[i, j] = f"({int(count)} items)"  
        else:  # If there's no data, show "0 items"
            annotations.iloc[i, j] = "0 items"

# create mask so to display values only where there are items
mask = heatmap_data.isna()

# set up plot
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=annotations, fmt="", cmap="YlOrBr", linewidths=0.5, cbar_kws={'label': 'Average Price (£)'}, mask=mask)

# labels and title
plt.title('Framed and signed shirts are the most expensive', fontsize=16)
plt.ylabel('Presentation Type', fontsize=12)
plt.xlabel('Product Type', fontsize=12)

# show plot
plt.tight_layout()
plt.savefig("figures/heatmap.pdf",format="pdf")
#plt.show()
#print('Plot saved as "heatmap.pdf" in "figures" directory')
