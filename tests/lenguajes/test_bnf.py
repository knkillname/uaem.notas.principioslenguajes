"""Pruebas unitarias para el módulo materiales.lenguajes.bnf."""

import unittest

from materiales.lenguajes.bnf import ParserBNFLibreContexto, Token
from materiales.lenguajes.estructuras import Terminal, Variable


class TestParserBNFLibreContexto(unittest.TestCase):
    """Prueba la clase ParserBNFLibreContexto."""

    def test_tokenizar(self) -> None:
        """Prueba el método tokenizar."""
        entrada = """
        # Esto es un comentario.
        <S> ::= <A> | <B>  # Esto también es un comentario.
        <A> ::= "a"<A> | "a"

        <B> ::= "b"<B> | "" | "\\""

        """
        salida = [
            Token(tipo="NUEVA_LINEA", valor="\n", linea=2, columna=1),
            Token(tipo="NUEVA_LINEA", valor="\n", linea=3, columna=33),
            Token(tipo="NO_TERMINAL", valor="<S>", linea=3, columna=9),
            Token(tipo="PRODUCCION", valor="::=", linea=3, columna=13),
            Token(tipo="NO_TERMINAL", valor="<A>", linea=3, columna=17),
            Token(tipo="UNION", valor="|", linea=3, columna=21),
            Token(tipo="NO_TERMINAL", valor="<B>", linea=3, columna=23),
            Token(tipo="NUEVA_LINEA", valor="\n", linea=4, columna=60),
            Token(tipo="NO_TERMINAL", valor="<A>", linea=4, columna=9),
            Token(tipo="PRODUCCION", valor="::=", linea=4, columna=13),
            Token(tipo="TERMINAL", valor='"a"', linea=4, columna=17),
            Token(tipo="NO_TERMINAL", valor="<A>", linea=4, columna=20),
            Token(tipo="UNION", valor="|", linea=4, columna=24),
            Token(tipo="TERMINAL", valor='"a"', linea=4, columna=26),
            Token(tipo="NUEVA_LINEA", valor="\n", linea=5, columna=29),
            Token(tipo="NUEVA_LINEA", valor="\n", linea=6, columna=1),
            Token(tipo="NO_TERMINAL", valor="<B>", linea=6, columna=9),
            Token(tipo="PRODUCCION", valor="::=", linea=6, columna=13),
            Token(tipo="TERMINAL", valor='"b"', linea=6, columna=17),
            Token(tipo="NO_TERMINAL", valor="<B>", linea=6, columna=20),
            Token(tipo="UNION", valor="|", linea=6, columna=24),
            Token(tipo="TERMINAL", valor='""', linea=6, columna=26),
            Token(tipo="UNION", valor="|", linea=6, columna=29),
            Token(tipo="TERMINAL", valor='"\\""', linea=6, columna=31),
            Token(tipo="NUEVA_LINEA", valor="\n", linea=7, columna=35),
            Token(tipo="NUEVA_LINEA", valor="\n", linea=8, columna=1),
            Token(tipo="FIN", valor="", linea=8, columna=9),
        ]
        resultado = list(ParserBNFLibreContexto().tokenizar(entrada))
        self.assertEqual(resultado, salida)

        with self.assertRaises(SyntaxError):
            list(ParserBNFLibreContexto().tokenizar("S ::= <A> | <B> #"))

    def test_diseccionar(self) -> None:
        """Prueba el método diseccionar."""
        entrada = """
        # Esto es un comentario.
        <S> ::= <A> | <B>  # Esto también es un comentario.
        <A> ::= "a"<A> | "a"

        <B> ::= "b"<B> | ""

        """
        salida = {
            Variable("S"): ((Variable("A"),), (Variable("B"),)),
            Variable("A"): ((Terminal("a"), Variable("A")), (Terminal("a"),)),
            Variable("B"): ((Terminal("b"), Variable("B")), ()),
        }
        resultado = ParserBNFLibreContexto().diseccionar(entrada)
        self.assertEqual(resultado, salida)

        with self.assertRaises(SyntaxError):
            ParserBNFLibreContexto().diseccionar("S ::= <A> | <B> #")

    def test_error_no_terminal_en_izquierda(self) -> None:
        """Falla si la izquierda de la producción no es NO_TERMINAL."""
        # Izquierda comienza con un terminal en vez de no terminal
        with self.assertRaises(SyntaxError):
            ParserBNFLibreContexto().diseccionar('"a" ::= <A>')

    def test_error_signo_produccion_ausente(self) -> None:
        """Falla si no aparece '::=' tras el no terminal."""
        # Falta '::=' entre la izquierda y la derecha
        with self.assertRaises(SyntaxError):
            ParserBNFLibreContexto().diseccionar('<A> "a"')

    def test_error_simbolo_en_cadena(self) -> None:
        """Falla si la cadena comienza con un símbolo inválido."""
        # La derecha empieza con '|' en vez de un símbolo válido
        with self.assertRaises(SyntaxError):
            ParserBNFLibreContexto().diseccionar('<A> ::= | "a"')

    def test_error_cadena_inicio_invalido(self) -> None:
        """Falla si la cadena comienza con token inválido (caso adicional)."""
        with self.assertRaises(SyntaxError):
            ParserBNFLibreContexto().diseccionar('<B> ::= | "b"')
