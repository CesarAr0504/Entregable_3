# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 00:27:19 2023

@author: ceag0
"""
from Clases_Practica_POO import *
    
def main():
    #Creamos el objeto sistema
    MySistem=Sistema()
    
    while True:
        menu=input("""\nIngrese una de las opciones:
        1. Ingresar un paciente
        2. Ver información de un paciente
        3. Número de pacientes almacenados en el sistema
        4. Salir
        > """)
        if menu=="1":
            MySistem.ingresarPaciente()
            print("Paciente ingresado con éxito")
        elif menu=="2":
            MySistem.verDatosPaciente()
        elif menu=="3":
            print(f"Hay {MySistem.verNumeroPacientes()} paciente(s) en el sistema")
        elif menu=="4":
            print("Hasta pronto!")
            break
        else:
            print("Ingrese una opción válida")
if __name__ == "__main__":
    main()