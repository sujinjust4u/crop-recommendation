import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pickle

# Load data
df = pd.read_csv('Crop_recommendation.csv')

# Split features and target
X = df.drop('label', axis=1)
y = df['label']

# Scalers
ms = MinMaxScaler()
sc = StandardScaler()

# Fit and transform
X_ms = ms.fit_transform(X)
X_sc = sc.fit_transform(X_ms)

# Model - trained on the double-scaled data to match original logic
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_sc, y)

# Save
pickle.dump(model, open('model.pkl', 'wb'))
pickle.dump(ms, open('minmaxscaler.pkl', 'wb'))
pickle.dump(sc, open('standscaler.pkl', 'wb'))

print("Model retrained successfully! New model predicts strings directly.")
