"""Cálculo de áreas y perímetros de figuras planas."""

from math import pi

import matplotlib.pyplot as plt


def area_cuadrado(lado: float) -> float:
    """Devuelve el área de un cuadrado de lado "lado".

    Parámetros
    ----------
    lado : float
        La longitud del lado del cuadrado.

    Devuelve
    --------
    float
        El área del cuadrado.
    """
    area = lado * lado
    return area


def perimetro_cuadrado(lado: float) -> float:
    """Devuelve el perímetro de un cuadrado."""
    return 4 * lado


def area_triangulo(base: float, altura: float) -> float:
    """Devuelve el área del triángulo"""
    return base * altura / 2


def dibujar_cuadrado(lado: float, ax: plt.axes) -> None:
    x = [0.0, 0.0, lado, lado, 0.0]
    y = [0.0, lado, lado, 0.0, 0.0]
    ax.plot(x, y)
