from Modelo_e import *
from Vista_e import *
from PyQt5.QtWidgets import QApplication   #medicoAnalitico
import sys 

class Coordinador:    
    def __init__(self, vista, modelo):
        self.__mi_vista= vista
        self.__mi_modelo= modelo
    
    def validar_login(self, u,p):
        return self.__mi_modelo.validar_login(u,p)
        

#Codigo cliente
def main():
    app= QApplication(sys.argv)
    vista= VentanaLogin()
    modelo= Login()    
    coordinador= Coordinador(vista, modelo)
    vista.setControlador(coordinador)
    vista.show()
    sys.exit(app.exec_())

    

if __name__== "__main__":
    main()