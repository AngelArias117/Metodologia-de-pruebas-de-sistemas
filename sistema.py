class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.id_producto = id_producto
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def hay_stock(self, cantidad):
        return self.stock >= cantidad

    def descontar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        if not self.hay_stock(cantidad):
            raise ValueError("Stock insuficiente")

        self.stock -= cantidad


class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email


class Carrito:
    def __init__(self, usuario):
        self.usuario = usuario
        self.items = []

    def agregar_producto(self, producto, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")

        if not producto.hay_stock(cantidad):
            raise ValueError("Stock insuficiente")

        self.items.append({
            "producto": producto,
            "cantidad": cantidad
        })

    def esta_vacio(self):
        return len(self.items) == 0

    def calcular_total(self):
        total = 0

        for item in self.items:
            producto = item["producto"]
            cantidad = item["cantidad"]
            total += producto.precio * cantidad

        return total

    def confirmar_compra(self):
        if self.esta_vacio():
            raise ValueError("El carrito está vacío")

        for item in self.items:
            producto = item["producto"]
            cantidad = item["cantidad"]
            producto.descontar_stock(cantidad)


class PlataformaPagoX:
    MEDIOS_VALIDOS = ["credito", "debito", "transferencia"]

    def validar_medio_pago(self, medio_pago):
        return medio_pago in self.MEDIOS_VALIDOS

    def procesar_pago(self, monto, medio_pago):
        if monto <= 0:
            return False

        if not self.validar_medio_pago(medio_pago):
            return False

        return True


class Compra:
    def __init__(self, usuario, carrito, plataforma_pago):
        self.usuario = usuario
        self.carrito = carrito
        self.plataforma_pago = plataforma_pago
        self.estado = "pendiente"

    def finalizar_compra(self, medio_pago):
        if self.carrito.esta_vacio():
            self.estado = "rechazada"
            return False

        total = self.carrito.calcular_total()

        pago_aprobado = self.plataforma_pago.procesar_pago(total, medio_pago)

        if not pago_aprobado:
            self.estado = "rechazada"
            return False

        self.carrito.confirmar_compra()
        self.estado = "aprobada"
        return True