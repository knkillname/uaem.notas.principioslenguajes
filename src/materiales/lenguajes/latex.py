from typing import Any


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
