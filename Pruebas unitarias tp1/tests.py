import unittest
from sistema import *

class TestReglasNegocio(unittest.TestCase):

    # Definicion de variables antes de cada test
    def setUp(self):
        self.producto = Producto(1, "Mouse", 100, 10)
        self.usuario = Usuario(1, "Angel", "aa@mail.com")
        self.carrito = Carrito(self.usuario)

    # Caso válido: Agregar producto
    def test_01_agregar_producto_valido(self):
        self.carrito.agregar_producto(self.producto, 2)
        self.assertEqual(len(self.carrito.items), 1)

    # Caso inválido: Cantidad negativa
    def test_02_agregar_producto_cantidad_invalida(self):
        with self.assertRaises(ValueError):
            self.carrito.agregar_producto(self.producto, -1)

    # Caso inválido: Sin stock
    def test_03_agregar_producto_sin_stock(self):
        with self.assertRaises(ValueError):
            self.carrito.agregar_producto(self.producto, 15)

class TestEstadosSistema(unittest.TestCase):

    # Definicion de variables antes de cada test
    def setUp(self):
        self.usuario = Usuario(1, "Pablo", "pl@mail.com")
        self.carrito = Carrito(self.usuario)
        self.producto = Producto(1, "Mouse", 100, 10)
        self.px = PlataformaPagoX()
        self.compra = Compra(self.usuario, self.carrito, self.px)

    # Escenario normal: Flujo principal
    def test_04_flujo_principal(self):
        self.carrito.agregar_producto(self.producto, 2)
        self.assertEqual(self.compra.estado, 'pendiente')
        self.assertEqual(self.compra.carrito.calcular_total(), 200)
        self.assertTrue(self.compra.finalizar_compra('debito'))
        self.assertEqual(self.compra.estado, 'aprobada')
        self.assertTrue(self.carrito.esta_vacio())
        self.assertEqual(self.producto.stock, 8)

    # Escenario alternativo: Compra mas de un producto
    def test_07_varios_productos(self):
        self.carrito.agregar_producto(self.producto, 2)
        teclado = Producto(2, "Teclado", 60, 7)
        self.carrito.agregar_producto(teclado, 2)
        self.assertEqual(self.compra.estado, 'pendiente')
        self.assertEqual(self.compra.carrito.calcular_total(), 320)
        self.assertTrue(self.compra.finalizar_compra('debito'))
        self.assertEqual(self.compra.estado, 'aprobada')
        self.assertTrue(self.carrito.esta_vacio())
        self.assertEqual(self.producto.stock, 8)
        self.assertEqual(teclado.stock, 5)

    # Escenarios de fallo:
    # Pago invalido
    def test_05_medio_de_pago_invalido(self):
        self.carrito.agregar_producto(self.producto, 2)
        self.assertEqual(self.compra.estado, 'pendiente')
        self.assertFalse(self.compra.finalizar_compra(''))# no se elige un medio de pago
        self.assertEqual(self.compra.estado, 'rechazada')
        self.assertEqual(self.producto.stock, 10)
        self.assertFalse(self.carrito.esta_vacio())
    #  Carrito vacio
    def test_06_compra_vacia(self):
        self.assertTrue(self.carrito.esta_vacio())
        self.assertEqual(self.compra.estado, 'pendiente')
        self.assertFalse(self.compra.finalizar_compra('debito'))
        self.assertEqual(self.compra.estado, 'rechazada')


if __name__ == '__main__':
    unittest.main()
