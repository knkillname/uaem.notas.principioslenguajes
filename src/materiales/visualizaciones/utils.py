"""Utilidades para visualizaciones con Graphviz."""

from typing import Any

import pygraphviz  # type: ignore[import-untyped]


def dibujar_svg(arbol: pygraphviz.AGraph) -> str:
    """Genera SVG desde un grafo Graphviz, retornando texto.

    Levanta RuntimeError si el backend regresa None.
    """
    resultado: Any = arbol.draw(format="svg", prog="dot")
    if resultado is None:
        raise RuntimeError("Error al generar el SVG.")
    assert isinstance(resultado, bytes)
    return resultado.decode("utf-8")
