import unittest
from sistema import *

class TestReglasNegocio(unittest.TestCase):

    # Caso válido
    def test_agregar_producto_valido(self):
        p = Producto(1, "Mouse", 100, 10)
        u = Usuario(1, "Angel", "a@mail.com")
        c = Carrito(u)

        c.agregar_producto(p, 2)

        self.assertEqual(len(c.items), 1)

    # Caso inválido: cantidad negativa
    def test_agregar_producto_cantidad_invalida(self):
        p = Producto(1, "Mouse", 100, 10)
        u = Usuario(1, "Angel", "a@mail.com")
        c = Carrito(u)

        with self.assertRaises(ValueError):
            c.agregar_producto(p, -1)

    # Caso inválido: sin stock
    def test_agregar_producto_sin_stock(self):
        p = Producto(1, "Mouse", 2, 2)
        u = Usuario(1, "Angel", "a@mail.com")
        c = Carrito(u)

        with self.assertRaises(ValueError):
            c.agregar_producto(p, 5)


if __name__ == '__main__':
    unittest.main()