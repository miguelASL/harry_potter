import sys
import pyttsx3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QRadioButton, QButtonGroup, QMessageBox, QProgressBar, QStackedWidget, QHBoxLayout
from models.random_forest import model
import numpy as np

# Inicializar el motor de texto a voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Preguntas y opciones
questions = [
    "¿Qué valor es más importante para ti?",
    "¿Cómo reaccionas ante un desafío?",
    "¿Cuál de estas actividades prefieres?",
    "¿Qué cualidad define mejor tu personalidad?",
    "¿Qué tipo de libros prefieres?",
    "¿Cómo te describirían tus amigos?"
]
options = [
    ["Valentía", "Inteligencia", "Lealtad", "Ambición"],
    ["Luchar", "Planear", "Cooperar", "Manipular"],
    ["Deportes", "Lectura", "Ayudar a otros", "Competencia"],
    ["Atrevido", "Curioso", "Amigable", "Determinado"],
    ["Aventura", "Ciencia ficción", "Romance", "Misterio"],
    ["Leal", "Ingenioso", "Amable", "Líder"]
]


class SortingHatApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sombrero Seleccionador")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            background-color: #1E1E1E; 
            color: white; 
            font-family: Arial, sans-serif;
        """)

        # Imagen del sombrero seleccionador
        self.image_label = QLabel(self)
        pixmap = QtGui.QPixmap("c:/Users/msarm/Desktop/sombrero.png")
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(
                200, 200, QtCore.Qt.KeepAspectRatio))
        else:
            self.image_label.setText("Imagen no encontrada")
            self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        # Layout principal
        self.layout = QVBoxLayout()
        self.layout.addWidget(
            self.image_label, alignment=QtCore.Qt.AlignCenter)

        # Barra de progreso
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #FF8C00;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #FF8C00;
                width: 20px;
            }
        """)
        self.progress_bar.setMaximum(len(questions))
        self.layout.addWidget(self.progress_bar)

        # Contenedor de preguntas
        self.question_container = QStackedWidget()
        self.layout.addWidget(self.question_container)

        self.radio_groups = []

        for i in range(len(questions)):
            page = QtWidgets.QWidget()
            page_layout = QVBoxLayout()
            label = QLabel(questions[i])
            label.setStyleSheet("font-size: 18px; margin-top: 20px;")
            page_layout.addWidget(label)

            group = QButtonGroup()
            for option in options[i]:
                btn = QRadioButton(option)
                btn.setStyleSheet("font-size: 16px; margin-left: 20px;")
                page_layout.addWidget(btn)
                group.addButton(btn)

            self.radio_groups.append(group)
            page.setLayout(page_layout)
            self.question_container.addWidget(page)

        # Botones de navegación
        self.nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("Anterior")
        self.prev_button.setStyleSheet("""
            background-color: #FF8C00; 
            font-size: 16px; 
            padding: 10px;
        """)
        self.prev_button.clicked.connect(self.prev_question)
        self.nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Siguiente")
        self.next_button.setStyleSheet("""
            background-color: #FF8C00; 
            font-size: 16px; 
            padding: 10px;
        """)
        self.next_button.clicked.connect(self.next_question)
        self.nav_layout.addWidget(self.next_button)

        self.layout.addLayout(self.nav_layout)

        # Botón de enviar
        self.submit_button = QPushButton("¡Descubre tu casa!")
        self.submit_button.setStyleSheet("""
            background-color: gold; 
            font-size: 18px; 
            padding: 10px; 
            margin-top: 20px;
        """)
        self.submit_button.clicked.connect(self.predict_house)
        self.layout.addWidget(self.submit_button,
                              alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.layout)

        self.current_question = 0
        self.update_question()

    def update_question(self):
        self.question_container.setCurrentIndex(self.current_question)
        self.progress_bar.setValue(self.current_question + 1)

    def next_question(self):
        if self.current_question < len(questions) - 1:
            self.current_question += 1
            self.update_question()

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.update_question()

    def predict_house(self):
        user_answers = []
        for i, group in enumerate(self.radio_groups):
            selected = group.checkedButton()
            if selected:
                user_answers.append(options[i].index(selected.text()) + 1)
            else:
                QMessageBox.warning(
                    self, "Error", "Debes responder todas las preguntas.")
                return

        user_answers = np.array(user_answers).reshape(1, -1)
        print(f"Respuestas del usuario: {user_answers}")
        predicted_house = model.predict(user_answers)[0]
        print(f"Casa predicha: {predicted_house}")

        responses = {
            "Gryffindor": "¡Eres valiente y audaz! Bienvenido a Gryffindor.",
            "Ravenclaw": "¡Tu inteligencia y creatividad te llevan a Ravenclaw!",
            "Hufflepuff": "¡La lealtad y el trabajo duro te hacen parte de Hufflepuff!",
            "Slytherin": "¡Eres ambicioso y astuto, encajas en Slytherin!"
        }

        engine.say(responses[predicted_house])
        engine.runAndWait()

        QMessageBox.information(
            self, "Sombrero Seleccionador", responses[predicted_house])

        # Mostrar visualmente el motivo de la elección
        self.show_reason(predicted_house)

    def show_reason(self, house):
        reasons = {
            "Gryffindor": "Valor y audacia son tus características principales.",
            "Ravenclaw": "Tu inteligencia y creatividad destacan.",
            "Hufflepuff": "La lealtad y el trabajo duro son tus virtudes.",
            "Slytherin": "La ambición y astucia te definen."
        }
        QMessageBox.information(self, "Motivo de la elección", reasons[house])
