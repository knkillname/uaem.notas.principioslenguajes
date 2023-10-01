"""Ejemplos de gramáticas libres de contexto."""
from .gramaticas import GramaticaLibreContexto


def gramatica1() -> GramaticaLibreContexto:
    """Ejemplo 1 de gramática libre de contexto."""
    gramatica_bnf = """
        <S> ::= "a" <S> "b" | <T>
        <T> ::= "c" <T> | ""
    """

    return GramaticaLibreContexto.desde_bnf(gramatica_bnf)


def gramatica2() -> GramaticaLibreContexto:
    """Ejemplo 2 de gramática libre de contexto."""
    gramatica_bnf = """
        <Oracion> ::= <Sujeto> " " <Predicado>
        <Sujeto> ::= <Articulo> " " <Sustantivo>| <NombrePropio> | <Pronombre>
        <Predicado> ::= <PredicadoSimple> | <PredicadoCompuesto>
        <PredicadoSimple> ::= <VerboSimple> " " <Objeto>
        <PredicadoSimple> ::= <VerboSimple> " " <Preposicon> " " <Objeto>
        <Objeto> ::= <Articulo> " " <Sustantivo>
        <PredicadoCompuesto> ::= <VerboCompuesto> " " <Oracion>
        <Preposicon> ::= "a" | "con" | "de" | "por" | "sobre"
        <Articulo> ::= "el" | "la" | "un" | "una"
        <Pronombre> ::= "él" | "ella"
        <Sustantivo> ::= "moneda" | "caparazón" | "hongo" | "flor" | "estrella"
        <NombrePropio> ::= "Mario" | "Luigi"
        <VerboSimple> ::= "come" | "salta" | "toma" | "golpea" | "esquiva"
        <VerboCompuesto> ::= "dice que" | "piensa que" | "sabe que"
    """

    return GramaticaLibreContexto.desde_bnf(gramatica_bnf)
