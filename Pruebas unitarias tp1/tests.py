import unittest
from sistema import *

class TestReglasNegocio(unittest.TestCase):

    # Caso válido: Agregar producto
    def test_agregar_producto_valido(self):
        p = Producto(1, "Mouse", 100, 10)
        u = Usuario(1, "Angel", "aa@mail.com")
        c = Carrito(u)

        c.agregar_producto(p, 2)

        self.assertEqual(len(c.items), 1)

    # Caso inválido: Cantidad negativa
    def test_agregar_producto_cantidad_invalida(self):
        p = Producto(1, "Mouse", 100, 10)
        u = Usuario(1, "Angel", "aa@mail.com")
        c = Carrito(u)

        with self.assertRaises(ValueError):
            c.agregar_producto(p, -1)

    # Caso inválido: Sin stock
    def test_agregar_producto_sin_stock(self):
        p = Producto(1, "Mouse", 100, 2)
        u = Usuario(1, "Angel", "aa@mail.com")
        c = Carrito(u)

        with self.assertRaises(ValueError):
            c.agregar_producto(p, 5)

class TestEstadosSistema(unittest.TestCase):

    # Escenario normal: Flujo principal
    def test_flujo_principal(self):
        u = Usuario(1, "Pablo", "pl@mail.com")
        c = Carrito(u)
        p = Producto(1, "Mouse", 100, 10)
        c.agregar_producto(p, 2)
        px = PlataformaPagoX()
        compra = Compra(u, c, px)
        self.assertEqual(compra.estado, 'pendiente')
        self.assertTrue(compra.finalizar_compra('debito'))
        self.assertEqual(compra.estado, 'aprobada')
        self.assertEqual(p.stock, 8)
        self.assertTrue(c.esta_vacio())

    # Escenario alternativo: Pago invalido
    def test_medio_de_pago_invalido(self):
        u = Usuario(1, "Pablo", "pl@mail.com")
        c = Carrito(u)
        p = Producto(1, "Mouse", 100, 10)
        c.agregar_producto(p, 2)
        px = PlataformaPagoX()
        compra = Compra(u, c, px)
        self.assertEqual(compra.estado, 'pendiente')
        self.assertFalse(compra.finalizar_compra(''))# no se elige un medio de pago
        self.assertEqual(compra.estado, 'rechazada')
        self.assertEqual(p.stock, 10)
        self.assertFalse(c.esta_vacio())

    # Escenario de fallo: Carrito vacio
    def test_compra_vacia(self):
        u = Usuario(1, "Pablo", "aa@mail.com")
        c = Carrito(u)
        self.assertTrue(c.esta_vacio())
        px = PlataformaPagoX()
        compra = Compra(u, c, px)
        self.assertEqual(compra.estado, 'pendiente')
        self.assertFalse(compra.finalizar_compra('debito'))
        self.assertEqual(compra.estado, 'rechazada')

if __name__ == '__main__':
    unittest.main()