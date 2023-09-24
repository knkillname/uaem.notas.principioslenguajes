"""Módulo para trabajar con lenguajes numerables."""
import functools
from typing import Iterator


def cmp_shortlex(cadena_1: str, cadena_2: str) -> int:
    """Compara dos cadenas en orden shortlex.

    Parámetros
    ----------
    cadena_1 : str
        Primera cadena a comparar.
    cadena_2 : str
        Segunda cadena a comparar.

    Devuelve
    --------
    int
        -1 si cadena_1 va antes que cadena_2.
        0 si cadena_1 es igual a cadena_2.
        1 si cadena_1 va después que cadena_2.
    """
    if cadena_1 == cadena_2:
        return 0
    if len(cadena_1) < len(cadena_2):
        return -1
    if len(cadena_1) > len(cadena_2):
        return 1

    assert len(cadena_1) == len(cadena_2) and cadena_1 != cadena_2
    return -1 if cadena_1 < cadena_2 else 1  # Usamos orden lexicográfico


Shortlex = functools.cmp_to_key(cmp_shortlex)


def _pivote(cadena: str, malo: str) -> int:
    """Devuelve el índice del último carácter que no es malo.

    Parámetros
    ----------
    cadena : str
        La cadena sobre la que se busca el pivote.
    malo : str
        El carácter que se considera malo.

    Devuelve
    --------
    int
        El índice del último carácter que no es malo, o -1 si todos son
        malos.
    """
    for i in range(len(cadena) - 1, -1, -1):
        if cadena[i] != malo:
            return i
    return -1


def siguiente(cadena: str, alfabeto: str) -> str:
    """Devuelve la cadena siguiente en orden shortléxico.

    Parámetros
    ----------
    cadena : str
        Una cadena sobre el alfabeto dado.
    alfabeto : str
        Una cadena de caracteres ordenados shortléxicamente.

    Devuelve
    --------
    str
        La cadena siguiente en orden shortléxico.
    """
    i = _pivote(cadena, alfabeto[-1])
    if i == -1:  # Todos los caracteres son el último del alfabeto.
        return alfabeto[0] * (len(cadena) + 1)  # Agrega un carácter más.
    car = alfabeto[alfabeto.find(cadena[i]) + 1]  # Siguiente carácter.
    return cadena[:i] + car + (len(cadena) - i - 1) * alfabeto[0]


def estrella(alfabeto: str) -> Iterator[str]:
    """Genera todas las cadenas sobre el alfabeto dado.

    Parámetros
    ----------
    alfabeto : str
        Una cadena de caracteres ordenados shortléxicamente.

    Produce
    -------
    str
        Todas las cadenas sobre el alfabeto dado, en orden shortléxico.
    """
    cadena = ""
    while True:
        yield cadena
        cadena = siguiente(cadena, alfabeto)
