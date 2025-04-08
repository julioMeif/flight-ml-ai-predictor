import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from sklearn.utils.multiclass import unique_labels
import matplotlib.pyplot as plt
import joblib
import os

# Load the dataset
df = pd.read_csv("../data/model_dataset.csv")

# One-hot encode categorical features
X = pd.get_dummies(df.drop('actual_airlines', axis=1))
y = df['actual_airlines']

# Encode target labels
y_encoder = LabelEncoder()
y_encoded = y_encoder.fit_transform(y)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)

# Filter target names based on actual labels present in y_test
labels_in_test = unique_labels(y_test, y_pred)
target_names_filtered = y_encoder.inverse_transform(labels_in_test)

print(classification_report(y_test, y_pred, labels=labels_in_test, target_names=target_names_filtered))

# Feature importance
importances = pd.Series(model.feature_importances_, index=X.columns)
print("\nTop Feature Importances:")
print(importances.sort_values(ascending=False).head(10))

# Save model and encoder
os.makedirs("../model", exist_ok=True)
joblib.dump(model, "../model/random_forest_model.pkl")
joblib.dump(y_encoder, "../model/label_encoder.pkl")

# Show confusion matrix
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, display_labels=target_names_filtered, xticks_rotation=45)
plt.tight_layout()
plt.show()
