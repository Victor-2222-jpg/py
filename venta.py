import json
from Array import Array
from cliente import Cliente
from producto import Producto
import os

class Venta(Array):
    def __init__(self, id=None, cliente=None, productos=None, fecha=None, cantidad=None, total=None):
        self.lista = not any([id, cliente, productos, fecha, cantidad, total])
        if not self.lista:
            self.id = id
            self.cliente = cliente
            self.productos = productos
            self.fecha = fecha
            self.cantidad = cantidad
            self.total = total
        else:
            super().__init__()

    def dictionary(self):
        if self.lista:
            return [obj.dictionary() for obj in self.lista_objetos]
        else:
            return {
                "id": self.id,
                "cliente": self.cliente.dictionary(),
                "productos": self.productos.dictionary(),
                "fecha": self.fecha,
                "cantidad": self.cantidad,
                "total": self.total
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

       
    
    def ReadJson(self, archivo):
        try:
            if os.path.exists(archivo):
                with open(archivo, 'r') as file:
                    datos = json.load(file)
                    if not isinstance(datos, list):
                        datos = [datos]
                return datos
            else:
                return None
        except Exception as e:
            return None
    
    def fromJson(self, archivo):
        datos = self.ReadJson(archivo)
        if datos:
            return self.fromDictionary(datos)
        return None

    def fromDictionary(self, json_datos):
        if isinstance(json_datos, list):
            self.lista_objetos = []
            for dato in json_datos:
                self.lista_objetos.append(self.fromDictionary(dato))
            return self
        else:
            cliente = Cliente().fromDictionary(json_datos['cliente'])
            productos = Producto().fromDictionary(json_datos['productos'])
            obj = Venta(
                json_datos['id'],
                cliente,
                productos,
                json_datos['fecha'],
                json_datos['cantidad'],
                json_datos['total']
            )
            return obj

    def showObject(self):
        try:
            print("\nVentas:")
            for venta in self.lista_objetos:
                print(venta.dictionary())
        except Exception as e:
            print(f"Error: {e}")
        
          
 
    
    
    

if __name__ == "__main__":
  
   
   miVenta = Venta()
   miVenta.fromJson()
   miVenta.showObject()



   """
    producto1 = Producto(1, "Leche", 25, "Lala 100", "lacteos", 1)
    producto2 = Producto(2, "Emperador", 16, "Galleta de chocolate", "Abarrotes", 2)
    producto3 = Producto(3, "Coca Cola", 15, "Refresco de cola", "Bebidas", 3)
    producto4 = Producto(4, "Papas", 10, "Papas fritas", "Abarrotes", 4)

    contenedor= Producto()
    contenedor.save(producto1)
    contenedor.save(producto2)

    contenedor2= Producto()
    contenedor2.save(producto3)
    contenedor2.save(producto4)

    
    
    cliente = Cliente(1, "Raul Medina", "raul12@email.com", "555-1234", "Calle 123", "Regular")
    
    
    venta1 = Venta(1, cliente, contenedor, "2024-03-20", 1, 15000)
    venta2 = Venta(2, cliente, contenedor2, "2024-03-21", 2, 15500)

    
    print("\nVenta individual en JSON:")
    print(venta1.castJson())

    
    gestor = Venta()
    gestor.save(venta1)
    gestor.save(venta2)

   
    indice = gestor.find(2)
    
   
    gestor.delete(0)

   
    print("\nArray en JSON:")
    print(gestor.export())
    """