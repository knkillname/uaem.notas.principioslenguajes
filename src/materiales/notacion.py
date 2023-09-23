"""Módulo para la notación de objetos matemáticos."""


class Conjunto(frozenset):
    """Representa un conjunto de elementos."""

    def _repr_markdown_(self) -> str:
        # pylint: disable=protected-access
        elementos = []
        for elemento in self:
            try:
                elementos.append(elemento._repr_markdown_())
            except AttributeError:
                elementos.append(str(elemento))
        elementos.sort()
        interior = ", ".join(elementos)
        return f"{{{interior}}}"


class Sucesion(list):
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
