import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QSlider, QGraphicsScene, QGraphicsView, QLabel, QDialog, QFileDialog, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pydicom
import os

class MyGraphCanvas(FigureCanvas):
    def __init__(self, parent, archivo, carpeta):
        super().__init__(Figure())
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)

        # Llama al método para mostrar la imagen en el widget
        self.mostrar_en_qt(archivo, carpeta)

    def mostrar_en_qt(self, archivo_dicom, carpeta):
        # Convierte el archivo DICOM a QImage
        ruta_completa = os.path.join(carpeta, archivo_dicom)
        imagen_dicom = pydicom.dcmread(ruta_completa)

        # Muestra la imagen usando Matplotlib
        self.ax.imshow(imagen_dicom.pixel_array, cmap='gray', aspect='auto')  # Ajusta la relación de aspecto
        self.ax.axis('off')
        self.ax.set_position([0, 0, 1, 1])  # Configura el objeto Axes para ocupar todo el espacio
        self.draw()

    def convertir_a_qimage(self, archivo_dicom):
        # Lee la imagen DICOM usando pydicom
        matriz_pixeles = archivo_dicom.pixel_array

        # Normaliza la matriz de píxeles (0 a 255)
        matriz_normalizada = ((matriz_pixeles - matriz_pixeles.min()) / (matriz_pixeles.max() - matriz_pixeles.min()) * 255).astype('uint8')

        # Crea un objeto QImage desde la matriz de píxeles
        height, width = matriz_normalizada.shape
        qimage = QImage(matriz_normalizada.data, width, height, QImage.Format_Grayscale8)

        return qimage

class VentanaLogin(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_login.ui",self)
        self.setup()

    
    def setup(self):
        self.buttonBox.accepted.connect(self.opcion_aceptar)
        self.buttonBox.rejected.connect(self.opcion_rechazar)
        
    
        
    def opcion_aceptar(self):
        usuario= self.campo_usuario.text()
        password= self.campo_pass.text()
        validacion= self.__controlador.validar_login(usuario,password)
        
        if validacion:
            text="Bienvenido al programa! \nPor favor seleccione la carpeta con imagenes DICOM"
            message= QMessageBox.information(self, "Login", text, QMessageBox.Ok)
            
            #Abrimos la ventana de imagenes si se autentica el usuario
            self.abrir_ventana_imagenes()
            self.campo_usuario.setText("")
            self.campo_pass.setText("")
            
            
        else:
            text="¡Datos de acceso incorrectos!"
            message= QMessageBox.warning(self, "Alerta!", text, QMessageBox.Ok)
    def opcion_rechazar(self):
        self.campo_usuario.setText("")
        self.campo_pass.setText("")
    
    def setControlador(self,c):
        self.__controlador= c
        
    def abrir_ventana_imagenes(self):
        carpeta=QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta", "/ruta/inicial")
        archivos_dicom = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.dcm')]
        
        # Verifica si hay archivos DICOM en la carpeta
        if not archivos_dicom:
            text="¡No se encontraron archivos .dcm en la ruta especificada!"
            message= QMessageBox.critical(self, "Alerta!", text, QMessageBox.Ok)
        else:
            v_img=VentanaImagen(archivos_dicom,carpeta, self)
            self.hide()
            v_img.show()

class VentanaImagen(QDialog):
    def __init__(self, archivos, carpeta, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_imagenes.ui", self)
        self.__ventanaPadre = ppal
        self.archivos = archivos
        self.carpeta = carpeta
        self.setup()
        self.valor_actual.setText("1")
    def setup(self):
        self.cerrar_sesion.clicked.connect(self.mostrar_inicio)
        self.slider.setMinimum(1)
        self.slider.setMaximum(len(self.archivos))
        self.slider.setValue(1)
        self.slider.valueChanged.connect(self.actualizar_grafica)
        self.slider.valueChanged.connect(self.ver_valor)
        
        self.valor_maximo.setText(str(len(self.archivos)))
        layout = QVBoxLayout()
        self.imagen_dcm.setLayout(layout)
        self.grafico = MyGraphCanvas(self.imagen_dcm, self.archivos[0], self.carpeta)
        layout.addWidget(self.grafico)
        
        #Abre ventana de información 
        self.info_im.clicked.connect(self.abrir_info)
    
    def mostrar_inicio (self):
        text= "Sesión cerrada con éxito \n¡Hasta pronto!"
        message= QMessageBox.information(self, "Log out", text, QMessageBox.Ok)
        self.close()
        self.__ventanaPadre.show()
    def ver_valor(self):
        self.valor_actual.setText(str(self.slider.value()))
        
    def actualizar_grafica(self):
        indice = self.slider.value()
        self.grafico.mostrar_en_qt(self.archivos[indice - 1], self.carpeta)
    def abrir_info(self):
        v_info=VentanaInfo_img(self.archivos,self.carpeta,self.slider.value(), self)
        v_info.show()
        
class VentanaInfo_img(QDialog):
    def __init__(self, archivos,carpeta, indice, ppal=None):
        super().__init__(ppal)
        loadUi("ventana_info.ui",self)
        self.indice=indice
        self.archivos=archivos
        self.carpeta=carpeta
        self.setup()
        
    def setup(self):
        self.regresar.clicked.connect(self.close)
        self.mode.setText(self.info("Modality"))
        self.body_part.setText(self.info("BodyPartExamined"))
        self.pat_sex.setText(self.info("PatientSex"))
        self.peso_pac.setText(str(self.info("PatientWeight")) + " Kg")
        self.date.setText(f'{str(self.info("AcquisitionDate"))[:4]}/ {str(self.info("AcquisitionDate"))[4:6]}/ {str(self.info("AcquisitionDate"))[6:]}')
    
    def info(self,caracteristica):
        imagen_dicom = pydicom.dcmread(os.path.join(self.carpeta, self.archivos[self.indice-1]))
        return getattr(imagen_dicom, caracteristica, "No existe")
        
    
        ### VER EN VIDEO COMO VUELVE A RECUPERAR LAS PESTAÑAS HIDE"
        
        
        
        
        
        
        
        
