"""Pruebas unitarias para el módulo materiales.lenguajes.bnf."""
import unittest

from materiales.lenguajes.bnf import ParserBNFLibreContexto, Token
from materiales.lenguajes.estructuras import NoTerminal, Terminal


class TestParserBNFLibreContexto(unittest.TestCase):
    """Prueba la clase ParserBNFLibreContexto."""

    def test_tokenizar(self):
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

    def test_diseccionar(self):
        """Prueba el método diseccionar."""
        entrada = """
        # Esto es un comentario.
        <S> ::= <A> | <B>  # Esto también es un comentario.
        <A> ::= "a"<A> | "a"

        <B> ::= "b"<B> | ""

        """
        salida = {
            NoTerminal("S"): [(NoTerminal("A"),), (NoTerminal("B"),)],
            NoTerminal("A"): [(Terminal("a"), NoTerminal("A")), (Terminal("a"),)],
            NoTerminal("B"): [(Terminal("b"), NoTerminal("B")), (Terminal(""),)],
        }
        resultado = ParserBNFLibreContexto().diseccionar(entrada)
        self.assertEqual(resultado, salida)

        with self.assertRaises(SyntaxError):
            ParserBNFLibreContexto().diseccionar("S ::= <A> | <B> #")
