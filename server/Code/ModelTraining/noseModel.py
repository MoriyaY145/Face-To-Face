# model Random Forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import joblib
data = pd.read_csv('../../data/ExcelKeyPoints//nose_labels.csv')
x = data.iloc[:, 1:-1]
y = data.iloc[:, -1]
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
# Train the Random Forest model
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
joblib.dump(rf_model, rf'../../models/noseModel.keras')





