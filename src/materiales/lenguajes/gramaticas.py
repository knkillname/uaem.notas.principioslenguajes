from collections import UserString
from collections.abc import Sequence
from typing import NamedTuple


class NoTerminal(UserString):
    """Representa un símbolo no terminal de una gramática.

    Un símbolo no terminal es un símbolo que puede ser reemplazado por
    una sucesión de símbolos terminales y no terminales.

    Atributos
    ---------
    data : str
        El nombre del símbolo no terminal.
    """

    def __repr__(self) -> str:
        return f"NoTerminal({self.data!r})"

    def __str__(self) -> str:
        """Devuelve la representación BNF del símbolo no terminal."""
        return f"<{self.data}>"

    def _repr_markdown_(self) -> str:
        """Devuelve la representación BNF del símbolo no terminal."""
        return f"<**{self.data}**>"


Simbolo = NoTerminal | str


def _a_markdown(obj: Simbolo) -> str:
    """Devuelve la representación Markdown de un símbolo.

    Si el símbolo es un `NoTerminal`, se devuelve su representación
    Markdown. Si no, se devuelve la representación `str` del símbolo.

    Parámetros
    ----------
    obj
        El símbolo a representar.

    Devuelve
    --------
    str
        La representación Markdown del símbolo.
    """
    # pylint: disable=protected-access
    try:
        return obj._repr_markdown_()
    except AttributeError:
        contenido = str(obj)
        if contenido:
            return f"“`{contenido}`”"
        return r"$\varepsilon$"


class Produccion(NamedTuple):
    """Representa una producción de una gramática.

    Una producción es una regla que indica cómo se puede reemplazar un
    símbolo no terminal por una sucesión de símbolos terminales y no
    terminales.

    Atributos
    ---------
    izq : NoTerminal
        El símbolo no terminal que se reemplaza.
    der : Sequence[Simbolo]
        La sucesión de símbolos terminales y no terminales por la que
        se reemplaza el símbolo no terminal.
    """

    izq: NoTerminal
    der: Sequence[Simbolo]

    def __str__(self) -> str:
        return f'{self.izq} ::= {" ".join(str(sim) for sim in self.der)}'

    def __repr__(self) -> str:
        return f"Produccion({self.izq!r}, {self.der!r})"

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        return (
            f"{_a_markdown(self.izq)} ::= "
            f'{" ".join(_a_markdown(sim) for sim in self.der)}'
        )


class Gramatica:
    """Representa una gramática.

    Una gramática es un conjunto de producciones.

    Atributos
    ---------
    producciones : list[Produccion]
        Las producciones de la gramática.
    """

    def __init__(self, producciones: Sequence[Produccion]) -> None:
        self.producciones = list(producciones)

    def __str__(self) -> str:
        return "\n".join(str(p) for p in self.producciones)

    def __repr__(self) -> str:
        return f"Gramatica({self.producciones!r})"

    def _repr_markdown_(self) -> str:
        producciones = self._recolectar()
        renglones = []
        for izq, derechas in producciones.items():
            izq_str = _a_markdown(izq)
            der = " | ".join(" ".join(map(_a_markdown, der)) for der in derechas)
            renglones.append(f"- {izq_str} ::= {der}")
        return "\n".join(renglones)

    def _recolectar(self) -> dict[NoTerminal, Sequence[Simbolo]]:
        """Recolecta las producciones de la gramática.

        Este método devuelve un diccionario que asocia cada símbolo no
        terminal de la gramática con una lista de sucesiones de
        símbolos terminales y no terminales, como en la notación BNF.

        Devuelve
        --------
        dict[NoTerminal, Sequence[Simbolo]]
            El diccionario que asocia cada símbolo no terminal con una
            lista de sucesiones de símbolos terminales y no terminales.
        """
        resultado = {}
        for izq, der in self.producciones:
            recolectadas = resultado.setdefault(izq, [])
            recolectadas.append(der)
        return resultado
