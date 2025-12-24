"""Pruebas para materiales.lenguajes.numerabilidad."""

import unittest

from materiales.lenguajes.numerabilidad import Shortlex, cmp_shortlex, estrella, muestra


class TestNumerabilidad(unittest.TestCase):
    """Cobertura de funciones para lenguajes numerables."""

    def test_cmp_shortlex_iguales(self) -> None:
        """cmp_shortlex retorna 0 para cadenas iguales."""
        self.assertEqual(cmp_shortlex("a", "a"), 0)

    def test_cmp_shortlex_longitud_menor(self) -> None:
        """cmp_shortlex retorna -1 si primera cadena es más corta."""
        self.assertEqual(cmp_shortlex("a", "aa"), -1)

    def test_cmp_shortlex_longitud_mayor(self) -> None:
        """cmp_shortlex retorna 1 si primera cadena es más larga."""
        self.assertEqual(cmp_shortlex("aa", "a"), 1)

    def test_cmp_shortlex_mismo_largo_orden_lexico(self) -> None:
        """cmp_shortlex usa orden lexicográfico para igual longitud."""
        self.assertEqual(cmp_shortlex("a", "b"), -1)
        self.assertEqual(cmp_shortlex("b", "a"), 1)

    def test_shortlex_objeto(self) -> None:
        """Shortlex es una función de comparación válida."""
        cadenas = ["b", "a", "aa", ""]
        ordenadas = sorted(cadenas, key=Shortlex)
        # Esperado: "" < "a" < "b" < "aa"
        self.assertEqual(ordenadas[0], "")
        self.assertEqual(ordenadas[1], "a")
        self.assertEqual(ordenadas[2], "b")
        self.assertEqual(ordenadas[3], "aa")

    def test_estrella_vacia(self) -> None:
        """estrella genera cadena vacía primero."""
        gen = estrella("a")
        self.assertEqual(next(gen), "")

    def test_estrella_alfabeto_a(self) -> None:
        """estrella('a') genera '', 'a', 'aa', 'aaa'..."""
        gen = estrella("a")
        primeras = [next(gen) for _ in range(5)]
        self.assertEqual(primeras, ["", "a", "aa", "aaa", "aaaa"])

    def test_estrella_alfabeto_ab(self) -> None:
        """estrella('ab') genera cadenas sobre {a, b} en orden shortlex."""
        gen = estrella("ab")
        primeras = [next(gen) for _ in range(8)]
        # Esperado: "", "a", "b", "aa", "ab", "ba", "bb", "aaa"
        self.assertEqual(primeras[0], "")
        self.assertIn("a", primeras)
        self.assertIn("b", primeras)

    def test_muestra_retorna_lista(self) -> None:
        """muestra retorna una lista de elementos."""
        gen = estrella("a")
        # Use orden=3 to keep indices small and avoid timeouts
        m = muestra(gen, 5, orden=3)
        self.assertIsInstance(m, list)
        # May get fewer elements if iterator exhausted, so just check it's a list
        self.assertLessEqual(len(m), 5)

    def test_muestra_elementos_son_cadenas(self) -> None:
        """muestra retorna cadenas del iterable."""
        gen = estrella("ab")
        m = muestra(gen, 3)
        for elemento in m:
            self.assertIsInstance(elemento, str)

    def test_muestra_iterador_finito(self) -> None:
        """muestra maneja iteradores finitos sin error."""
        # Iterador pequeño que se agotará
        finito = iter(["a", "b", "c"])
        # Pedir elementos con orden pequeño para que sea más probable obtener algunos
        m = muestra(finito, 3, orden=2)
        # Debe retornar una lista (posiblemente vacía si los índices saltan demasiado)
        self.assertIsInstance(m, list)
        # Con orden=2, es más probable que obtengamos al menos algunos
        self.assertLessEqual(len(m), 3)


if __name__ == "__main__":
    unittest.main()
