import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QRadioButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton,QHBoxLayout, QWidget, QGraphicsView, QGraphicsScene,QGraphicsItem
from PyQt5.QtGui import QPen, QColor, QPainterPath, QPainter, QBrush
from PyQt5.QtCore import Qt, QRectF
from sympy import integrate, init_printing
import sympy as sp
import numpy as np
init_printing(use_latex="mathjax")
import math
from math import pi

class SemiCircleItem(QGraphicsItem):
    def __init__(self):
        super().__init__()
        self.setFlag(self.ItemIsSelectable)
        self.setFlag(self.ItemIsMovable)

    def boundingRect(self):
        return QRectF(-50, -50, 100, 100)  # Define the bounding rectangle of the semicircle

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.black))
        painter.setBrush(QBrush(Qt.green))
        path = QPainterPath()
        path.moveTo(50, 0)  # Mover a la posición inicial del arco
        path.arcTo(0, -50, 100, 100, 90, 180)  # Dibuja el semicírculo de 90 a 270 grados
        painter.drawPath(path)
        
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

class SectionConeItem(QGraphicsItem):
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
        path.moveTo(-50, -20)  # Punto central del cono
        path.lineTo(50, -50)  # Punto derecho
        path.lineTo(50, 50)  # Punto izquierdo
        path.lineTo(-50, 20)  # Volver al punto central para cerrar el cono
        painter.drawPath(path)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 919, 519)
        self.setWindowTitle("Calculadora de campos electromagneticos")

        layout = QHBoxLayout() 

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


        self.label_altura = QLabel("Altura:")
        self.input_altura = QLineEdit()
        self.input_altura.setFixedWidth(100)

        left_layout.addWidget(self.label_radio1)
        left_layout.addWidget(self.input_radio1)
        left_layout.addWidget(self.label_radio2)
        left_layout.addWidget(self.input_radio2)
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

        self.button_limpiar = QPushButton("Limpiar")
        self.button_limpiar.clicked.connect(self.limpiar_datos)

        left_layout.addWidget(self.button_ingresar)
        left_layout.addWidget(self.button_limpiar)

        layout.addLayout(left_layout)  

        # Right side layout
        self.graphics_view = QGraphicsView()  
        self.scene = QGraphicsScene()  
        self.graphics_view.setScene(self.scene)  
        self.graphics_view.setMinimumWidth(300)  

        layout.addWidget(self.graphics_view) 

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.label_campo_electrico = QLabel("Campo eléctrico: N/A")
        self.label_campo_electrico.setAlignment(Qt.AlignCenter)  
        layout.addWidget(self.label_campo_electrico)

        self.radio_cono.toggled.connect(self.toggle_campos_cono)
        self.radio_trono.toggled.connect(self.toggle_campos_trono)
        self.radio_hemisferio.toggled.connect(self.toggle_campos_hemisferio)
        
        self.draw_axes()
        self.enabledALL() 
        
    def limpiar_datos(self):
        self.scene.clear()
        self.input_altura.clear()
        self.input_carga.clear()
        self.input_coordenada_x.clear()
        self.input_radio1.clear()
        self.input_radio2.clear()
        self.label_campo_electrico.setText("Campo Electrico: N/A")
        self.draw_axes()
        print("A")

    def enabledALL(self):
        self.input_radio1.setEnabled(False)
        self.input_altura.setEnabled(False)
        self.input_radio2.setEnabled(False)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)


    def toggle_campos_cono(self):
        self.input_radio1.setEnabled(True)
        self.input_altura.setEnabled(True)
        self.input_radio2.setEnabled(False)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)
        if self.radio_cono.isChecked():
            self.cone_item = ConeItem()  
            self.cone_item.setPos(self.graphics_view.width() / 2, self.graphics_view.height() / 2)  # Posición del cono en el centro
            self.scene.addItem(self.cone_item) 


    def toggle_campos_trono(self):
        self.input_radio1.setEnabled(True)
        self.input_radio2.setEnabled(True)
        self.input_altura.setEnabled(True)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)
        if self.radio_trono.isChecked():
            self.cone_item = SectionConeItem()  
            self.cone_item.setPos(self.graphics_view.width() / 2, self.graphics_view.height() / 2)  # Posición del cono en el centro
            self.scene.addItem(self.cone_item) 

    def toggle_campos_hemisferio(self):
        self.input_radio1.setEnabled(True)
        self.input_radio2.setEnabled(False)
        self.input_altura.setEnabled(False)
        self.input_carga.setEnabled(True)
        self.input_coordenada_x.setEnabled(True)
        if self.radio_hemisferio.isChecked():
            self.cone_item = SemiCircleItem()
            self.cone_item.setPos(self.graphics_view.width() / 2, self.graphics_view.height() / 2)  # Posición del cono en el centro
            self.scene.addItem(self.cone_item) 
    
    def draw_axes(self):
        view_width = self.graphics_view.width()
        view_height = self.graphics_view.height()
        self.scene.addLine(view_width / 2, 0, view_width / 2, view_height, QPen(Qt.black))
        self.scene.addLine(0, view_height / 2, view_width, view_height / 2, QPen(Qt.black))

    def draw_line(self,x,long):
        view_width = self.graphics_view.width()
        view_height = self.graphics_view.height()
        self.scene.addLine(((view_width / 2) + x) * 1.2, view_height / 2, (view_width / 2) + long, view_height / 2, QPen(Qt.red))

    def ingresar_datos(self):
        figura_seleccionada = ""
        radio1 = ""
        radio2 = ""
        altura = ""
        carga = ""
        coordenada_x = ""
        carga = self.input_carga.text()
        coordenada_x = self.input_coordenada_x.text()
        if self.radio_cono.isChecked():
            figura_seleccionada = "Cono"
            radio1 = self.input_radio1.text()
            altura = self.input_altura.text()
            campoElectrico = CampoCono(radio1,altura,carga,coordenada_x)
            campoFormato = format(campoElectrico, '.1E')
            nuevoCampo = "Campo electrico: " + str(campoFormato) + " N/C"  # Cambia esto por el nuevo texto que desees
            self.label_campo_electrico.setText(nuevoCampo)
            longX = campoElectrico / 100000
            self.draw_line(int(coordenada_x),longX)
        elif self.radio_trono.isChecked():
            figura_seleccionada = "Trozo de Cono"
            radio1 = self.input_radio1.text()
            altura = self.input_altura.text()
            radio2 = self.input_radio2.text()
            campoElectrico = CampoTrozo(radio1, radio2, altura, coordenada_x, carga)
            campoFormato = format(campoElectrico, '.1E')
            nuevoCampo = "Campo electrico: " + str(campoFormato) + " N/C"  # Cambia esto por el nuevo texto que desees
            self.label_campo_electrico.setText(nuevoCampo)
            longX = campoElectrico / 100000
            self.draw_line(int(coordenada_x),longX)
        elif self.radio_hemisferio.isChecked():
            figura_seleccionada = "Hemisferio"
            radio1 = self.input_radio1.text()
            campoElectrico = CampoHemisferio(radio1, coordenada_x, carga)
            campoFormato = format(campoElectrico, '.1E')
            nuevoCampo = "Campo electrico: " + str(campoFormato) + " N/C"  # Cambia esto por el nuevo texto que desees
            self.label_campo_electrico.setText(nuevoCampo)
            longX = campoElectrico / 100000
            self.draw_line(int(coordenada_x),longX)

        


