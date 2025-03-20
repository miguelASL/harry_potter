import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
from data.training_data import X_train, y_train

# Cargar modelo entrenado o entrenar uno nuevo
try:
    model = joblib.load("sorting_hat_model.pkl")
except FileNotFoundError:
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    joblib.dump(model, "sorting_hat_model.pkl")
except Exception as e:
    print(f"Error al cargar o entrenar el modelo: {e}")
    model = None
