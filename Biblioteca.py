from datetime import date

class libros:
    #Constructor de la clase, donde representa el libro en el catalogo
    def __init__(self, titulo, autor, isbn, cantlib):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.cantlib = cantlib
        self.cantdispo = cantlib #La cantidad de libros disponibles es igual a los libros añadidos alprincipio
        print("Se ha registrado el libro: ", self.titulo)
   
    #Metodo para ver la informacion del libro
    def __str__(self):
        print("Titulo: ", self.titulo, ", Autor: ", self.autor, ", isbn: ", self.isbn, ", Cantidad disponible: ", self.cantdispo)
      
    
class usuarios:
    #Constructor de la clase, donde representa el usuario registrado
    def __init__(self, nombre, apellido, id):
        self.nombre=nombre
        self.apellido=apellido
        self.id=id
        print("Se ha registrado el usuario: ", self.nombre, self.apellido, "con el id: ", self.id)

    def __str__(self):
        print("Nombre: ", self.nombre, ", Apellido: ", self.apellido, ", ID: ", self.id)

class biblioteca: 
    """ 
    Clase principal del proyecto, donde se administra todo
    desde el catalogo de libros, usuarios, prestamos, devoluciones 
    """
    def __init__(self):
        self.catalogo = {} #Diccionario para almacenar los libros por ISBN
        self.usuarios = {} #Diccionario para almacenar los usuarios por ID
        self.lista_prestamos = [] #Lista para almacenar los prestamos realizados
        self.historial_devoluciones = [] #Lista para almacenar el historial de devoluciones

    #Metodo para registrar libros en el catalogo
    def registar_libros(self, titulo, autor, isbn, cantlib):
        if isbn in self.catalogo:
            print("El libro con ISBN ", isbn, " ya está registrado.")
        else:
            nuevo_libro = libros(titulo, autor, isbn, cantlib)
            self.catalogo[isbn] = nuevo_libro
            print("Libro: " , titulo, "registrado exitosamente. ")

    #Metodo para registrar usuarios
    def registrar_usuario(self, id, nombre, apellido):
        if id in self.usuarios:
            print("El usuario con ID ", id, " ya está registrado.")
        else:
            nuevo_usuario = usuarios(nombre, apellido, id)
            self.usuarios[id] = nuevo_usuario
            print("Usuario: ", nombre, apellido, "registrado exitosamente. ")

    #Metodo para realizar prestamos
    def realizar_prestamo(self, id_usuario, isbn_libro):
        if id_usuario not in self.usuarios: #Aqui validamos que el usuario exista
            print("El usuario con ID ", id_usuario, " no está registrado.")
            return

        if isbn_libro not in self.catalogo: #Aqui validamos que el libro exista
            print("El libro con ISBN ", isbn_libro, " no está registrado.")
            return

        libro = self.catalogo[isbn_libro] #Aqui obtenemos el libro del catalogo para validar su disponibilidad

        contador = sum(1 for p in self.lista_prestamos if p[0] == id_usuario)
        if contador >= 3:
            print("El usuario con ID ", id_usuario, " no puede tener más de 3 libros prestados al mismo tiempo.")
            return

        if libro.cantdispo > 0: #Aqui validamos que exista disponibilidad del libro, ya que la regla dice que no se puede 
                                #prestar un libro si no hay disponibilidad
            libro.cantdispo -= 1 #Si hay libros, se resta uno a la cantidad disponible
            print("Préstamo realizado: Usuario ID ", id_usuario, " ha prestado el libro ISBN ", isbn_libro)
        else:
            print("No hay disponibilidad del libro ISBN ", isbn_libro)
            return

        fecha = date.today() #Aqui se obtiene la fecha actual para registrar el prestamo
        nuevo_prestamo = (id_usuario, isbn_libro, fecha) #Aqui se crea una tupla con la informacion del prestamo
        self.lista_prestamos.append(nuevo_prestamo) #Aqui se agrega el prestamo a la lista de prestamos
        print("Préstamo registrado: Usuario ID ", id_usuario, " ha prestado el libro ISBN ", isbn_libro, " en la fecha ", fecha)


    #Metodo para realizar devoluciones
    def realizar_devolucion(self, id_usuario, isbn_libro):
        if id_usuario not in self.usuarios: #Aqui validamos que el usuario exista
            print("El usuario con ID ", id_usuario, " no está registrado.")
            return
        if isbn_libro not in self.catalogo: #Aqui validamos que el libro exista
            print("El libro con ISBN ", isbn_libro, " no está registrado.")
            return
        libro = self.catalogo[isbn_libro]
        libro.cantdispo += 1 #Cada vez que se realice una devolucion se suma uno a la cantidad de libros disponibles
        print("Devolución realizada: Usuario ID ", id_usuario, " ha devuelto el libro ISBN ", isbn_libro)
        fecha = date.today() #Aqui se obtiene la fecha actual para registrar la devolucion
        nuevo_historial = (id_usuario, isbn_libro, fecha) #Aqui se crea una tupla con la informacion de la devolucion
        self.historial_devoluciones.append(nuevo_historial) #Aqui se agrega la devolucion al historial de devoluciones
        print("Devolución registrada: Usuario ID ", id_usuario, " ha devuelto el libro ISBN ", isbn_libro, " en la fecha ", fecha)

        #Remover el prestamo de la lista de prestamos
        for p in self.lista_prestamos:
            if p[0] == id_usuario and p[1] == isbn_libro:
                self.lista_prestamos.remove(p)
                break

    #Top 3 libros más prestados
    def top_3_mas_prestados(self):
        resultado = top_3_mas_prestados(self.historial_devoluciones, self.catalogo)
        print("Top 3 libros más prestados:", resultado)

    #Listado de prestamos activos
    def prestamos_activos(self):
        resultado = prestamos_activos(self.lista_prestamos, self.catalogo, self.usuarios)
        print("Listado de préstamos activos:", resultado)

    #Buscar libros por autor
    def buscar_autor(self, autor):
        if autor in self.catalogo:
            resultado = buscar_autor(autor, self.catalogo)
            print(resultado)
        else:
            print("No se encontraron resultados para el autor: ", autor)

    #Buscar libros por titulo
    def buscar_titulo(self, titulo):
        if titulo in self.catalogo:
            resultado = buscar_titulo(titulo, self.catalogo)
            print( resultado)
        else:
            print("No se encontraron resultados para el título: ", titulo)

    
