"""Visualización de un AST"""

import ast
import html

import pygraphviz  # type: ignore[import-untyped]

from .utils import dibujar_svg


class DiagramaAST:
    """Visualización de un AST"""

    # pylint: disable=too-few-public-methods

    attrs_arista = {
        "fontcolor": "darkolivegreen",
        "fontsize": "11",
        "color": "cornflowerblue",
        "arrowhead": "none",
        "fontname": "sans",
    }
    attrs_nodo = {"shape": "oval", "fontcolor": "firebrick", "fontsize": "14"}
    attrs_hoja = {"shape": "box", "fontname": "monospace"}

    def __init__(self, raiz: ast.Expression):
        self.raiz = raiz
        self._arbol: pygraphviz.AGraph
        self._cuenta_nodo = 0
        self._producir_arbol()

    def _producir_arbol(self) -> None:
        self._arbol = pygraphviz.AGraph(directed=True)
        self._visitar(self.raiz)

    def _visitar(self, nodo: ast.AST) -> str:
        """Recorrido en profundidad del AST"""
        self._cuenta_nodo += 1
        nombre = str(self._cuenta_nodo)
        if not isinstance(nodo, ast.AST):
            self._arbol.add_node(nombre, label=repr(nodo), **self.attrs_hoja)
            return nombre
        etiqueta = html.escape(type(nodo).__name__)
        self._arbol.add_node(nombre, label=f"<<i>{etiqueta}</i>>", **self.attrs_nodo)
        for campo, valor in ast.iter_fields(nodo):
            if isinstance(valor, (list, tuple)):
                for i, item in enumerate(valor):
                    hijo = self._visitar(item)
                    self._arbol.add_edge(
                        nombre, hijo, label=f"{campo}[{i}]", **self.attrs_arista
                    )
            else:
                hijo = self._visitar(valor)
                self._arbol.add_edge(nombre, hijo, label=campo, **self.attrs_arista)
        return nombre

    def _repr_svg_(self) -> str:
        return dibujar_svg(self._arbol)
