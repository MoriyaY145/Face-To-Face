import numpy as np
import pandas as pd

data = pd.read_csv('eye_labels.csv')
x = np.array(data.iloc[:, 1:13])
y = np.array(data.iloc[:, 13:-1])

lengthsDY = []
widthsDX = []
for i in range(len(x)):
    rx = x[i]
    ry = y[i]
    dy = (ry[4]+ry[5]-ry[1]-ry[2])/2
    dx = rx[3]-rx[0]
    widthsDX.append(dx)
    lengthsDY.append(dy)

# Create DataFrame for the calculated lengths and widths
results = pd.DataFrame({'Length': lengthsDY, 'Width': widthsDX})
# Concatenate the original data DataFrame with the results DataFrame
final_data = pd.concat([data, results], axis=1)

# Write the final_data to a CSV file
final_data.to_csv('eye_labels.csv', index=False)

# sort by Length
data = pd.read_csv("eye_labels.csv")
df = data.sort_values("Length")
df.to_csv('eye_labels_sorted_according_length.csv', index=False)

# silt and small sort by Width
data = pd.read_csv('eye_labels_sorted_according_length.csv')
x = data.iloc[:6787, :]
x.to_csv('eye_labels_silt_and_small.csv', index=False)
df = pd.read_csv("eye_labels_silt_and_small.csv")
df = df.sort_values("Width")
df.to_csv('eye_labels_silt_and_small_sorted_according_width.csv', index=False)