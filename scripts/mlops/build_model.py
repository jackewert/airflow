import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # Use regressor for continuous target
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import dump_svmlight_file

# Load dataset
df = pd.read_csv('./data/ai_adoption_dataset.csv')

# Basic preprocessing
df = df.dropna()  # Drop missing values

# Separate features and target
target = 'adoption_rate'  # Target column for prediction
X = df.drop(columns=[target])
y = df[target]

# Encode categorical variables if needed
for col in X.select_dtypes(include='object').columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])

# Encode target if it's categorical
if y.dtype == 'object':
    y = LabelEncoder().fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Plot actual vs predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Adoption Rate')
plt.ylabel('Predicted Adoption Rate')
plt.title('Actual vs Predicted Adoption Rate')
plt.savefig('adoption_rate_prediction.png')
plt.close()

# Save as .pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save as .libsvm
dump_svmlight_file(X, y, 'model.lib')
print("Model saved as 'model.pkl' and 'model.lib'")