"""Módulo para la notación de objetos matemáticos."""

import itertools
from collections.abc import Hashable, Iterable, Iterator, Sequence
from typing import Any, TypeVar, overload

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
        self._datos: list[str] = list(
            itertools.islice(iterable, rebanada.start, rebanada.stop, rebanada.step)
        )

    @overload
    def __getitem__(self, indice: int) -> str:
        ...

    @overload
    def __getitem__(self, indice: slice) -> "Lenguaje":
        ...

    def __getitem__(self, indice):
        if isinstance(indice, slice):
            return Lenguaje(self._datos[indice], rebanada=slice(0, None, None))
        return self._datos[indice]

    def __len__(self) -> int:
        return len(self._datos)

    def _repr_latex_(self) -> str:
        # pylint: disable=protected-access
        cadenas: Iterator[str]
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
