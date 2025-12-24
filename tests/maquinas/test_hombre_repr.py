"""Pruebas de representación y validación para materiales.maquinas.hombre."""

# pylint: disable=protected-access

import unittest

from materiales.maquinas.hombre import ComputadoraHombrePequenno


class TestHombreRepresentaciones(unittest.TestCase):
    """Cobertura de __repr__, __str__, _repr_html_ y validaciones."""

    def test_repr_y_str(self) -> None:
        """Comprueba que __repr__ y __str__ contienen información esperada."""
        c = ComputadoraHombrePequenno()
        s = str(c)
        r = repr(c)
        self.assertIn("▶", c.marcador_pos)
        self.assertIn("acumulador", r)
        self.assertIn("X0", s)

    def test_repr_html(self) -> None:
        """Comprueba que _repr_html_ genera una tabla HTML legible."""
        c = ComputadoraHombrePequenno()
        html = c._repr_html_()
        self.assertIn("<table>", html)
        self.assertIn("<code>", html)

    def test_verificaciones_estado(self) -> None:
        """Valida errores de estado para acumulador, contador, memoria y E/S."""
        c = ComputadoraHombrePequenno()
        # Acumulador fuera de rango
        c.acumulador = 1000
        with self.assertRaises(ValueError):
            c._verificar_estado()
        # Contador fuera de rango
        c = ComputadoraHombrePequenno()
        c.contador = -1
        with self.assertRaises(ValueError):
            c._verificar_estado()
        # Memoria fuera de rango
        c = ComputadoraHombrePequenno()
        c.memoria[0] = 1000
        with self.assertRaises(ValueError):
            c._verificar_estado()
        # Entrada fuera de rango
        c = ComputadoraHombrePequenno()
        c.cargar_entrada([1000])
        with self.assertRaises(ValueError):
            c._verificar_estado()
        # Salida fuera de rango
        c = ComputadoraHombrePequenno()
        c.salida.append(1000)
        with self.assertRaises(ValueError):
            c._verificar_estado()


if __name__ == "__main__":
    unittest.main()
