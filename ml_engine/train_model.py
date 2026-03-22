import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")  # Important for web apps (no GUI)

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import seaborn as sns
import matplotlib.pyplot as plt
import os

from sklearn.metrics import roc_curve, auc

# ---------------- LOAD DATASET ----------------
df = pd.read_csv("learning_dataset.csv")

# ---------------- FEATURES & TARGET ----------------
X = df.drop("learning_success", axis=1)
y = df["learning_success"]

# ---------------- SPLIT DATA ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- TRAIN MODEL ----------------
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- PREDICT ----------------
pred = model.predict(X_test)

# ---------------- EVALUATE ----------------
acc = accuracy_score(y_test, pred)

print("Model Accuracy:", acc)
print(classification_report(y_test, pred))

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "ml_engine/learning_model.pkl")
print("Model saved successfully 🚀")

# ---------------- FEATURE IMPORTANCE ----------------
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

feature_importance.to_csv("ml_engine/feature_importance.csv", index=False)
print("Feature importance saved 🚀")

# ---------------- CONFUSION MATRIX ----------------
cm = confusion_matrix(y_test, pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Purples",
            xticklabels=["Low Success", "High Success"],
            yticklabels=["Low Success", "High Success"])

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")

# Save directly into static folder
if not os.path.exists("static"):
    os.makedirs("static")

plt.tight_layout()
plt.savefig("static/confusion_matrix.png")
plt.close()

print("Confusion matrix saved 🚀")



# ---------------- ROC CURVE ----------------
y_prob = model.predict_proba(X_test)[:, 1]

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6,5))
plt.plot(fpr, tpr, color="purple", label=f"AUC = {roc_auc:.2f}")
plt.plot([0,1], [0,1], linestyle="--", color="gray")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend(loc="lower right")

plt.tight_layout()
plt.savefig("static/roc_curve.png")
plt.close()

print("ROC curve saved 🚀")
print("AUC Score:", roc_auc)