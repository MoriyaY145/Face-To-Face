# model logistic regression
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


data = pd.read_csv('../../data/ExcelKeyPoints/eyebrow_labels.csv')
x = data.iloc[:, 1:-1]
y = data.iloc[:, -1]
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Training the logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Making predictions
y_pred = model.predict(X_test_scaled)

# Calculating accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the model
pickle.dump(model, open('../../models/eyebrowModel.pkl', 'wb'))

# Save the scaler
pickle.dump(scaler, open('../../models/scalerEyebrow.pkl', 'wb'))
