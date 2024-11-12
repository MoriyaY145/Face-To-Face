import numpy as np
import pandas as pd

data = pd.read_csv('mouth_labels.csv')
x = np.array(data.iloc[:, 1:21])
y = np.array(data.iloc[:, 21:-1])

tops = []
bottoms = []
widthsDX = []
for i in range(len(x)):
    rx = x[i]
    ry = y[i]
    top = ry[14]-ry[3]
    bottom = ry[9]-ry[18]
    total = top + bottom
    dx = max(rx)-min(rx)
    widthsDX.append(dx)
    tops.append(top)
    bottoms.append(bottom)

# Create DataFrame for the calculated lengths and widths
results = pd.DataFrame({'Top': tops, 'Bottom': bottoms, 'Width': widthsDX})
# Concatenate the original data DataFrame with the results DataFrame
final_data = pd.concat([data, results], axis=1)

# Write the final_data to a CSV file
final_data.to_csv('mouth_labels.csv', index=False)

data = pd.read_csv('mouth_labels.csv')
# sort by width
df = data.sort_values("Width")
df.to_csv('mouth_labels_sorted_according_width.csv', index=False)

# medium and thick sort by bottom
data = pd.read_csv('mouth_labels_sorted_according_width.csv')
x = data.iloc[2715:, :]
x.to_csv('mouth_labels_medium_and_thick.csv', index=False)
data = pd.read_csv("mouth_labels_medium_and_thick.csv")
df = data.sort_values("Bottom")
df.to_csv('mouth_labels_medium_and_thick_sorted_by_bottom.csv', index=False)

# medium and thick more 30 bottom sort by top
data = pd.read_csv('mouth_labels_medium_and_thick_sorted_by_bottom.csv')
x = data.iloc[6547:, :]
x.to_csv('mouth_labels_medium_and_thick_more_30_bottom.csv', index=False)
data = pd.read_csv("mouth_labels_medium_and_thick_more_30_bottom.csv")
df = data.sort_values("Top")
df.to_csv('mouth_labels_medium_and_thick_more_30_bottom_sorted_by_top.csv', index=False)
