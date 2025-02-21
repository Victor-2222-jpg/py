from cliente import Cliente
import cliente

class Interfazcliente():
    def __init__(self, cliente = None):
        if cliente is None:
            self.clientes = Cliente()  
            self.clientes = self.clientes.fromJson('clientes.json')
            self.clientes_respaldo = Cliente().fromJson('ClientesRespaldo.json')

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
                    self.clientes.saveJson('clientes.json')
                    if(self.clientes.check_internet()):
                        self.InsertarDB(nuevo_cliente.dictionary())
                        self.procesarClientesRespaldo()
                        print("Conexión a internet establecida")
                    else:
                        self.clientes_respaldo.save(nuevo_cliente)
                        nuevo_cliente.dictionary()
                        self.clientes_respaldo.saveJson('ClientesRespaldo.json')
                    
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
    
    def procesarClientesRespaldo(self):
        print("Procesando clientes del respaldo...")
        for cliente in self.clientes_respaldo.lista_objetos:
            self.InsertarDB(cliente.dictionary())
        self.clientes_respaldo = Cliente()
        self.clientes_respaldo.saveJson('ClientesRespaldo.json')
        print("Clientes del respaldo procesados y enviados a la base de datos")

if __name__ == "__main__":
    interfaz = Interfazcliente()
    interfaz.Menu()