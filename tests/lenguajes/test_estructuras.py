"""Pruebas para materiales.lenguajes.estructuras."""

# pylint: disable=protected-access

import unittest

from materiales.lenguajes.estructuras import (
    Cadena,
    MultiRegla,
    Regla,
    Terminal,
    UnionCadenas,
    Variable,
)


class TestEstructuras(unittest.TestCase):
    """Cobertura de representaciones y operaciones básicas."""

    def test_variable_y_terminal_str_markdown_latex(self) -> None:
        """Verifica representaciones de Variable y Terminal en str/md/latex."""
        v = Variable("S")
        t = Terminal("a")
        te = Terminal("")
        self.assertEqual(str(v), "<S>")
        self.assertTrue(v._repr_markdown_())
        self.assertTrue(v._repr_latex_())
        self.assertEqual(str(t), '"a"')
        self.assertEqual(str(te), "ε")
        self.assertTrue(t._repr_markdown_())
        self.assertTrue(t._repr_latex_())
        self.assertTrue(te._repr_markdown_())
        self.assertTrue(te._repr_latex_())

    def test_cadena_filtra_vacios_y_representaciones(self) -> None:
        """Cadena filtra símbolos vacíos y produce representaciones."""
        c = Cadena([Terminal("a"), Terminal(""), Variable("X")])
        self.assertEqual(str(c), '"a"<X>')
        self.assertTrue(c._repr_markdown_())
        self.assertTrue(c._repr_latex_())
        self.assertEqual(str(Cadena([])), "")

    def test_union_cadenas_y_multiregla_str_markdown_latex(self) -> None:
        """UnionCadenas y MultiRegla retornan str/md/latex apropiados."""
        u = UnionCadenas((Cadena([Terminal("a")]), Cadena([Variable("X")])))
        self.assertIn("|", str(u))
        self.assertTrue(u._repr_markdown_())
        self.assertTrue(u._repr_latex_())
        mr = MultiRegla(Variable("S"), u)
        self.assertIn("→", str(mr))
        self.assertTrue(mr._repr_markdown_())
        self.assertTrue(mr._repr_latex_())

    def test_regla_aplicar(self) -> None:
        """Regla.aplicar reemplaza la variable correcta según n_salto."""
        r = Regla(Variable("S"), Cadena([Terminal("a")]))
        cad = Cadena([Variable("S"), Variable("S")])
        res0 = r.aplicar(cad, 0)
        res1 = r.aplicar(cad, 1)
        self.assertEqual(str(res0), '"a"<S>')
        self.assertEqual(str(res1), '<S>"a"')
        self.assertIn("→", str(r))
        self.assertTrue(r._repr_markdown_())
        self.assertTrue(r._repr_latex_())

    def test_simbolo_comparaciones(self) -> None:
        """Símbolos soportan comparaciones y operadores."""
        v1 = Variable("A")
        v2 = Variable("B")
        v3 = Variable("A")
        # Test __lt__
        self.assertTrue(v1 < v2)
        self.assertFalse(v2 < v1)
        # Test __eq__ and __ne__
        self.assertEqual(v1, v3)
        self.assertNotEqual(v1, v2)
        self.assertTrue(v1 != v2)
        self.assertFalse(v1 != v3)
        # Test __lt__ with different types (should return NotImplemented)
        self.assertNotEqual(v1, "A")
        # Test __bool__
        self.assertTrue(bool(Variable("X")))
        self.assertFalse(bool(Variable("")))
        self.assertTrue(bool(Terminal("a")))
        self.assertFalse(bool(Terminal("")))

    def test_cadena_vacia_representaciones(self) -> None:
        """Cadena vacía tiene representaciones especiales."""
        c_vacia = Cadena([])
        self.assertEqual(str(c_vacia), "")
        md = c_vacia._repr_markdown_()
        latex = c_vacia._repr_latex_()
        # Debe contener epsilon
        self.assertIn("varepsilon", md)
        self.assertIn("varepsilon", latex)

    def test_simbolo_hash_y_repr(self) -> None:
        """Símbolos son hashables y tienen repr."""
        v = Variable("S")
        t = Terminal("a")
        # Test hash (debe funcionar en sets/dicts)
        simbolos = {v, t, Variable("S")}  # S duplicado
        self.assertEqual(len(simbolos), 2)
        # Test repr
        self.assertIn("Variable", repr(v))
        self.assertIn("Terminal", repr(t))


if __name__ == "__main__":
    unittest.main()
