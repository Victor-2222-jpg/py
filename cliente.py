import json
from Array import Array

class Cliente(Array):
    def __init__(self, id=None, nombre=None, email=None, telefono=None, direccion=None, tipo_persona=None):
        self.lista = all(param is None for param in [id, nombre, email, telefono, direccion, tipo_persona])
        if self.lista:
            super().__init__()
        else:
            self.id = id
            self.nombre = nombre
            self.email = email
            self.telefono = telefono
            self.direccion = direccion
            self.tipo_persona = tipo_persona

    def dictionary(self):
        if self.lista:
            return [obj.dictionary() for obj in self.lista_objetos]
        else:
            return {
                "id": self.id,
                "nombre": self.nombre,
                "email": self.email,
                "telefono": self.telefono,
                "direccion": self.direccion,
                "tipo_persona": self.tipo_persona
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
                        cliente = Cliente(item['id'], item['nombre'], item['email'], item['telefono'], item['direccion'], item['tipo_persona'])
                        self.save(cliente)
                else:
                    self.lista = False
                    self.id = datos['id']
                    self.nombre = datos['nombre']
                    self.email = datos['email']
                    self.telefono = datos['telefono']
                    self.direccion = datos['direccion']
                    self.tipo_persona = datos['tipo_persona']
                return self
            except Exception as e:
                return e
    
    def showObject(self):
        print("\nClientes")
        for cliente in self.lista_objetos:
            print(cliente.dictionary())



if __name__ == "__main__":
 
 cliente=Cliente()
 cliente.fromJson()
 cliente.showObject()

 """"
    cliente1 = Cliente(1, "Mateo Chavez", "juan@email.com", "555-1234", "Calle 123", "Regular")
    cliente2 = Cliente(2, "Maria Lopez", "maria@email.com", "555-5678", "Av Principal", "VIP")
    cliente3 = Cliente(3, "Carlos Frausto", "carlos@email.com", "555-9012", "Plaza Central", "Regular")

    
    print("\nCliente individual en JSON:")
    print(cliente1.castJson())

    
    gestor = Cliente()
    gestor.save(cliente1)
    gestor.save(cliente2)
    gestor.save(cliente3)

    
    indice = gestor.find(2)
    if indice is not None:
        cliente_nuevo = Cliente(2, "Mariana Hernandez", "mariana@email.com", "555-8765", "Nueva Dirección", "Premium")
        gestor.update(cliente_nuevo, indice)

    


    print("\nArray en JSON:")
    print(gestor.export()) 
"""