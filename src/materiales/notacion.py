"""Módulo para la notación de objetos matemáticos."""

from collections.abc import Hashable
from typing import Any, TypeVar

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


def quitar_dolares(texto: str) -> str:
    """Quita el entorno matemático de un texto LaTeX.

    La función devuelve el texto sin el entorno matemático, que puede
    estar dado por un signo $, un par de signos $$ o entre \\[ y \\].

    Parámetros
    ----------
    texto : str
        El texto LaTeX del que se quiere quitar el entorno matemático.

    Devuelve
    --------
    str
        El texto sin el entorno matemático.
    """
    texto = texto.strip()
    if texto.startswith("$$") and texto.endswith("$$"):
        return texto[2:-2]
    if texto.startswith("$") and texto.endswith("$"):
        return texto[1:-1]
    if texto.startswith("\\[") and texto.endswith("\\]"):
        return texto[2:-2]
    return texto


def obtener_latex(obj: Any) -> str:
    """Obtiene el código LaTeX de un objeto.

    Parámetros
    ----------
    obj : Any
        El objeto del que se quiere obtener el código LaTeX.

    Devuelve
    --------
    str
        El código LaTeX del objeto.
    """
    # pylint: disable=protected-access
    try:
        return quitar_dolares(obj._repr_latex_())
    except AttributeError:
        return str(obj)
