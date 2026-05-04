import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

print('Training flood risk model...')

df = pd.read_csv('data/rainfall.csv')

# Synthetic labels: based on rules + noise
df['score'] = (
    df['rainfall'] * 0.5 +
    df['prev_rainfall'] * 0.3 +
    np.random.normal(20, 10, len(df))  # elevation proxy noise
)
df['risk'] = pd.cut(df['score'], bins=[0, 40, 70, np.inf], labels=['Low', 'Medium', 'High'])

X = df[['rainfall', 'prev_rainfall']].values
y = (df['risk'] == 'High').astype(int)  # Binary for simplicity, expand later

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

score = model.score(X_test, y_test)
print(f'Model accuracy: {score:.3f}')

joblib.dump(model, 'flood_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

print('Saved flood_model.pkl & scaler.pkl')
print('Low risk threshold ~40, High >70 scores')
