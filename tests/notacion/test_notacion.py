"""Pruebas para materiales.notacion."""

import unittest

from materiales.lenguajes.estructuras import Terminal, Variable
from materiales.notacion import Conjunto, Lenguaje, ListaNumerada, Sucesion


class TestConjunto(unittest.TestCase):
    """Cobertura de Conjunto."""

    def test_conjunto_markdown(self) -> None:
        """Markdown básico de Conjunto."""
        c = Conjunto({Terminal("a"), "x"})
        md = c._repr_markdown_()
        self.assertTrue(md.startswith("{"))
        self.assertTrue(md.endswith("}"))

    def test_conjunto_iteracion(self) -> None:
        """Se puede iterar sobre un Conjunto."""
        c = Conjunto({1, 2, 3})
        elementos = list(c)
        self.assertEqual(len(elementos), 3)

    def test_conjunto_pertenencia(self) -> None:
        """Operador 'in' funciona con Conjunto."""
        c = Conjunto({"a", "b"})
        self.assertIn("a", c)
        self.assertNotIn("c", c)

    def test_conjunto_markdown_varios_elementos(self) -> None:
        """Markdown de Conjunto con múltiples elementos."""
        c = Conjunto({Terminal("a"), Terminal("b"), Terminal("c")})
        md = c._repr_markdown_()
        self.assertIn("{", md)
        self.assertIn("}", md)
        # Terminal usa backticks, no comillas
        self.assertGreater(md.count("`"), 0)

    def test_conjunto_markdown_sin_repr_markdown(self) -> None:
        """Markdown de Conjunto con elementos sin _repr_markdown_."""
        c = Conjunto({1, 2, 3})
        md = c._repr_markdown_()
        self.assertIn("{", md)
        self.assertIn("1", md)
        self.assertIn("2", md)
        self.assertIn("3", md)


class TestLenguaje(unittest.TestCase):
    """Cobertura de Lenguaje."""

    def test_lenguaje_getitem_y_latex(self) -> None:
        """Getitem y LaTeX de Lenguaje."""
        l = Lenguaje(["a", "b", "c"], rebanada=slice(0, None, None))
        self.assertEqual(l[0], "a")
        sub = l[1:]
        self.assertIsInstance(sub, Lenguaje)
        latex = l._repr_latex_()
        self.assertIn("\\{", latex)

    def test_lenguaje_len(self) -> None:
        """__len__ retorna cantidad de elementos."""
        l = Lenguaje(["a", "b", "c"], rebanada=slice(0, None, None))
        self.assertEqual(len(l), 3)

    def test_lenguaje_getitem_negativo(self) -> None:
        """Indexación negativa funciona."""
        l = Lenguaje(["a", "b", "c"], rebanada=slice(0, None, None))
        self.assertEqual(l[-1], "c")

    def test_lenguaje_slice_vacio(self) -> None:
        """Slicing vacío."""
        l = Lenguaje(["a", "b", "c"], rebanada=slice(0, None, None))
        sub = l[10:20]
        self.assertEqual(len(sub), 0)

    def test_lenguaje_iter(self) -> None:
        """Se puede iterar sobre Lenguaje."""
        l = Lenguaje(["a", "b"], rebanada=slice(0, None, None))
        elementos = list(l)
        self.assertEqual(elementos, ["a", "b"])

    def test_lenguaje_repr_latex(self) -> None:
        """_repr_latex_ genera LaTeX válido."""
        l = Lenguaje(["a", "b", "c"], rebanada=slice(0, None, None))
        latex = l._repr_latex_()
        self.assertIn("$", latex)
        self.assertIn("ldots", latex)
        # Debe contener los elementos
        self.assertIn("a", latex)


class TestSucesion(unittest.TestCase):
    """Cobertura de Sucesion."""

    def test_sucesion_markdown(self) -> None:
        """Markdown básico de Sucesion."""
        s = Sucesion((Terminal("a"), "x"))
        md = s._repr_markdown_()
        self.assertTrue(md.startswith("("))
        self.assertTrue(md.endswith(")"))

    def test_sucesion_indexacion(self) -> None:
        """Se puede indexar Sucesion."""
        s = Sucesion((1, 2, 3))
        self.assertEqual(s[0], 1)
        self.assertEqual(s[2], 3)

    def test_sucesion_len(self) -> None:
        """__len__ funciona en Sucesion."""
        s = Sucesion(("a", "b", "c"))
        self.assertEqual(len(s), 3)

    def test_sucesion_iteracion(self) -> None:
        """Se puede iterar sobre Sucesion."""
        s = Sucesion((1, 2, 3))
        elementos = list(s)
        self.assertEqual(elementos, [1, 2, 3])

    def test_sucesion_markdown_con_repr(self) -> None:
        """Markdown de Sucesion con elementos que tienen _repr_markdown_."""
        s = Sucesion((Terminal("a"), Terminal("b")))
        md = s._repr_markdown_()
        self.assertIn("(", md)
        self.assertIn(")", md)

    def test_sucesion_markdown_sin_repr(self) -> None:
        """Markdown de Sucesion con elementos sin _repr_markdown_."""
        s = Sucesion((1, 2, 3))
        md = s._repr_markdown_()
        self.assertIn("(", md)
        self.assertIn("1", md)
        self.assertIn("2", md)


class TestListaNumerada(unittest.TestCase):
    """Cobertura de ListaNumerada."""

    def test_lista_numerada_str_y_markdown(self) -> None:
        """Str y markdown básicos de ListaNumerada."""
        ln = ListaNumerada(("uno", "dos"))
        self.assertIn("1. uno", str(ln))
        md = ln._repr_markdown_()
        self.assertIn("1.", md)

    def test_lista_numerada_indexacion(self) -> None:
        """Se puede indexar ListaNumerada."""
        ln = ListaNumerada(("uno", "dos", "tres"))
        self.assertEqual(ln[0], "uno")

    def test_lista_numerada_len(self) -> None:
        """__len__ retorna cantidad de elementos."""
        ln = ListaNumerada(("a", "b", "c"))
        self.assertEqual(len(ln), 3)

    def test_lista_numerada_markdown_formato(self) -> None:
        """Markdown tiene formato numeral correcto."""
        ln = ListaNumerada(("primero", "segundo"))
        md = ln._repr_markdown_()
        self.assertIn("1.", md)
        self.assertIn("2.", md)

    def test_lista_numerada_str(self) -> None:
        """__str__ retorna lista numerada formateada."""
        ln = ListaNumerada(("uno", "dos", "tres"))
        s = str(ln)
        self.assertIn("1. uno", s)
        self.assertIn("2. dos", s)
        self.assertIn("3. tres", s)

    def test_lista_numerada_markdown_con_repr(self) -> None:
        """Markdown de ListaNumerada con elementos que tienen _repr_markdown_."""
        ln = ListaNumerada((Variable("A"), Variable("B")))
        md = ln._repr_markdown_()
        self.assertIn("1.", md)
        self.assertIn("2.", md)


if __name__ == "__main__":
    unittest.main()
