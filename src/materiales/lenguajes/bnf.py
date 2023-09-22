import json
import re
from collections import deque
from typing import Iterator, NamedTuple

GramLibreContextoBNF = dict[str, list[list[str]]]


class Token(NamedTuple):
    tipo: str
    valor: str
    linea: int
    columna: int


class ParserBNFLibreContexto:
    """Analizador sintáctico para gramáticas en notación BNF."""

    spec_tokens = {
        "NO_TERMINAL": r"<\w+?>",  # Los no terminales están entre corchetes angulares
        "TERMINAL": r'".*?"',  # Los terminales están entre comillas dobles
        "UNION": r"\|",  # La unión es el símbolo |
        "PRODUCCION": r"::=",  # La producción se simboliza con ::=
        "NUEVA_LINEA": r"\n",  # Salto de línea
        "COMENTARIO": r"\#.*?\n",  # Los comentarios comienzan con #
        "ESPACIO": r"\s+",  # Cualquier espacio en blanco
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
            valor = coincidencia.group(tipo)
            columna = coincidencia.start() - inicio_de_linea + 1
            match tipo:
                case "TERMINAL":
                    valor = json.loads(valor)  # Lee la cadena como JSON
                case "ESPACIO":
                    continue  # Ignora espacios
                case "NUEVA_LINEA" | "COMENTARIO":
                    linea += 1
                    inicio_de_linea = coincidencia.end()
                case "ERROR":
                    raise ValueError(
                        f"Carácter ilegal '{valor}' en línea {linea}, columna {columna}"
                    )
            yield Token(tipo, valor, linea, columna)

    def _consumir_izq(self, tokens: deque[Token]) -> str:
        """Consume el símbolo no terminal de la izquierda de una producción."""
        token = tokens.popleft()
        if token.tipo != "NO_TERMINAL":
            raise ValueError(
                f"Se esperaba un símbolo no terminal en línea {token.linea}, columna {token.columna}"
            )
        return token.valor

    def _consumir_signo_de_produccion(self, tokens: deque[Token]) -> None:
        """Consume el signo de producción de una producción."""
        token = tokens.popleft()
        if token.tipo != "PRODUCCION":
            raise ValueError(
                "Se esperaba un signo de producción en línea "
                f"{token.linea}, columna {token.columna}"
            )

    def _consumir_simbolo(self, tokens: deque[Token]) -> str:
        """Consume un símbolo terminal o no terminal."""
        token = tokens.popleft()
        if token.tipo not in ("TERMINAL", "NO_TERMINAL"):
            raise ValueError(
                "Se esperaba un símbolo terminal o no terminal en línea "
                f"{token.linea}, columna {token.columna}"
            )
        return token.valor

    def _consumir_cadena(self, tokens: deque[Token]) -> list[str]:
        """Consume una cadena de símbolos terminales y no terminales."""
        cadena: list[str] = []
        if tokens[0] not in ("TERMINAL", "NO_TERMINAL"):
            raise ValueError(
                "Se esperaba un símbolo terminal o no terminal en línea "
                f"{tokens[0].linea}, columna {tokens[0].columna}"
            )
        while tokens and tokens[0].tipo in ("TERMINAL", "NO_TERMINAL"):
            cadena.append(self._consumir_simbolo(tokens))
        return cadena

    def _consumir_fin_de_linea(self, tokens: deque[Token]) -> None:
        """Consume un salto de línea."""
        token = tokens.popleft()
        if token.tipo not in ("NUEVA_LINEA", "FIN"):
            raise ValueError(
                "Se esperaba un salto de línea en línea "
                f"{token.linea}, columna {token.columna}"
            )

    def _consumir_derecha(self, tokens: deque[Token]) -> list[list[str]]:
        """Consume la parte derecha de una producción."""
        derecha: list[list[str]] = []
        derecha.append(self._consumir_cadena(tokens))
        while tokens and tokens[0].tipo == "UNION":
            tokens.popleft()
            derecha.append(self._consumir_cadena(tokens))
        return derecha

    def _consumir_produccion(self, tokens: deque[Token]) -> tuple[str, list[list[str]]]:
        """Consume una producción."""
        izq = self._consumir_izq(tokens)
        self._consumir_signo_de_produccion(tokens)
        der = self._consumir_derecha(tokens)
        self._consumir_fin_de_linea(tokens)
        return izq, der

    def _consumir_gramatica(self, tokens: deque[Token]) -> GramLibreContextoBNF:
        """Consume una gramática."""
        gramatica: GramLibreContextoBNF = {}
        while tokens:
            izq, der = self._consumir_produccion(tokens)
            gramatica.setdefault(izq, []).extend(der)
        return gramatica

    def diseccionar(self, texto: str) -> GramLibreContextoBNF:
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
            raise ValueError(
                "Se esperaba el fin de la cadena en línea "
                f"{tokens[0].linea}, columna {tokens[0].columna}"
            )
        return gramatica


if __name__ == "__main__":
    TEXTO = """
    # Comentario
    <S> ::= <S> <S> | <S> <S> <S> | "a"
    """
    parser = ParserBNFLibreContexto()
    print(TEXTO)
    for token in parser.tokenizar(TEXTO):
        print(token)
    print(parser.diseccionar(TEXTO))
