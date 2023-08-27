import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QRadioButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,QHBoxLayout, QWidget, QGraphicsView, QGraphicsScene,QGraphicsItem
from PyQt5.QtGui import QPen, QColor, QPainterPath, QPainter, QBrush
from PyQt5.QtCore import Qt, QRectF
import math

class ConeItem(QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(-50, -50, 100, 100)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-50, -50, 100, 100)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black))
        painter.setBrush(QBrush(Qt.blue))

        path = QPainterPath()
        path.moveTo(-50, 0)  # Punto central del cono
        path.lineTo(50, -50)  # Punto derecho
        path.lineTo(50, 50)  # Punto izquierdo
        path.lineTo(-50, 0)  # Volver al punto central para cerrar el cono
        painter.drawPath(path)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 919, 519)
        self.setWindowTitle("Radio Buttons and Text Inputs Example")

        layout = QHBoxLayout()  # Cambio a QHBoxLayout para organizar elementos horizontalmente

        # Left side layout
        left_layout = QVBoxLayout()

        self.group = QButtonGroup()

        self.radio_cono = QRadioButton("Cono")
        self.radio_trono = QRadioButton("Trono de Cono")
        self.radio_hemisferio = QRadioButton("Hemisferio")

        left_layout.addWidget(self.radio_cono)
        left_layout.addWidget(self.radio_trono)
        left_layout.addWidget(self.radio_hemisferio)

        self.group.addButton(self.radio_cono)
        self.group.addButton(self.radio_trono)
        self.group.addButton(self.radio_hemisferio)

        self.label_radio1 = QLabel("Radio 1:")
        self.input_radio1 = QLineEdit()
        self.input_radio1.setFixedWidth(100)

        self.label_radio2 = QLabel("Radio 2:")
        self.input_radio2 = QLineEdit()
        self.input_radio2.setFixedWidth(100)

        self.label_base = QLabel("Base:")
        self.input_base = QLineEdit()
        self.input_base.setFixedWidth(100)

        self.label_altura = QLabel("Altura:")
        self.input_altura = QLineEdit()
        self.input_altura.setFixedWidth(100)

        left_layout.addWidget(self.label_radio1)
        left_layout.addWidget(self.input_radio1)
        left_layout.addWidget(self.label_radio2)
        left_layout.addWidget(self.input_radio2)
        left_layout.addWidget(self.label_base)
        left_layout.addWidget(self.input_base)
        left_layout.addWidget(self.label_altura)
        left_layout.addWidget(self.input_altura)

        self.label_carga = QLabel("Carga Eléctrica:")
        self.input_carga = QLineEdit()
        self.input_carga.setFixedWidth(100)

        left_layout.addWidget(self.label_carga)
        left_layout.addWidget(self.input_carga)

        self.label_coordenada_x = QLabel("Coordenada x:")
        self.input_coordenada_x = QLineEdit()
        self.input_coordenada_x.setFixedWidth(100)

        left_layout.addWidget(self.label_coordenada_x)
        left_layout.addWidget(self.input_coordenada_x)

        self.button_ingresar = QPushButton("Ingresar")
        self.button_ingresar.clicked.connect(self.ingresar_datos)

        left_layout.addWidget(self.button_ingresar)

        layout.addLayout(left_layout)  # Agregamos el layout izquierdo al layout principal

        # Right side layout
        self.graphics_view = QGraphicsView()  # Creamos el QGraphicsView
        self.scene = QGraphicsScene()  # Creamos la escena para el QGraphicsView
        self.graphics_view.setScene(self.scene)  # Asignamos la escena al QGraphicsView
        self.graphics_view.setMinimumWidth(300)  # Definimos el ancho mínimo del QGraphicsView

        layout.addWidget(self.graphics_view)  # Agregamos el QGraphicsView al layout principal

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.label_campo_electrico = QLabel("Campo eléctrico: N/A")
        self.label_campo_electrico.setAlignment(Qt.AlignCenter)  # Alineación del texto al centro
        layout.addWidget(self.label_campo_electrico)

        self.radio_cono.toggled.connect(self.toggle_campos_cono)
        self.radio_trono.toggled.connect(self.toggle_campos_trono)
        self.radio_hemisferio.toggled.connect(self.toggle_campos_hemisferio)
        
        self.draw_axes()
        self.enabledALL()  # Inicialmente deshabilitar campos
    def enabledALL(self):
        self.input_radio1.setEnabled(False)
        self.input_base.setEnabled(False)
        self.input_altura.setEnabled(False)
        self.input_radio2.setEnabled(False)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)


    def toggle_campos_cono(self):
        self.input_radio1.setEnabled(True)
        self.input_base.setEnabled(True)
        self.input_altura.setEnabled(True)
        self.input_radio2.setEnabled(False)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)
        if self.radio_cono.isChecked():
            self.cone_item = ConeItem()  # Crea una instancia del objeto de cono
            self.cone_item.setPos(self.graphics_view.width() / 2, self.graphics_view.height() / 2)  # Posición del cono en el centro
            self.scene.addItem(self.cone_item)  # Agrega el objeto de cono a la escena


    def toggle_campos_trono(self):
        self.input_radio1.setEnabled(True)
        self.input_radio2.setEnabled(False)
        self.input_base.setEnabled(False)
        self.input_altura.setEnabled(True)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)

    def toggle_campos_hemisferio(self):
        self.input_radio1.setEnabled(True)
        self.input_radio2.setEnabled(False)
        self.input_base.setEnabled(False)
        self.input_altura.setEnabled(False)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)
    
    def draw_axes(self):
        view_width = self.graphics_view.width()
        view_height = self.graphics_view.height()
        self.scene.addLine(view_width / 2, 0, view_width / 2, view_height, QPen(Qt.black))
        self.scene.addLine(0, view_height / 2, view_width, view_height / 2, QPen(Qt.black))

    def ingresar_datos(self):
        figura_seleccionada = ""
        radio1 = ""
        radio2 = ""
        base = ""
        altura = ""
        carga = ""
        coordenada_x = ""

        if self.radio_cono.isChecked():
            figura_seleccionada = "Cono"
            radio1 = self.input_radio1.text()
            base = self.input_base.text()
            altura = self.input_altura.text()
        elif self.radio_trono.isChecked():
            figura_seleccionada = "Trono de Cono"
            radio1 = self.input_radio1.text()
            altura = self.input_altura.text()
            radio2 = self.input_radio2.text()
        elif self.radio_hemisferio.isChecked():
            figura_seleccionada = "Hemisferio"
            radio1 = self.input_radio1.text()

        carga = self.input_carga.text()
        coordenada_x = self.input_coordenada_x.text()

        print("Figura seleccionada:", figura_seleccionada)
        print("Radio 1:", radio1)
        print("Radio 2:", radio2)
        print("Base:", base)
        print("Altura:", altura)
        print("Carga Eléctrica:", carga)
        print("Coordenada x:", coordenada_x)


app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
