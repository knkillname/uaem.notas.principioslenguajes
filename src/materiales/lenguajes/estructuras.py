"""Estructuras de datos para representar gramáticas libres de contexto."""
import abc
import collections
from collections.abc import Iterable, Mapping, Sequence
from typing import NamedTuple, NotRequired, Self, TypedDict

from ..notacion import obtener_latex as _latex


class Simbolo(collections.UserString, metaclass=abc.ABCMeta):
    """Representa un símbolo de una gramática."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.data!r})"

    def __str__(self) -> str:
        return self.data

    @abc.abstractmethod
    def _repr_markdown_(self) -> str:
        """Devuelve la representación Markdown del símbolo."""

    @abc.abstractmethod
    def _repr_latex_(self) -> str:
        """Devuelve la representación LaTeX del símbolo."""


class Variable(Simbolo):
    """Representa una variable."""

    def __str__(self) -> str:
        return f"<{self.data}>"

    def _repr_markdown_(self) -> str:
        return f"***{self.data}***"

    def _repr_latex_(self) -> str:
        return rf"${{{self.data}}}$"


class Terminal(Simbolo):
    """Representa un símbolo terminal."""

    def __str__(self) -> str:
        if self.data == "":
            return "ε"
        return f'"{self.data}"'

    def _repr_markdown_(self) -> str:
        if self.data == "":
            return r"${{\varepsilon}}$"
        return f"`{self.data}`"

    def _repr_latex_(self) -> str:
        if self.data == "":
            return r"$\varepsilon$"
        return rf"$\texttt{{{self.data}}}$"


TCadena = Sequence[Simbolo]


class Cadena(tuple[Simbolo]):
    """Representa una cadena de símbolos terminales y variables."""

    def __new__(cls, __iterable: Iterable[Simbolo]) -> Self:
        return super().__new__(cls, filter(None, __iterable))  # type: ignore

    def __str__(self) -> str:
        return "".join(str(s) for s in self)

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        if not self:
            return r"${\varepsilon}$"
        return "".join(s._repr_markdown_() for s in self)

    def _repr_latex_(self) -> str:
        # pylint: disable=protected-access
        if not self:
            return r"$\varepsilon$"
        return f"${' '.join(_latex(s) for s in self)}$"


class Produccion(NamedTuple):
    """Representa una producción con una cadena a la derecha."""

    izquierda: Variable
    derecha: Cadena

    def aplicar(self, cadena: Cadena, n_salto: int) -> Cadena:
        """Aplica la producción a una cadena.

        Parámetros
        ----------
        cadena : Cadena
            La cadena a la que se le aplicará la producción.
        n_salto : int
            El número de veces que se ha aplicado la producción.

        Devuelve
        --------
        Cadena
            La cadena resultante de aplicar la producción.
        """
        indices = [
            i
            for (i, simbolo) in enumerate(cadena)
            if isinstance(simbolo, Variable) and simbolo == self.izquierda
        ]
        i_var = indices[n_salto]
        return Cadena([*cadena[:i_var], *self.derecha, *cadena[i_var + 1 :]])

    def __str__(self) -> str:
        return f"{self.izquierda} → {' '.join(str(s) for s in self.derecha)}"

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        return (
            rf"{self.izquierda._repr_markdown_()} $\to$ "
            rf"{self.derecha._repr_markdown_()}"
        )

    def _repr_latex_(self) -> str:
        # pylint: disable=protected-access
        izquierda = _latex(self.izquierda)
        derecha = _latex(self.derecha)
        return rf"${izquierda} \to {derecha}$"


class DerivacionDict(TypedDict):
    """Representa una derivación de una gramática."""

    cadena: NotRequired[Cadena]
    n_produccion: int
    n_salto: NotRequired[int]


class UnionCadenas(tuple[Cadena, ...]):
    """Representa la unión de varias cadenas."""

    def __str__(self) -> str:
        return " | ".join("".join(str(s) for s in cad) for cad in self)

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        return " | ".join(cad._repr_markdown_() for cad in self)

    def _repr_latex_(self) -> str:
        # pylint: disable=protected-access
        return " \\mid ".join(_latex(cad) for cad in self)


class MultiProduccion(NamedTuple):
    """Representa una producción con varias cadenas a la derecha."""

    izquierda: Variable
    derecha: UnionCadenas

    def __str__(self) -> str:
        derecha = " | ".join(" ".join(str(s) for s in cad) for cad in self.derecha)
        return f"{self.izquierda} → {derecha}"

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        return (
            rf"{self.izquierda._repr_markdown_()} $\to$ "
            f"{self.derecha._repr_markdown_()}"
        )

    def _repr_latex_(self) -> str:
        # pylint: disable=protected-access
        return rf"{_latex(self.izquierda)} \to {_latex(self.derecha)}"


GramaticaLibreContextoMap = Mapping[Variable, UnionCadenas]
GramaticaLibreContextoDict = dict[Variable, list[Cadena]]
