"""Pruebas unitarias para materiales.maquinas.pila."""

import unittest

from materiales.maquinas.pila import MaquinaDePila


class TestMaquinaDePila(unittest.TestCase):
    """Cobertura amplia de operaciones de la máquina de pila."""

    def setUp(self) -> None:
        self.m = MaquinaDePila()

    def test_pila_basico(self) -> None:
        """Apilar, cima, desapilar, vaciar y vacío."""
        self.assertTrue(self.m.esta_vacia())
        self.m.apilar(1).apilar(2)
        self.assertFalse(self.m.esta_vacia())
        self.assertEqual(self.m.ver_cima(), 2)
        self.assertEqual(self.m.desapilar(), 2)
        self.m.vaciar()
        self.assertTrue(self.m.esta_vacia())

    def test_aritmetica(self) -> None:
        """+, -, signo, *, /, //, %, **."""
        self.m.vaciar().apilar(3).apilar(4).suma()
        self.assertEqual(self.m.ver_cima(), 7)
        self.m.vaciar().apilar(10).apilar(6).resta()
        self.assertEqual(self.m.ver_cima(), 4)
        self.m.vaciar().apilar(-5).invertir_signo()
        self.assertEqual(self.m.ver_cima(), 5)
        self.m.vaciar().apilar(3).apilar(5).multiplicacion()
        self.assertEqual(self.m.ver_cima(), 15)
        self.m.vaciar().apilar(20).apilar(5).division()
        self.assertEqual(self.m.ver_cima(), 4)
        self.m.vaciar().apilar(20).apilar(6).division_entera()
        self.assertEqual(self.m.ver_cima(), 3)
        self.m.vaciar().apilar(20).apilar(6).modulo()
        self.assertEqual(self.m.ver_cima(), 2)
        self.m.vaciar().apilar(2).apilar(3).potencia()
        self.assertEqual(self.m.ver_cima(), 8)

    def test_comparaciones(self) -> None:
        """<, <=, ==, !=, >=, >."""
        self.m.vaciar().apilar(3).apilar(4).menor_que()
        self.assertTrue(self.m.ver_cima())
        self.m.vaciar().apilar(4).apilar(4).menor_o_igual_que()
        self.assertTrue(self.m.ver_cima())
        self.m.vaciar().apilar(4).apilar(4).igual_que()
        self.assertTrue(self.m.ver_cima())
        self.m.vaciar().apilar(4).apilar(5).diferente_que()
        self.assertTrue(self.m.ver_cima())
        self.m.vaciar().apilar(5).apilar(4).mayor_o_igual_que()
        self.assertTrue(self.m.ver_cima())
        self.m.vaciar().apilar(5).apilar(4).mayor_que()
        self.assertTrue(self.m.ver_cima())

    def test_logicos(self) -> None:
        """and, or, not."""
        self.m.vaciar().apilar(True).apilar(False).y_logico()
        self.assertFalse(self.m.ver_cima())
        self.m.vaciar().apilar(True).apilar(False).o_logico()
        self.assertTrue(self.m.ver_cima())
        self.m.vaciar().apilar(False).negacion()
        self.assertTrue(self.m.ver_cima())

    def test_bits_y_corrimientos(self) -> None:
        """&, |, ^, ~, <<, >>."""
        self.m.vaciar().apilar(0b1100).apilar(0b1010).y_bit_a_bit()
        self.assertEqual(self.m.ver_cima(), 0b1000)
        self.m.vaciar().apilar(0b1100).apilar(0b1010).o_bit_a_bit()
        self.assertEqual(self.m.ver_cima(), 0b1110)
        self.m.vaciar().apilar(0b1100).apilar(0b1010).xor()
        self.assertEqual(self.m.ver_cima(), 0b0110)
        self.m.vaciar().apilar(0b0011).negacion_bit_a_bit()
        self.assertEqual(self.m.ver_cima(), ~0b0011)
        self.m.vaciar().apilar(0b0001).apilar(3).corrimiento_izquierda()
        self.assertEqual(self.m.ver_cima(), 0b1000)
        self.m.vaciar().apilar(0b1000).apilar(3).corrimiento_derecha()
        self.assertEqual(self.m.ver_cima(), 0b0001)

    def test_repr_markdown(self) -> None:
        """_repr_markdown_ genera tabla con niveles."""
        # pylint: disable=protected-access
        self.m.vaciar()
        md_vacia = self.m._repr_markdown_()
        self.assertIn("Nivel", md_vacia)
        self.assertIn("Elemento", md_vacia)
        # Pila con elementos
        self.m.apilar(10).apilar(20).apilar(30)
        md = self.m._repr_markdown_()
        self.assertIn("Nivel", md)
        self.assertIn("|", md)
        self.assertIn("30", md)
        self.assertIn("20", md)
        self.assertIn("10", md)


if __name__ == "__main__":
    unittest.main()
