

class Login:
    def __init__(self):
        self.__usuario = "medicoAnalitico"
        self.__password = "bio12345"
        
    def set_usuario(self, u):
        self.__usuario = u
    
    def set_password(self, p):
        self.__password = p
    
    def validar_login(self, u, p):
        return (self.__usuario == u) and (self.__password == p)


