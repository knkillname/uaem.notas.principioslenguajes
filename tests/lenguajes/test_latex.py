"""Pruebas para materiales.lenguajes.latex."""

import unittest

from materiales.lenguajes.latex import obtener_latex, quitar_dolares


class TestQuitarDolares(unittest.TestCase):
    """Cobertura de quitar_dolares."""

    def test_quitar_dolares_simple(self) -> None:
        """Quita entorno matemático con $."""
        resultado = quitar_dolares("$x + y$")
        self.assertEqual(resultado, "x + y")

    def test_quitar_dolares_doble(self) -> None:
        """Quita entorno matemático con $$."""
        resultado = quitar_dolares("$$x + y$$")
        self.assertEqual(resultado, "x + y")

    def test_quitar_dolares_corchetes(self) -> None:
        """Quita entorno matemático con \\[."""
        resultado = quitar_dolares("\\[x + y\\]")
        self.assertEqual(resultado, "x + y")

    def test_quitar_dolares_sin_dolares(self) -> None:
        """No modifica texto sin entorno matemático."""
        texto = "x + y"
        resultado = quitar_dolares(texto)
        self.assertEqual(resultado, texto)

    def test_quitar_dolares_espacios(self) -> None:
        """Maneja espacios alrededor del texto."""
        resultado = quitar_dolares("  $x + y$  ")
        self.assertEqual(resultado, "x + y")

    def test_quitar_dolares_doble_con_espacios(self) -> None:
        """Maneja espacios con $$ múltiples."""
        resultado = quitar_dolares("  $$x + y$$  ")
        self.assertEqual(resultado, "x + y")

    def test_quitar_dolares_solo_abre(self) -> None:
        """Maneja $ de apertura sin cierre."""
        texto = "$x + y"
        resultado = quitar_dolares(texto)
        self.assertEqual(resultado, texto)

    def test_quitar_dolares_solo_cierra(self) -> None:
        """Maneja $ de cierre sin apertura."""
        texto = "x + y$"
        resultado = quitar_dolares(texto)
        self.assertEqual(resultado, texto)

    def test_quitar_dolares_vacio(self) -> None:
        """Maneja texto vacío."""
        resultado = quitar_dolares("$$$$")
        self.assertEqual(resultado, "")

    def test_quitar_dolares_complejo(self) -> None:
        """Maneja expresiones matemáticas complejas."""
        resultado = quitar_dolares("$\\frac{a}{b}$")
        self.assertEqual(resultado, "\\frac{a}{b}")


class TestObtenerLatex(unittest.TestCase):
    """Cobertura de obtener_latex."""

    def test_obtener_latex_con_metodo(self) -> None:
        """obtener_latex usa _repr_latex_ si existe."""

        # pylint: disable=too-few-public-methods
        class MockObj:
            """Mock object with _repr_latex_ method."""

            def _repr_latex_(self) -> str:
                return "$x + y$"

        resultado = obtener_latex(MockObj())
        self.assertEqual(resultado, "x + y")

    def test_obtener_latex_sin_metodo(self) -> None:
        """obtener_latex usa str() si no existe _repr_latex_."""
        resultado = obtener_latex(42)
        self.assertEqual(resultado, "42")

    def test_obtener_latex_string(self) -> None:
        """obtener_latex funciona con strings."""
        resultado = obtener_latex("hello")
        self.assertEqual(resultado, "hello")

    def test_obtener_latex_con_dolares_dobles(self) -> None:
        """obtener_latex quita dolares dobles correctamente."""

        # pylint: disable=too-few-public-methods
        class MockObj:
            """Mock object returning double-dollar LaTeX."""

            def _repr_latex_(self) -> str:
                return "$$x + y$$"

        resultado = obtener_latex(MockObj())
        self.assertEqual(resultado, "x + y")

    def test_obtener_latex_con_corchetes(self) -> None:
        """obtener_latex quita corchetes correctamente."""

        # pylint: disable=too-few-public-methods
        class MockObj:
            """Mock object with bracket LaTeX."""

            def _repr_latex_(self) -> str:
                return "\\[x + y\\]"

        resultado = obtener_latex(MockObj())
        self.assertEqual(resultado, "x + y")

    def test_obtener_latex_objeto_personalizado(self) -> None:
        """obtener_latex maneja objetos con _repr_latex_ complejo."""

        # pylint: disable=too-few-public-methods
        class Variable:
            """Variable class with complex LaTeX representation."""

            def __init__(self, name: str) -> None:
                self.name = name

            def _repr_latex_(self) -> str:
                return f"$\\mathrm{{{self.name}}}$"

        resultado = obtener_latex(Variable("X"))
        self.assertEqual(resultado, "\\mathrm{X}")

    def test_obtener_latex_none(self) -> None:
        """obtener_latex maneja None."""
        resultado = obtener_latex(None)
        self.assertEqual(resultado, "None")


if __name__ == "__main__":
    unittest.main()
