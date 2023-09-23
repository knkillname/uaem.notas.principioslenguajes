"""Estructuras de datos para representar gramáticas libres de contexto."""
import abc
import collections
from collections.abc import Mapping, Sequence
from typing import NamedTuple


class Simbolo(collections.UserString, metaclass=abc.ABCMeta):
    """Representa un símbolo de una gramática."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data!r})"

    def __str__(self) -> str:
        return self.data

    @abc.abstractmethod
    def _repr_markdown_(self) -> str:
        """Devuelve la representación Markdown del símbolo."""


class NoTerminal(Simbolo):
    """Representa un símbolo no terminal."""

    def __str__(self) -> str:
        contenido = self._extraer_contenido()
        return f"<{contenido}>"

    def _repr_markdown_(self) -> str:
        contenido = self._extraer_contenido()
        return f"***{contenido}***"

    def _extraer_contenido(self):
        contenido = self.data
        if contenido.startswith("<") and contenido.endswith(">"):
            contenido = contenido[1:-1]
        return contenido


class Terminal(Simbolo):
    """Representa un símbolo terminal."""

    def __str__(self) -> str:
        if self.data == "":
            return "ε"
        return f'"{self.data}"'

    def _repr_markdown_(self) -> str:
        if self.data == "":
            return r"$\varepsilon$"
        return f"`{self.data}`"


TCadena = Sequence[Simbolo]


class Cadena(list[Simbolo]):
    """Representa una cadena de símbolos terminales y no terminales."""

    def __str__(self) -> str:
        return " ".join(str(s) for s in self)

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        return " ".join(s._repr_markdown_() for s in self)


class Produccion(NamedTuple):
    """Representa una producción con una cadena a la derecha."""

    izquierda: NoTerminal
    derecha: TCadena

    def __str__(self) -> str:
        return f"{self.izquierda} → {' '.join(str(s) for s in self.derecha)}"

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        return (
            rf"{self.izquierda._repr_markdown_()} $\to$ "
            f"{''.join(s._repr_markdown_() for s in self.derecha)}"
        )


class MultiProduccion(NamedTuple):
    """Representa una producción con varias cadenas a la derecha."""

    izquierda: NoTerminal
    derecha: Sequence[TCadena]

    def __str__(self) -> str:
        derecha = " | ".join(" ".join(str(s) for s in cad) for cad in self.derecha)
        return f"{self.izquierda} → {derecha}"

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        derecha = " | ".join(
            " ".join(s._repr_markdown_() for s in cad) for cad in self.derecha
        )
        return rf"{self.izquierda._repr_markdown_()} $\to$ " f"{derecha}"


GramaticaLibreContextoMap = Mapping[NoTerminal, Sequence[TCadena]]
GramaticaLibreContextoDict = dict[NoTerminal, list[TCadena]]
