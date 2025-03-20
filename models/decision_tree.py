from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report
from data.training_data import X_train, y_train

# Modelo de Machine Learning
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predicciones en los datos de entrenamiento
y_pred = model.predict(X_train)

# Matriz de confusión
conf_matrix = confusion_matrix(y_train, y_pred)
print("Matriz de Confusión:")
print(conf_matrix)

# Reporte de clasificación
class_report = classification_report(y_train, y_pred)
print("Reporte de Clasificación:")
print(class_report)
