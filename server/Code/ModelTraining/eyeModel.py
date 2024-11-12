# model XGBoost
# עשיתי pip install xgboost
import numpy as np
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pandas as pd
from joblib import dump

data = pd.read_csv('../../data/ExcelKeyPoints//eye_labels.csv')
x = data.iloc[:, 1:-1]
y = data.iloc[:, -1]

# Encoding labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y_encoded, test_size=0.2, random_state=42)

# Training the XGBoost model
model = xgb.XGBClassifier(objective='multi:softmax', num_class=3)
model.fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)

# Calculating accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
# עובד Accuracy: 98.24%

# Save the model
dump(model, rf'../../models/eyeModel.keras')

