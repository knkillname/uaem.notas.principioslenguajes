"""Pruebas para materiales.lenguajes.ejemplos y numerabilidad."""

import unittest

from materiales.lenguajes import ejemplos, numerabilidad


class TestEjemplos(unittest.TestCase):
    """Smoke tests para módulo ejemplos."""

    def test_modulo_importa(self) -> None:
        """Módulo ejemplos se importa sin errores."""
        self.assertTrue(hasattr(ejemplos, "__doc__"))


class TestNumerabilidad(unittest.TestCase):
    """Smoke tests para módulo numerabilidad."""

    def test_modulo_importa(self) -> None:
        """Módulo numerabilidad se importa sin errores."""
        self.assertTrue(hasattr(numerabilidad, "__doc__"))


if __name__ == "__main__":
    unittest.main()
