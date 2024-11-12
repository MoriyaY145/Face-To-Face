import numpy as np
import pandas as pd

data = pd.read_csv('nose_labels.csv')
x = np.array(data.iloc[:, 1:10])
y = np.array(data.iloc[:, 10:-1])

lengthsDY = []
widthsDX = []
for i in range(len(x)):
    rx = x[i]
    ry = y[i]
    dy = ry[6]-ry[0]
    dx = rx[8]-rx[4]
    widthsDX.append(dx)
    lengthsDY.append(dy)

# Create DataFrame for the calculated lengths and widths
results = pd.DataFrame({'Length': lengthsDY, 'Width': widthsDX})
# Concatenate the original data DataFrame with the results DataFrame
final_data = pd.concat([data, results], axis=1)

# Write the final_data to a CSV file
final_data.to_csv('nose_labels.csv', index=False)

data = pd.read_csv("nose_labels.csv")

# sort by Length
df = data.sort_values("Length")
df.to_csv('nose_labels_sorted_according_length.csv', index=False)

# long and wide sort by width
data = pd.read_csv('nose_labels_sorted_according_length.csv')
x = data.iloc[887:, :]
x.to_csv('nose_labels_wide_and_long.csv', index=False)
data = pd.read_csv("nose_labels_wide_and_long.csv")
df = data.sort_values("Width")
df.to_csv('nose_labels_wide_and_long_sorted_according_width.csv', index=False)
