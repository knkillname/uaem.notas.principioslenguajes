"""Módulo para la notación de objetos matemáticos."""

import itertools
from collections.abc import Hashable, Iterable, Sequence
from typing import Any, TypeVar

from materiales.lenguajes.estructuras import Terminal
from materiales.lenguajes.latex import obtener_latex

T = TypeVar("T", bound=Hashable)


class Conjunto(frozenset[T]):
    """Representa un conjunto de elementos."""

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        elementos = []
        for elemento in self:
            try:
                elementos.append(elemento._repr_markdown_())  # type: ignore
            except AttributeError:
                elementos.append(str(elemento))
        elementos.sort()
        interior = ", ".join(elementos)
        return f"{{{interior}}}"


class Lenguaje(Sequence[str]):
    """Representa un conjunto numerable de elementos."""

    def __init__(self, iterable: Iterable[str], *, rebanada: slice) -> None:
        self._rebanada = rebanada
        self._datos = list(
            itertools.islice(iterable, rebanada.start, rebanada.stop, rebanada.step)
        )

    def __getitem__(self, indice: int) -> str:
        return self._datos[indice]

    def __len__(self) -> int:
        return len(self._datos)

    def _repr_latex_(self) -> str:
        # pylint: disable=protected-access
        cadenas = (obtener_latex(Terminal(cadena)) for cadena in self._datos)
        cadenas = itertools.chain(cadenas, (r"\ldots",))
        return rf"$\{{{', '.join(cadenas)}\}}$"


class Sucesion(tuple[Any, ...]):
    """Representa una sucesión de elementos."""

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        elementos = []
        for elemento in self:
            try:
                elementos.append(elemento._repr_markdown_())
            except AttributeError:
                elementos.append(str(elemento))
        interior = ", ".join(elementos)
        return f"({interior})"


class ListaNumerada(tuple[Any, ...]):
    """Representa una lista numerada de elementos."""

    def __str__(self) -> str:
        return "\n".join(f"{i}. {e}" for i, e in enumerate(self, start=1))

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        elementos = []
        for elemento in self:
            try:
                elementos.append(elemento._repr_markdown_())
            except AttributeError:
                elementos.append(str(elemento))
        interior = "\n".join(f"{i}. {e}" for i, e in enumerate(elementos, start=1))
        return f"{interior}"
