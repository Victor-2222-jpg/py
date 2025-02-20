from cliente import Cliente
import cliente

class Interfazcliente():
    def __init__(self, cliente = None):
        if cliente is None:
            self.clientes = Cliente()  
            self.clientes = self.clientes.fromJson()
            self.Noguardar = False 
        else:
            self.clientes = cliente
            self.Noguardar = True

    def Menu(self):
        while True:
            print("\n=== MENÚ DE CLIENTES ===")
            print("1. Mostrar clientes")
            print("2. Insertar cliente")
            print("3. Actualizar cliente")
            print("4. Eliminar cliente")
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
                return self.clientes
            else:
                print("Opción no válida. Intente nuevamente.")

    def Insert(self):
        print("\n=== INSERTAR CLIENTE ===")
        try:
            id = input("Ingrese ID del cliente: ")
            nombre = input("Ingrese nombre del cliente: ")
            email = input("Ingrese email del cliente: ")
            telefono = input("Ingrese teléfono del cliente: ")
            direccion = input("Ingrese dirección del cliente: ")
            tipo_persona = input("Ingrese tipo de persona (Fisica/Moral): ")
            
            nuevo_cliente = Cliente(id, nombre, email, telefono, direccion, tipo_persona)
            if self.clientes.save(nuevo_cliente):
                print("Cliente agregado exitosamente.")
                
                if not self.Noguardar:
                    self.InsertarDB(nuevo_cliente.dictionary())
                    self.clientes.saveJson()
                return nuevo_cliente
            print("Error al guardar el cliente.")
            return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def Show(self):
        print("\n=== LISTADO DE CLIENTES ===")
        self.clientes.showObject()
        return True

    def Update(self):
        print("\n=== ACTUALIZAR CLIENTE ===")
        id = input("Ingrese ID del cliente a actualizar: ")
        
        indice = self.clientes.find(id)
        if indice is not None:
            try:
                nombre = input("Nuevo nombre del cliente: ")
                email = input("Nuevo email del cliente: ")
                telefono = input("Nuevo teléfono del cliente: ")
                direccion = input("Nueva dirección del cliente: ")
                tipo_persona = input("Nuevo tipo de persona (Fisica/Moral): ")
                
                nuevo_cliente = Cliente(id, nombre, email, telefono, direccion, tipo_persona)
                if self.clientes.update(nuevo_cliente, indice):
                    if not self.Noguardar:
                        self.clientes.saveJson()
                    print("Cliente actualizado exitosamente.")
                    return nuevo_cliente
                print("Error al actualizar el cliente.")
                return False
            except ValueError as e:
                print(f"Error: {e}")
                return False
        else:
            print("Cliente no encontrado.")
            return False

    def Delete(self):
        print("\n=== ELIMINAR CLIENTE ===")
        id = input("Ingrese el indice del cliente a eliminar: ")
        
        indice = self.clientes.find(id)
        if indice is not None:
            if self.clientes.delete(indice):
                if not self.Noguardar:
                    self.clientes.saveJson()
                print("Cliente eliminado exitosamente.")
                return True
            print("Error al eliminar el cliente.")
            return False
        else:
            print("Cliente no encontrado.")
            return False
        
    def InsertarDB(self, cliente = None):
        coleccion = Cliente().conexcionMongoDB("Clientes")
        resultado = coleccion.insert_one(cliente)
        print(f"Documento insertado con ID: {resultado.inserted_id}")

if __name__ == "__main__":
    interfaz = Interfazcliente()
    interfaz.Menu()