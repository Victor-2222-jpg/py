
from venta import Venta
from producto import Producto
from interfazc import Interfazcliente
from interfazp import interfazproducto


class InterfazVenta():
    def __init__(self, ventas= None):
        if ventas is None:
            self.ventas = Venta()
            self.ventas = self.ventas.fromJson()
            self.Noguardar = False
        else:
            self.ventas = ventas
            self.Noguardar = True

    def Menu(self):
        while True:
            print("\n=== MENÚ DE VENTAS ===")
            print("1. Mostrar ventas")
            print("2. Realizar venta")
            print("3. Actualizar venta")
            print("4. Eliminar venta")
            print("5. Salir")
            
            opcion = input("\nSeleccione una opción (1-5): ")
            
            if opcion == "1":
                self.Show()
            elif opcion == "2":
                self.Insert()
            elif opcion == "3":
                self.Update()
            elif opcion == "4":
                self.Delete()
            elif opcion == "5":
                print("¡Gracias por su preferencia!")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def Insert(self):
        try:
            print("\n=== REALIZAR VENTA ===")
            id_venta = input("Ingrese indice de la venta: ")
    
            cliente = Interfazcliente().Insert()

            productos = interfazproducto(Producto()).Menu()
            total = input("Ingrese total: ")
            fecha = input("Ingrese fecha (YYYY-MM-DD): ")

            cantidad= float(input("Ingrese cantidad: "))
          
            nueva_venta = Venta(id_venta, cliente, productos, fecha, cantidad, total)
            
            if self.ventas.save(nueva_venta):
                self.InsertarDB(nueva_venta.dictionary())
                if not self.Noguardar:
                    self.ventas.saveJson()
                print(f"Venta realizada exitosamente")
                return nueva_venta  
            
            print("Error al guardar la venta.")
            return False
            
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def Show(self):
        print("\n=== LISTADO DE VENTAS ===")
        self.ventas.showObject()
        return True

    def Update(self):
        try:
            print("\n=== ACTUALIZAR VENTA ===")
            id_venta = input("Ingrese Indice de la venta a actualizar: ")
            
            indice = self.ventas.find(id_venta)
            if indice is not None:
                
                print("\n=== ACTUALIZAR CLIENTE ===")
                cliente = Interfazcliente().Insert()
                if not cliente:
                    print("Error al seleccionar cliente")
                    return False
                
                print("\n=== ACTUALIZAR PRODUCTOS ===")
                productos = interfazproducto(Producto()).Menu()
                if not productos:
                    print("Error al seleccionar productos")
                    return False
                
                fecha = input("Ingrese fecha (YYYY-MM-DD): ")   
                cantidad = float(input("Ingrese cantidad: "))
                total = float(input("Ingrese total: "))

                venta_actualizada = Venta(id_venta, cliente, productos, fecha, cantidad, total)
                if self.ventas.update(venta_actualizada, indice):
                    if not self.Noguardar:
                     self.ventas.saveJson()
                    print("Venta actualizada exitosamente")
                    return venta_actualizada
                else:
                    print("Error al actualizar la venta")
                    return False
            else:
                print("Venta no encontrada")
                return False
                
        except ValueError as e:
            print(f"Error: {e}")
            return False
    

    def Delete(self):
        print("\n=== ELIMINAR VENTA ===")
        id_venta = input("Ingrese el indice de la venta a eliminar: ")
        
        indice = self.ventas.find(id_venta)
        if indice is not None:
            if self.ventas.delete(indice):
                
                if not self.Noguardar:
                    self.ventas.saveJson()
                
                print("Venta eliminada exitosamente.")
                return True
            print("Error al eliminar la venta.")
            return False
        else:
            print("Venta no encontrada.")
            return False
        
    def InsertarDB(self, venta = None):
        coleccion = Venta().conexcionMongoDB("Ventas")
        resultado = coleccion.insert_one(venta)
        print(f"Documento insertado con ID: {resultado.inserted_id}")

if __name__ == "__main__":
    interfaz = InterfazVenta()
    interfaz.Menu()