from pymongo import MongoClient
import socket

class Array:
    def __init__(self, id=None):
        self.lista = True
        if self.lista:
            self.lista_objetos = []
        else:
            self.id = id

    def __str__(self):
        if self.lista:
            return f'Lista con {len(self.lista_objetos)} elementos'
        return f'ID: {self.id}'

    def save(self, objeto):
        if isinstance(objeto, type(self)):
            self.lista_objetos.append(objeto)
            return True
        return False

    def find(self, id_objeto):
        for i, objeto in enumerate(self.lista_objetos):
            if objeto.id == id_objeto:
                return i
        return None

    def delete(self, indice):
        if 0 <= indice < len(self.lista_objetos):
            eliminado = self.lista_objetos[indice]
            del self.lista_objetos[indice]
            return eliminado
        return None

    def update(self, nuevo_objeto, indice=None):
        if indice is None:
            return nuevo_objeto
        if 0 <= indice < len(self.lista_objetos):
            self.lista_objetos[indice] = nuevo_objeto
            return nuevo_objeto
        return None
    
    def conexcionMongoDB(self,Coleccion):
        client = MongoClient("mongodb+srv://myAtlasDBUser:vmx123@myatlasclusteredu.eymom.mongodb.net/")
        db = client["PythonEjercico"]
        coleccion = db[Coleccion]
        return coleccion
    
    def check_internet(self, host="8.8.8.8", port=53, timeout=3):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error:
            return False

    