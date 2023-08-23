# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 16:45:11 2023

@author: ceag0
"""

class Persona():
    def __init__(self):
        self.__nombre=""
        self.__cedula=0
        self.__gen=""
        
    #Setters
    def asignarNombre(self,nombre):
        self.__nombre= nombre
    def asignarCedula(self,cedula):
        self.__cedula= cedula
    def asignarGen(self,gen):
        self.__gen= gen
    
    #Getters
    def verNombre(self):
        return self.__nombre
    def verCedula(self):
        return self.__cedula
    def verGen(self):
        return self.__gen
    
    #Deleters
    def deleteNombre(self):
        del self.__nombre
    def deleteCedula(self):
        del self.__cedula
    def deleteGen(self):
        del self.__gen
        
class Paciente(Persona):
    def __init__(self):
        super().__init__()
        self.__servicio= ""
    def asignarServicio(self,serv):
        self.__servicio= serv
    def verServicio(self):
        return self.__servicio

class Trabajador_Hospital(Persona):
    def __init__(self):
        super().__init__()
        self.__turno=""
    def asignarTurno(self,turno):
        self.__turno= turno
    def verTurno(self):
        return self.__turno  
        
class Enfermera(Trabajador_Hospital):
    def __init__(self):
        super().__init__()
        self.__rango=""
    def asignarRango(self,ran):
        self.__rango= ran
    def verRango(self):
        return self.__rango

class Medico(Trabajador_Hospital):
    def __init__(self):
        super().__init__()
        self.__especialidad=""
    def asignarEspecialidad(self, esp):
        self.__especialidad=esp
    def verEspecialidad(self):
        return self.__especialidad
    
#Creando la clase sistema
class Sistema():
    def __init__(self):
        self.__lista_pacientes=[]
        self.__numero_pac= len(self.__lista_pacientes)
    def ingresarPaciente(self):
        
        #Validar que se ingrese un entero
        while True:
            try:
                cedula=int(input("No. de documento (sin puntos): "))
                break
            except ValueError:
                print("Ingrese solo numeros enteros")
        validar=""
        for p in self.__lista_pacientes:
            if cedula==p.verCedula():
                print("El numero de cédula ya se encuentra en el sistema")
                validar=True
        if validar!=True:
            nombre=input("Ingrese nombre: ")
            while True:
                gen=input("""Ingrese género:
                1. Masculino
                2. Femenino
                > """)
                if gen=="1":
                    gen= "Masculino"
                    break
                elif gen=="2":
                    gen="Femenino"
                    break
                else:
                    print("Ingrese una opción válida")
            servicio=input("Ingrese servicio: ")
            p=Paciente()
            p.asignarCedula(cedula)
            p.asignarNombre(nombre)
            p.asignarGen(gen)
            p.asignarServicio(servicio)
        
        #Se ingresa el paciente creado en la lista
        self.__lista_pacientes.append(p)
        
        #Actualizo el numero de pacientes
        self.__numero_pac=len(self.__lista_pacientes)
        
    def verNumeroPacientes(self):
        return self.__numero_pac
    
    def verDatosPaciente(self):
        validar=False
        while True:
            try:
                cedula=int(input("No. de documento (sin puntos): "))
                break
            except ValueError:
                print("Ingrese solo numeros enteros")
        for paciente in self.__lista_pacientes:
            if cedula==paciente.verCedula():
                validar=True
                break
            else:
                validar=False
        if validar==False:
            print("Paciente no encontrado en el sistema...")
        else:
            print("\nPaciente encontrado!")
            print(f"Nombre: {paciente.verNombre()}")
            print(f"Cédula: {paciente.verCedula()}")
            print(f"Género: {paciente.verGen()}")
            print(f"Servicio: {paciente.verServicio()}")
            
    

    