def main():
    print("Bienvenido a la Biblioteca del Tecnologico de Culiacan")
    print(""" 
Opcion 1: Registrar libro 
opcion 2: Registrar usuario 
opcion 3: Realizar préstamo 
opcion 4: Devolver libro 
opcion 5: Consultar disponibilidad de libros 
opcion 6: Consultar usuarios registrados 
opcion 7: Buscar por titulo 
opcion 8: Buscar por autor 
opcion 9: Consultar el top 3 de libros más prestados 
opcion 10: Mostrar el listado de prestamos activos 
opcion 11: Salir      
      """)
    b = biblioteca()
    while True:
        opcion = input("¿Que desea hacer dentro de la biblioteca?")
        if opcion == "1":
            print("Registrar libro")
            titulo = input("Ingrese el titulo del libro: ")
            autor = input("Ingrese el autor del libro: ")
            isbn = input("Ingrese el ISBN del libro: ")
            cantlib = int(input("Ingrese la cantidad de libros disponibles: "))
            if cantlib <= 0:
                print("La cantidad de libros debe ser mayor a cero.")
            else:
                print("Libro registrado exitosamente.")
                b.registar_libros(titulo, autor, isbn, cantlib)

        elif opcion == "2":
            print("Registrar usuario")
            nombre = input("Ingrese el nombre del usuario: ")
            apellido = input("Ingrese el apellido del usuario: ")
            id = input("Ingrese el ID del usuario: ")
            if id in b.usuarios:
                print("El usuario con ID ", id, " ya está registrado.")
            else:
                print("Usuario registrado exitosamente.")
                b.registrar_usuario(id, nombre, apellido)

        elif opcion == "3":
            print("Realizar préstamo")
            id_usuario = input("Ingrese el ID del usuario: ").strip
            isbn_libro = input("Ingrese el isbn dek libro: ").strip
            b.realizar_prestamo(id_usuario, isbn_libro)

        elif opcion == "4":
            print("Devolver libro")
            id_usuario = input("Ingrese el id del usuario: ").strip()
            isbn_libro = input("Ingrese el isbn del libro: ").strip()
            b.realizar_devolucion(id_usuario, isbn_libro)

        elif opcion == "5":
            print("Consultar disponibilidad de libros")
            b.consultar_disponibilidad()

        elif opcion == "6":
            print("Consultar usuarios registrados")
            b.consultar_usuarios()

        elif opcion == "7":
            print("Buscar por titulo")
            titulo = input("Ingrese el título del libro: ").strip()
            b.buscar_titulo(titulo)

        elif opcion == "8":
            print("Buscar por autor")
            autor = input("Ingrese el autor del libro: ").strip()
            b.buscar_autor(autor)

        elif opcion == "9":
            print("Consultar el top 3 de libros más prestados")
            b.top_3_mas_prestados()

        elif opcion == "10":
            print("Mostrar el listado de prestamos activos")
            b.prestamos_activos()

        elif opcion == "11":
            print("Esperamos verlo pronto, adios")
            break
        else: 
            print("Opcion no valida, ingrese una nueva")