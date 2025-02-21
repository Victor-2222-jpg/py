import json
from Array import Array

class Producto(Array):
    def __init__(self, id=None, nombre=None, precio=None, descripcion=None, categoria=None, cantidad=None):
        self.lista = all(param is None for param in [id, nombre, precio, descripcion, categoria, cantidad])
        if self.lista:
            super().__init__() 
        else:
            self.id = id
            self.nombre = nombre
            self.precio = precio
            self.descripcion = descripcion
            self.categoria = categoria
            self.cantidad = cantidad

    def dictionary(self):
        if self.lista:
            return [obj.dictionary() for obj in self.lista_objetos]
        else:
            
            return {
                "id": self.id,
                "nombre": self.nombre,
                "descripcion": self.descripcion,
                "precio": self.precio,
                "cantidad": self.cantidad,
                "categoria": self.categoria
            }
        
    def saveJson(self, archivo):
        datos = self.dictionary()
        with open(archivo, 'w') as file:
            json.dump(datos, file, indent=4)
        return True

    def castJson(self):
        return json.dumps(self.dictionary(), indent=4)
    
    def export(self):
        datos = self.saveJson()
        return datos
    
    def fromJson(self, archivo):
            try:
                with open(archivo, 'r') as file:
                    datos = json.load(file)
                return self.fromDictionary(datos)
            except Exception as e:
                return e
    
    def fromDictionary(self, datos): 
            try:
                if isinstance(datos, list):
                    self.lista = True
                    super().__init__()
                    for item in datos:
                        producto = Producto(item['id'], item['nombre'], item['precio'], item['descripcion'], item['categoria'], item['cantidad'])
                        self.save(producto)
                else:
                        self.lista = False
                        self.id = datos['id']
                        self.nombre = datos['nombre']
                        self.precio = datos['precio']
                        self.descripcion = datos['descripcion']
                        self.categoria = datos['categoria']
                        self.cantidad = datos['cantidad']

                return self
            except Exception as e:
                return e

    def showObject(self):
        for obj in self.lista_objetos:
            print(obj.dictionary())
        


        


if __name__ == "__main__":
    

  producto = Producto()
  producto.fromJson()
  producto.showObject()



"""
        class Producto(Array):
        # ...existing code...
    
        def fromJson(self, archivo='productos.json'):
            
            try:
                with open(archivo, 'r') as file:
                    datos = json.load(file)
                return self.fromDictionary(datos)
            except Exception as e:
                print(f"Error al leer JSON: {e}")
                return None
    
        def fromDictionary(self, datos):
            
            try:
                if isinstance(datos, list):
                    self.lista = True
                    super().__init__()
                    for item in datos:
                        producto = Producto()
                        producto.setData(item)
                        self.save(producto)
                    return self
                else:
                    return self.setData(datos)
            except Exception as e:
                print(f"Error al convertir datos: {e}")
                return None
    
        def setData(self, datos):

            self.id = datos.get('id')
            self.nombre = datos.get('nombre')
            self.precio = datos.get('precio')
            self.descripcion = datos.get('descripcion')
            self.categoria = datos.get('categoria')
            self.cantidad = datos.get('cantidad')
            self.lista = False
            return self
    
    
    
    
    
"""