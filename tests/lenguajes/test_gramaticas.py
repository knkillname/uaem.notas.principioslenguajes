"""Pruebas para materiales.lenguajes.gramaticas."""

# pylint: disable=protected-access

import unittest

from materiales.lenguajes.estructuras import Cadena, Terminal, UnionCadenas, Variable
from materiales.lenguajes.gramaticas import Derivacion, GramaticaLibreContexto


class TestGramaticaLibreContexto(unittest.TestCase):
    """Cobertura de GramaticaLibreContexto y operaciones derivadas."""

    def setUp(self) -> None:
        """Crea una gramática simple: S -> aS | a."""
        self.gramatica_dict = {
            Variable("S"): UnionCadenas(
                (
                    Cadena([Terminal("a"), Variable("S")]),
                    Cadena([Terminal("a")]),
                )
            )
        }
        self.gramatica = GramaticaLibreContexto(self.gramatica_dict)

    def test_init_y_datos(self) -> None:
        """GramaticaLibreContexto se construye correctamente."""
        self.assertIn(Variable("S"), self.gramatica)
        self.assertEqual(len(self.gramatica), 1)

    def test_variables_y_terminales(self) -> None:
        """Variables y terminales se extraen correctamente."""
        vars_set = self.gramatica.variables
        terms = self.gramatica.terminales
        self.assertIn(Variable("S"), vars_set)
        self.assertIn(Terminal("a"), terms)

    def test_reglas_y_variable_inicial(self) -> None:
        """Reglas y variable inicial son correctas."""
        reglas = self.gramatica.reglas
        self.assertEqual(len(reglas), 2)
        self.assertEqual(self.gramatica.variable_inicial, Variable("S"))

    def test_desde_bnf(self) -> None:
        """Construcción desde BNF funciona."""
        texto = '<S> ::= "a"<S> | "a"'
        g = GramaticaLibreContexto.desde_bnf(texto)
        self.assertIn(Variable("S"), g)

    def test_getitem(self) -> None:
        """Acceso a cadenas de una variable."""
        s_cadenas = self.gramatica[Variable("S")]
        self.assertEqual(len(s_cadenas), 2)

    def test_iter(self) -> None:
        """Iteración sobre variables."""
        vars_iter = list(self.gramatica)
        self.assertIn(Variable("S"), vars_iter)

    def test_reglas_aplicables(self) -> None:
        """Reglas aplicables a una cadena."""
        cad = Cadena([Variable("S")])
        aplicables = list(self.gramatica.reglas_aplicables(cad))
        self.assertEqual(len(aplicables), 2)

    def test_producir_lenguaje(self) -> None:
        """Lenguaje producido contiene cadenas esperadas."""
        lenguaje = self.gramatica.producir_lenguaje()
        primeras = [next(lenguaje) for _ in range(3)]
        self.assertIn("a", primeras)

    def test_hacer_derivacion(self) -> None:
        """Se puede iniciar una derivación."""
        der = self.gramatica.hacer_derivacion()
        self.assertIsInstance(der, Derivacion)

    def test_repr_y_str(self) -> None:
        """Representaciones funcionan."""
        r = repr(self.gramatica)
        s = str(self.gramatica)
        self.assertIn("GramaticaLibreContexto", r)
        self.assertIn("S", s)

    def test_repr_markdown_y_latex(self) -> None:
        """Representaciones markdown y latex funcionan."""
        md = self.gramatica._repr_markdown_()
        latex = self.gramatica._repr_latex_()
        self.assertTrue(md)
        self.assertTrue(latex)

    def test_validacion_no_es_diccionario(self) -> None:
        """Validación rechaza string en lugar de diccionario."""
        with self.assertRaises(TypeError) as cm:
            GramaticaLibreContexto("S -> a")  # type: ignore[arg-type]
        self.assertIn("desde_bnf", str(cm.exception))

    def test_validacion_clave_no_variable(self) -> None:
        """Validación rechaza clave que no es Variable."""
        bad_dict = {"S": UnionCadenas((Cadena([Terminal("a")]),))}
        with self.assertRaises(TypeError):
            GramaticaLibreContexto(bad_dict)  # type: ignore[arg-type]

    def test_validacion_valor_no_secuencia(self) -> None:
        """Validación rechaza valor que no es Sequence."""
        bad_dict = {Variable("S"): Terminal("a")}
        with self.assertRaises(TypeError):
            GramaticaLibreContexto(bad_dict)  # type: ignore[arg-type]

    def test_validacion_cadena_no_secuencia(self) -> None:
        """Validación rechaza cadena que no es Sequence."""
        bad_dict = {Variable("S"): [Terminal("a")]}
        with self.assertRaises(TypeError):
            GramaticaLibreContexto(bad_dict)  # type: ignore[arg-type]


class TestDerivacion(unittest.TestCase):
    """Cobertura de Derivacion."""

    def setUp(self) -> None:
        """Crea una gramática y derivación."""
        gramatica_dict = {
            Variable("S"): UnionCadenas(
                (
                    Cadena([Terminal("a"), Variable("S")]),
                    Cadena([Terminal("a")]),
                )
            )
        }
        self.gramatica = GramaticaLibreContexto(gramatica_dict)
        self.derivacion = Derivacion(self.gramatica)

    def test_cadena_inicial(self) -> None:
        """Cadena inicial es la variable inicial."""
        self.assertEqual(self.derivacion.cadena, Cadena([Variable("S")]))

    def test_historial_vacio_inicial(self) -> None:
        """Historial comienza vacío."""
        self.assertEqual(len(self.derivacion.historial), 0)

    def test_aplicar_regla(self) -> None:
        """Aplicar regla modifica la cadena."""
        self.derivacion.aplicar_regla(1)
        self.assertGreater(len(self.derivacion.historial), 0)

    def test_arbol(self) -> None:
        """Se puede crear un árbol de derivación."""
        self.derivacion.aplicar_regla(1)
        arbol = self.derivacion.arbol()
        self.assertIsNotNone(arbol)

    def test_repr_latex(self) -> None:
        """Representación latex funciona."""
        latex = self.derivacion._repr_latex_()
        self.assertTrue(latex)
        self.derivacion.aplicar_regla(1)
        latex2 = self.derivacion._repr_latex_()
        self.assertTrue(latex2)


if __name__ == "__main__":
    unittest.main()