#Funciones para calcular


def CampoCono(radio_, altura_, carga_, distancia_):
    radio = int(radio_)
    altura = int(altura_)
    carga = int(carga_)
    distancia = int(distancia_)
    x = sp.Symbol('x')
    funcionCono = 1 - (
        (altura - x + distancia) / (
            sp.sqrt(
                ((altura - x + distancia) ** 2) +
                ((radio - ((radio * x) / altura)) ** 2)
            )
        )
    )
    integralCono = sp.integrate(funcionCono, (x, 0, altura))
    E_Cono = ((3 * carga) / (2 * sp.pi * 8.85E-12 * (radio ** 2) * altura)) * integralCono

    resultado_numericoCono = E_Cono.evalf()
    """ resultado_numericoCono = format(resultado_numericoCono, '.1E') """

    return resultado_numericoCono

def CampoTrozo(radio1_, radio2_, altura_, distancia_, carga_):
    radio1 = int(radio1_)
    radio2 = int(radio2_)
    altura = int(altura_)
    distancia = int(distancia_)
    carga = int(carga_)
    
    x = sp.Symbol('x')
    
    funcionTrozo = 1 - (
        (-altura - x + distancia) / (
            sp.sqrt(
                ((altura - x + distancia) ** 2) +
                ((((radio2-radio1)/altura)*x)+radio1) ** 2
            )
        )
    )
    
    integralTrozo = sp.integrate(funcionTrozo, (x, 0, altura))
    E_Trozo = ((3 * carga) / (2 * sp.pi * 8.85E-12 * ((radio1 ** 2) + (radio2**2) + radio1*radio2) * altura)) * integralTrozo

    resultado_numericoTrozo = E_Trozo.evalf()
    """ resultado_numericoTrozo = format(resultado_numericoTrozo, '.1E') """
    
    if radio2 <= radio1:
        resultado_numeroTrozo = 0
    
    return resultado_numericoTrozo

def CampoHemisferio(radio1_, distancia_, carga_):
    radio = int(radio1_)
    distancia = int(distancia_)
    carga = int(carga_)

    x = sp.Symbol('x')

    funcionHemisferio = 1 - (
        (radio - x + distancia) / (
            sp.sqrt(
                ((radio - x + distancia) ** 2) +
                ((radio**2)-((x-radio)**2))
            )
        )
    )
    
    integralHemisferio = sp.integrate(funcionHemisferio, (x, 0, radio))
    E_Hemisferio = ((3 * carga) / (4 * sp.pi * 8.85E-12 * (radio**3))) * integralHemisferio

    resultado_numericoHemisferio = E_Hemisferio.evalf()    
    return resultado_numericoHemisferio

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
