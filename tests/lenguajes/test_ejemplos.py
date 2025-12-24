"""Pruebas para materiales.lenguajes.ejemplos."""

import unittest

from materiales.lenguajes.ejemplos import gramatica1, gramatica2
from materiales.lenguajes.estructuras import Variable


class TestEjemplos(unittest.TestCase):
    """Cobertura de funciones de ejemplo."""

    def test_gramatica1_construccion(self) -> None:
        """gramatica1() retorna una gramática válida."""
        g = gramatica1()
        self.assertIn(Variable("S"), g)
        self.assertIn(Variable("T"), g)

    def test_gramatica1_produce_lenguaje(self) -> None:
        """gramatica1() produce cadenas esperadas."""
        g = gramatica1()
        lenguaje = g.producir_lenguaje()
        primeras = [next(lenguaje) for _ in range(5)]
        self.assertIn("", primeras)

    def test_gramatica2_construccion(self) -> None:
        """gramatica2() retorna una gramática con oraciones."""
        g = gramatica2()
        self.assertIn(Variable("Oracion"), g)
        self.assertIn(Variable("Sujeto"), g)
        self.assertIn(Variable("Predicado"), g)

    def test_gramatica2_tiene_terminales(self) -> None:
        """gramatica2() contiene terminales de palabras."""
        g = gramatica2()
        terms = g.terminales
        # Debe tener varios terminales de palabras
        self.assertGreater(len(terms), 0)


if __name__ == "__main__":
    unittest.main()
