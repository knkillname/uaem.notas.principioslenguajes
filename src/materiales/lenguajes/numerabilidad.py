"""Módulo para trabajar con lenguajes numerables."""
import functools
import itertools
from collections.abc import Iterable, Iterator
from typing import TypeVar

import numpy as np


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
    for longitud in itertools.count():  # 0, 1, 2, ...
        for cadena in itertools.product(alfabeto, repeat=longitud):
            yield "".join(cadena)


T = TypeVar("T")


def muestra(iterable: Iterable[T], n_elementos: int, orden: int = 16) -> list[T]:
    """
    Devuelve una muestra aleatoria de elementos de un iterable infinito.

    Parámetros
    ----------
    iterable : Iterable[T]
        Un iterable infinito.
    n_elementos : int
        Número de elementos a tomar de iterable.
    orden : int, opcional
        Orden de la muestra. Entre más grande sea, más grandes serán los
        índices de los elementos tomados. Por defecto es 16.

    Devuelve
    --------
    list[T]
        Una lista de n_elementos elementos tomados aleatoriamente de
        iterable.
    """
    indices = np.zeros(n_elementos + 1, dtype=int)
    indices[1:] = np.random.geometric(1 / 2**orden, size=n_elementos)
    indices.sort()
    indices = np.diff(indices)

    iterator = iter(iterable)
    # Usar islice para obtener los elementos de iterable en los índices dados
    return [next(itertools.islice(iterator, i, None)) for i in indices]
