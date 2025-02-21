from producto import Producto

class interfazproducto():
    def __init__(self, producto = None):
        if producto is None:
            self.productos = Producto()  
            self.productos = self.productos.fromJson('productos.json')
            self.productos_respaldo = Producto().fromJson('productoRespaldo.json')
            self.Noguardar = False 
        else:
            self.productos = producto
            self.Noguardar = True

    def Menu(self):
        while True:
            print("\n=== MENÚ DE PRODUCTOS ===")
            print("1. Mostrar productos")
            print("2. Insertar producto")
            print("3. Actualizar producto")
            print("4. Eliminar producto")
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
                print("¡Vuelva pronto!")
                return self.productos 
            else:
                print("Opción no válida. Intente nuevamente.")

    def Insert(self):
        print("\n=== INSERTAR PRODUCTO ===")
        try:
            id = input("Ingrese ID del producto: ")
            nombre = input("Ingrese nombre del producto: ")
            precio = float(input("Ingrese precio del producto: "))
            descripcion = input("Ingrese descripción del producto: ")
            categoria = input("Ingrese categoría del producto: ")
            cantidad = int(input("Ingrese cantidad en stock: "))
            
            nuevo_producto = Producto(id, nombre, precio, descripcion, categoria, cantidad)
            if self.productos.save(nuevo_producto):
                print("Producto agregado exitosamente.")
                
                if not self.Noguardar: 
                    self.productos.saveJson('productos.json')
                    if(self.productos.check_internet()):
                        self.InsertarDB(nuevo_producto.dictionary())
                        self.procesarProductosRespaldo()
                        print("Conexión a internet establecida")
                    else:
                        self.productos_respaldo.save(nuevo_producto)
                        nuevo_producto.dictionary()
                        self.productos_respaldo.saveJson('productoRespaldo.json')
            else:
                print("Error al guardar el producto.")
        except ValueError:
            print("Error: Asegúrese de ingresar valores numéricos válidos para precio y cantidad.")

    def Show(self):
        print("\n=== LISTADO DE PRODUCTOS ===")
        self.productos.showObject()

    def Update(self):
        print("\n=== ACTUALIZAR PRODUCTO ===")
        id = input("Ingrese indice del producto a actualizar: ")
        
        indice = self.productos.find(id)
        if indice is not None:
            try:
                nombre = input("Nuevo nombre del producto: ")
                precio = float(input("Nuevo precio del producto: "))
                descripcion = input("Nueva descripción del producto: ")
                categoria = input("Nueva categoría del producto: ")
                cantidad = int(input("Nueva cantidad en stock: "))
                
                nuevo_producto = Producto(id, nombre, precio, descripcion, categoria, cantidad)
                if self.productos.update(nuevo_producto, indice):
                    if not self.Noguardar: 
                        self.productos.saveJson()
                    print("Producto actualizado exitosamente.")
                else:
                    print("Error al actualizar el producto.")
            except ValueError:
                print("Error: Asegúrese de ingresar valores numéricos válidos para precio y cantidad.")
        else:
            print("Producto no encontrado.")

    def Delete(self):
        print("\n=== ELIMINAR PRODUCTO ===")
        id = input("Ingrese ID del producto a eliminar: ")
        
        indice = self.productos.find(id)
        if indice is not None:
            if self.productos.delete(indice):
                if not self.Noguardar:  
                    self.productos.saveJson()
                print("Producto eliminado exitosamente.")
            else:
                print("Error al eliminar el producto.")
        else:
            print("Producto no encontrado.")

    def InsertarDB(self, producto = None):
        coleccion = Producto().conexcionMongoDB("Productos")
        resultado = coleccion.insert_one(producto)
        print(f"Documento insertado con ID: {resultado.inserted_id}")


    def procesarProductosRespaldo(self):
        print("Procesando productos del respaldo...")
        for producto in self.productos_respaldo.lista_objetos:
            self.InsertarDB(producto.dictionary())
        self.productos_respaldo = Producto()
        self.productos_respaldo.saveJson('productoRespaldo.json')
        print("Productos del respaldo procesados y enviados a la base de datos")


    
if __name__ == "__main__":
    interfaz = interfazproducto()
    interfaz.Menu()