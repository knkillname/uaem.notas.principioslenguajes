"""Módulo para analizar gramáticas en notación BNF.

Este módulo contiene la clase ParserBNFLibreContexto, que permite
analizar gramáticas en notación BNF. La gramática debe ser libre de
contexto.
"""
import json
import re
from collections import deque
from typing import Iterator, NamedTuple

from .estructuras import (
    Cadena,
    GramaticaLibreContextoDict,
    GramaticaLibreContextoMap,
    MultiRegla,
    Simbolo,
    Terminal,
    UnionCadenas,
    Variable,
)


class Token(NamedTuple):
    """Representa un token de una gramática en BNF.

    Atributos
    ---------
    tipo : str
        El tipo del token.
    valor : str
        El texto del token.
    linea : int
        El número de línea donde se encuentra el token.
    columna : int
        El número de columna donde se encuentra el token.
    """

    tipo: str
    valor: str
    linea: int
    columna: int


class ParserBNFLibreContexto:
    """Analizador sintáctico para gramáticas en notación BNF."""

    spec_tokens = {
        "NO_TERMINAL": r"<[\w\-\.]+?>",  # No terminales van entre corchetes angulares
        "TERMINAL": r'"(\\.|[^"\\])*"',  # Los terminales están entre comillas dobles
        "UNION": r"\|",  # La unión es el símbolo |
        "PRODUCCION": r"::=",  # La producción se simboliza con ::=
        "NUEVA_LINEA": r"\n",  # Salto de línea
        "COMENTARIO": r"\#[^\n]*",  # Los comentarios comienzan con #
        "ESPACIO": r"\s+?",  # Cualquier espacio en blanco
        "FIN": r"$",  # Fin de la cadena
        "ERROR": r".",  # Cualquier otro carácter
    }
    tok_regex = "|".join(f"(?P<{tipo}>{regex})" for tipo, regex in spec_tokens.items())

    def tokenizar(self, texto: str) -> Iterator[Token]:
        """Convierte un texto en una secuencia de tokens."""
        linea = 1
        inicio_de_linea = 0
        for coincidencia in re.finditer(self.tok_regex, texto):
            tipo = coincidencia.lastgroup
            if tipo is None:
                continue
            valor = coincidencia.group(tipo)
            columna = coincidencia.start() - inicio_de_linea + 1
            match tipo:
                case "ESPACIO" | "COMENTARIO":
                    continue  # Ignora espacios y comentarios
                case "NUEVA_LINEA":
                    linea += 1
                    inicio_de_linea = coincidencia.end()
                case "ERROR":
                    raise SyntaxError(
                        f"Carácter ilegal '{valor}' en línea {linea}, columna {columna}"
                    )
            yield Token(tipo, valor, linea, columna)

    def _consumir_no_terminal(self, tokens: deque[Token]) -> Variable:
        """Consume un símbolo no terminal."""
        token = tokens.popleft()
        if token.tipo != "NO_TERMINAL":
            raise SyntaxError(
                "Se esperaba un símbolo no terminal en línea "
                f"{token.linea}, columna {token.columna}"
            )
        return Variable(token.valor[1:-1])

    def _consumir_signo_de_produccion(self, tokens: deque[Token]) -> None:
        """Consume el signo de producción de una producción."""
        token = tokens.popleft()
        if token.tipo != "PRODUCCION":
            raise SyntaxError(
                "Se esperaba un signo de producción en línea "
                f"{token.linea}, columna {token.columna}"
            )

    def _consumir_simbolo(self, tokens: deque[Token]) -> Simbolo:
        """Consume un símbolo terminal o no terminal."""
        token = tokens.popleft()
        match token.tipo:
            case "TERMINAL":
                return Terminal(json.loads(token.valor))
            case "NO_TERMINAL":
                return Variable(token.valor[1:-1])
        raise SyntaxError(
            "Se esperaba un símbolo terminal o no terminal en línea "
            f"{token.linea}, columna {token.columna}"
        )

    def _consumir_cadena(self, tokens: deque[Token]) -> Cadena:
        """Consume una cadena de símbolos terminales y no terminales."""
        cadena: list[Simbolo] = []
        assert tokens
        if tokens[0].tipo not in ("TERMINAL", "NO_TERMINAL"):
            raise SyntaxError(
                "Se esperaba un símbolo terminal o no terminal en línea "
                f"{tokens[0].linea}, columna {tokens[0].columna}"
            )
        while tokens and tokens[0].tipo in ("TERMINAL", "NO_TERMINAL"):
            cadena.append(self._consumir_simbolo(tokens))
        return Cadena(cadena)

    def _consumir_fin_de_linea(self, tokens: deque[Token]) -> bool:
        """Consume un salto de línea."""
        consumido = False
        while tokens:
            token = tokens[0]
            if token.tipo in ("NUEVA_LINEA", "FIN"):
                tokens.popleft()
                consumido = True
            else:
                break
        return consumido

    def _consumir_derecha(self, tokens: deque[Token]) -> UnionCadenas:
        """Consume la parte derecha de una producción."""
        derecha: list[Cadena] = []
        derecha.append(self._consumir_cadena(tokens))
        while tokens and tokens[0].tipo == "UNION":
            tokens.popleft()
            derecha.append(self._consumir_cadena(tokens))
        return UnionCadenas(derecha)

    def _consumir_produccion(self, tokens: deque[Token]) -> MultiRegla:
        """Consume una producción."""
        izq = self._consumir_no_terminal(tokens)
        self._consumir_signo_de_produccion(tokens)
        der = self._consumir_derecha(tokens)
        return MultiRegla(izq, der)

    def _consumir_gramatica(self, tokens: deque[Token]) -> GramaticaLibreContextoMap:
        """Consume una gramática."""
        gramatica: GramaticaLibreContextoDict = {}
        self._consumir_fin_de_linea(tokens)
        while tokens:
            izq, der = self._consumir_produccion(tokens)
            gramatica.setdefault(izq, []).extend(der)
            self._consumir_fin_de_linea(tokens)
        resultado = {izq: UnionCadenas(der) for izq, der in gramatica.items() if der}
        return resultado

    def diseccionar(self, texto: str) -> GramaticaLibreContextoMap:
        """
        Convierte un texto en BNF a una estructura de gramática.

        El texto debe estar en notación BNF y la gramática debe ser
        libre de contexto.

        Parámetros
        ----------
        texto : str
            El texto en notación BNF.

        Devuelve
        --------
        GramLibreContextoBNF
            Un diccionario que representa la gramática. Las llaves son
            los símbolos no terminales y los valores son listas de
            sucesiones de símbolos terminales y no terminales.
        """
        tokens = deque(self.tokenizar(texto))
        gramatica = self._consumir_gramatica(tokens)
        if tokens:
            raise SyntaxError(
                "Se esperaba el fin de la cadena en línea "
                f"{tokens[0].linea}, columna {tokens[0].columna}"
            )
        return gramatica
