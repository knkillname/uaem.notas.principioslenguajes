"""Módulo de gramáticas libres de contexto."""
from collections.abc import Collection, Sequence
from typing import Self

from .. import notacion
from . import bnf
from .estructuras import (
    Cadena,
    GramaticaLibreContextoMap,
    MultiProduccion,
    NoTerminal,
    Produccion,
    TCadena,
    Terminal,
)


class GramaticaLibreContexto:
    """Representa una gramática libre de contexto."""

    def __init__(self, gramatica: GramaticaLibreContextoMap) -> None:
        """Inicializa la gramática."""
        self._datos: GramaticaLibreContextoMap = gramatica

    @classmethod
    def desde_cadena(cls, texto: str) -> Self:
        """
        Construye una gramática a partir de una cadena de texto.

        Parámetros
        ----------
        texto : str
            La cadena de texto en notación BNF.

        Devuelve
        --------
        GramaticaLibreContexto
            La gramática construida.
        """
        return cls(bnf.ParserBNFLibreContexto().diseccionar(texto))

    @property
    def no_terminales(self) -> Collection[NoTerminal]:
        """Devuelve los no terminales de la gramática."""
        resultado = set(self._datos.keys())
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, NoTerminal):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @property
    def terminales(self) -> Collection[Terminal]:
        """Devuelve los terminales de la gramática."""
        resultado = set()
        for cadenas in self._datos.values():
            for cadena in cadenas:
                for simbolo in cadena:
                    if isinstance(simbolo, Terminal):
                        resultado.add(simbolo)
        return notacion.Conjunto(resultado)

    @property
    def producciones(self) -> Collection[Produccion]:
        """Devuelve las producciones de la gramática."""
        resultado = set()
        for izq, der in self._datos.items():
            for cadena in der:
                resultado.add(Produccion(izq, tuple(cadena)))
        return notacion.Conjunto(resultado)

    @property
    def simbolo_inicial(self) -> NoTerminal:
        """Devuelve el símbolo inicial de la gramática."""
        return next(iter(self._datos.keys()))

    def reemplazos(self, simbolo: NoTerminal) -> Sequence[TCadena]:
        """
        Devuelve los reemplazos disponibles para un símbolo no terminal.

        Parámetros
        ----------
        simbolo : NoTerminal
            El símbolo no terminal que se desea reemplazar.

        Devuelve
        --------
        Sequence[Cadena]
            Una sucesión de cadenas de símbolos terminales y no
            terminales.
        """
        resultados = [Cadena(r) for r in self._datos.get(simbolo, ())]
        return notacion.Sucesion(resultados)

    def __repr__(self) -> str:
        """Devuelve una representación de la gramática."""
        return f"{self.__class__.__name__}({self._datos!r})"

    def __str__(self) -> str:
        """Devuelve una representación de la gramática."""
        renglones = (MultiProduccion(izq, der) for izq, der in self._datos.items())
        return "\n".join(str(prod) for prod in renglones)

    def _repr_markdown_(self) -> str:
        """Devuelve una representación de la gramática."""
        # pylint: disable=protected-access
        renglones = (MultiProduccion(izq, der) for izq, der in self._datos.items())
        return "\n".join(f"- {prod._repr_markdown_()}" for prod in renglones)
