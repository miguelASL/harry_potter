import numpy as np

# Datos de entrenamiento ficticios (respuestas de usuarios pasados y sus casas)
X_train = np.array([
    [5, 2, 1, 4, 3, 2],  # Gryffindor
    [2, 5, 3, 1, 4, 1],  # Ravenclaw
    [1, 3, 5, 2, 2, 4],  # Hufflepuff
    [4, 1, 2, 5, 1, 3],  # Slytherin
    [5, 3, 2, 4, 3, 2],  # Gryffindor
    [1, 5, 4, 2, 4, 1],  # Ravenclaw
    [3, 4, 1, 5, 2, 4],  # Hufflepuff
    [4, 1, 5, 2, 1, 3]   # Slytherin
])
y_train = np.array(["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin",
                   "Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"])
