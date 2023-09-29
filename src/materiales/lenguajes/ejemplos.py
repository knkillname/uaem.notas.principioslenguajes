from .gramaticas import GramaticaLibreContexto


def gramatica1() -> GramaticaLibreContexto:
    """Ejemplo 1 de gramática libre de contexto."""
    gramatica_bnf = """
        <S> ::= "a" <S> "b" | <T>
        <T> ::= "c" <T> | ""
    """

    return GramaticaLibreContexto.desde_bnf(gramatica_bnf)
