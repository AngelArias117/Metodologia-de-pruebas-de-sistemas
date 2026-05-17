# Sistema de compras

# Modulos:
# - Registro de usuarios
# - Carrito de compras
# - Pagos
# - Envios


class Usuario:

    def __init__(self, mail, nombre):
        self.mail = mail
        self.nombre = nombre
        self.registrado = False

    def registrar_usuario(self):
        self.registrado = True
        print(f"Usuario {self.nombre} registrado correctamente")


class Carrito:

    def __init__(self, usuario):
        self.usuario = usuario
        self.productos = []

    def agregar_producto(self, producto):

        if self.usuario.registrado:
            self.productos.append(producto)
            print(f"Producto '{producto}' agregado al carrito")
        else:
            print("El usuario no está registrado")


class Pago:

    def __init__(self, carrito):
        self.carrito = carrito
        self.pagado = False

    def procesar_pago(self):

        if self.carrito.usuario.registrado:
            if len(self.carrito.productos) > 0:
                self.pagado = True
                print("Pago realizado correctamente")
            else:
                print("No se puede realizar el pago porque el carrito está vacío")
        else: 
            print("No se puede realizar el pago porque el usuario no está registrado")


class Envio:

    def __init__(self, pago):
        self.pago = pago
        self.estado = "Pendiente"

    def generar_envio(self):

        if self.pago.carrito.usuario.registrado:
            if self.pago.pagado:
                self.estado = "En camino"
                print("Envío generado correctamente")
            else:
                print("No se puede generar el envío porque el pago no fue realizado")
        else:
            print("No se puede generar el envío porque el usuario no está registrado")

# Ejecucion del sistema

print("Sistema de compras:")

# Registro
usuario1 = Usuario("cuenta@mail", "Daniel")
usuario1.registrar_usuario()

# Carrito
carrito1 = Carrito(usuario1)
carrito1.agregar_producto("Laptop")
carrito1.agregar_producto("Mouse")

# Pago
pago1 = Pago(carrito1)
pago1.procesar_pago()

# Envío
envio1 = Envio(pago1)
envio1.generar_envio()